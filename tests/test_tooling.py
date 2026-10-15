import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
installer=load('installer','install.py')
preflight=load('preflight','template/tool/preflight.py')
planner=load('planner','template/tool/plan_checks.py')
gate=load('gate','template/tool/ci_gate.py')
results=load('results','template/tool/verify_test_results.py')

class InstallerTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'game'
    def tearDown(self): self.tmp.cleanup()
    def install(self,**kw):
        with contextlib.redirect_stdout(io.StringIO()): return installer.install(self.root,**kw)
    def test_new_and_idempotent(self):
        self.install(new=True);first=(self.root/'AGENTS.md').read_bytes()
        self.install(new=True);self.assertEqual(first,(self.root/'AGENTS.md').read_bytes())
        self.assertTrue((self.root/'Assets/UnityAgentKit/Editor/KitBuild.cs.meta').exists())
    def test_four_agent_pack_installed(self):
        self.install(new=True)
        contract=(self.root/'AGENTS.md').read_text()
        head=(self.root/'agents/HEAD.md').read_text()
        qa=(self.root/'agents/QA.md').read_text()
        self.assertIn('four agents total',contract)
        self.assertIn('agents/QA.md',contract)
        self.assertIn('Reviewer/QA',head)
        self.assertIn('exact integrated candidate SHA',head)
        self.assertIn('Read-only by default',qa)
        self.assertIn('No push, merge, CI dispatch',qa)
        self.assertIn('exclusive test paths',head)
    def test_dry_run_writes_nothing(self):
        self.install(new=True,dry=True);self.assertFalse(self.root.exists())
    def test_conflict_is_non_destructive(self):
        self.root.mkdir();(self.root/'AGENTS.md').write_text('Owner notes')
        (self.root/'tool').mkdir();(self.root/'tool/doctor.py').write_text('existing')
        with self.assertRaises(ValueError): self.install(new=True)
        self.assertEqual('Owner notes',(self.root/'AGENTS.md').read_text())
        self.assertFalse((self.root/'Packages').exists())
    def test_owner_notes_survive(self):
        self.root.mkdir();(self.root/'AGENTS.md').write_text('# Owner\nKeep this exactly.\n')
        self.install(new=True);text=(self.root/'AGENTS.md').read_text();self.assertIn('Keep this exactly.',text)
        self.install(new=True);self.assertEqual(text,(self.root/'AGENTS.md').read_text())
    def test_existing_settings_identity_preserved(self):
        self.install(new=True);p=self.root/'ProjectSettings/ProjectVersion.txt';p.write_text('m_EditorVersion: 6000.0.40f1\n')
        c=self.root/'unity-kit.json';data=json.loads(c.read_text());data['packageName']='com.owner.realgame';c.write_text(json.dumps(data))
        self.install(new=False);self.assertIn('6000.0.40f1',p.read_text());self.assertIn('com.owner.realgame',c.read_text())
    def test_symlink_rejected_before_writes(self):
        self.root.mkdir();(self.root/'tool').symlink_to(Path(self.tmp.name)/'elsewhere')
        with self.assertRaises(ValueError):self.install(new=True)
        self.assertFalse((self.root/'AGENTS.md').exists())
    def test_installed_starter_preflight(self):
        self.install(new=True)
        subprocess.run(['git','init','-q'],cwd=self.root,check=True)
        files=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=self.root).decode().splitlines()
        self.assertEqual([],preflight.inspect(self.root,files))

class PreflightTests(unittest.TestCase):
    def check(self,files):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name,text in files.items():p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
            return preflight.inspect(root,list(files))
    def test_bad_json_and_python(self):
        self.assertEqual(2,len(self.check({'a.json':'{','x.py':'def x('})))
    def test_detect_token_no_value_leak(self):
        token='gh'+'p_'+'a'*36
        errors=self.check({'bad.txt':token});self.assertTrue(errors);self.assertNotIn(token,str(errors))
    def test_private_key(self):
        self.assertTrue(self.check({'bad.txt':'-----BEGIN '+'PRIVATE KEY-----'}))
    def test_missing_meta(self):self.assertTrue(self.check({'Assets/A.cs':'class A {}'}))
    def test_duplicate_guid(self):
        guid='a'*32
        errors=self.check({'Assets/A.cs':'','Assets/B.cs':'','Assets/A.cs.meta':'guid: '+guid,'Assets/B.cs.meta':'guid: '+guid})
        self.assertTrue(any('duplicate GUID' in e for e in errors))
    def test_orphan_meta(self):self.assertTrue(self.check({'Assets/A.cs.meta':'guid: '+'a'*32}))
    def test_generated_and_key(self):self.assertTrue(self.check({'Library/a':'x','upload.keystore':'x'}))

class RiskTests(unittest.TestCase):
    def test_docs(self):self.assertEqual('preflight',planner.plan(['README.md'])['recommended'])
    def test_cs(self):self.assertEqual('targeted',planner.plan(['Assets/Player.cs'])['recommended'])
    def test_scene(self):self.assertEqual('full',planner.plan(['Assets/Level.unity'])['recommended'])
    def test_shared(self):self.assertEqual('full',planner.plan(['Assets/Shared/Api.cs'])['recommended'])

class GateTests(unittest.TestCase):
    def env(self):
        return {key:'configured' for key in ('UNITY_LICENSE','UNITY_EMAIL','UNITY_PASSWORD','ANDROID_KEYSTORE_BASE64','KEYSTORE_PASSWORD','KEY_ALIAS','KEY_PASSWORD','PLAY_SERVICE_ACCOUNT_JSON')}
    def test_flutter_signing_names_required_individually(self):
        env=self.env();env.update(KIT_STAGE='build',KIT_VERSION_CODE='100',KIT_TARGET_API='36')
        config={'packageName':'com.owner.game'}
        self.assertEqual([],gate.validate(env,config))
        for key in ('ANDROID_KEYSTORE_BASE64','KEYSTORE_PASSWORD','KEY_ALIAS','KEY_PASSWORD'):
            with self.subTest(key=key):
                missing=dict(env);del missing[key]
                self.assertIn('Missing GitHub secret: '+key,gate.validate(missing,config))
    def test_workflow_maps_flutter_names_to_builder_inputs(self):
        workflow=(ROOT/'template/.github/workflows/unity-android.yml').read_text()
        for field,secret in {'androidKeystoreBase64':'ANDROID_KEYSTORE_BASE64',
                             'androidKeystorePass':'KEYSTORE_PASSWORD',
                             'androidKeyaliasName':'KEY_ALIAS',
                             'androidKeyaliasPass':'KEY_PASSWORD'}.items():
            self.assertIn(field+': ${{ secrets.'+secret+' }}',workflow)
            self.assertIn(secret+': ${{ secrets.'+secret+' }}',workflow)
        self.assertIn('serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}',workflow)
    def test_preflight_without_secrets(self):self.assertEqual([],gate.validate({},{}))
    def test_targeted_requires_filter(self):
        env=self.env();env['KIT_STAGE']='targeted';self.assertTrue(gate.validate(env,{}))
    def test_shell_characters_rejected(self):
        env=self.env();env.update(KIT_STAGE='targeted',KIT_FILTER='X;$(evil)');self.assertTrue(gate.validate(env,{}))
    def test_internal_requires_confirmation_and_main(self):
        env=self.env();env.update(KIT_STAGE='internal',KIT_VERSION_CODE='100',KIT_TARGET_API='36')
        self.assertTrue(gate.validate(env,{'packageName':'com.owner.game'}))
        env.update(KIT_CONFIRM='UPLOAD INTERNAL',GITHUB_REF='refs/heads/main')
        self.assertEqual([],gate.validate(env,{'packageName':'com.owner.game'}))
    def test_missing_signing_and_bad_version(self):
        self.assertTrue(gate.validate({'KIT_STAGE':'build','KIT_VERSION_CODE':'0'},{}))
    def test_production_not_supported(self):self.assertTrue(gate.validate({'KIT_STAGE':'production'},{}))

class ResultTests(unittest.TestCase):
    def check(self,files,both=False):
        with tempfile.TemporaryDirectory() as d:
            for n,t in files.items():(Path(d)/n).write_text(t)
            return results.verify(d,both)
    def test_missing(self):self.assertTrue(self.check({}))
    def test_empty_filter(self):self.assertTrue(self.check({'results.xml':'<test-run result="Passed"/>'}))
    def test_failed(self):self.assertTrue(self.check({'results.xml':'<test-run result="Failed"><test-case result="Failed"/></test-run>'}))
    def test_full_requires_both(self):
        xml='<test-run result="Passed"><test-case result="Passed"/></test-run>'
        self.assertTrue(self.check({'editmode.xml':xml},True))
        self.assertEqual([],self.check({'editmode.xml':xml,'playmode.xml':xml},True))
    def test_not_runnable_is_failure(self):
        self.assertTrue(self.check({'results.xml':'<test-run result="Passed"><test-case result="Passed"/><test-case result="NotRunnable"/></test-run>'}))
    def test_skipped_only(self):self.assertTrue(self.check({'results.xml':'<test-run result="Passed"><test-case result="Skipped"/></test-run>'}))

if __name__=='__main__':unittest.main()
