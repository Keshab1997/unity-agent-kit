import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('secrets_check',ROOT/'template/tool/secrets_check.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

class SecretAuditTests(unittest.TestCase):
    def env(self):
        return {'UNITY_LICENSE':'<root><License/></root>','UNITY_EMAIL':'sample@example.test',
                'UNITY_PASSWORD':'PRIVATE-SENTINEL-PASSWORD','ANDROID_KEYSTORE_BASE64':'YQ==',
                'KEYSTORE_PASSWORD':'PRIVATE-STORE-SENTINEL','KEY_ALIAS':'PRIVATE-ALIAS-SENTINEL',
                'KEY_PASSWORD':'PRIVATE-KEY-SENTINEL','PLAY_SERVICE_ACCOUNT_JSON':json.dumps({
                    'type':'service_account','client_email':'service@example.test','private_key':'BEGIN PRIVATE KEY sentinel'})}
    def test_missing_secrets_are_crossed(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output): code=audit.report({})
        self.assertEqual(1,code)
        for name in audit.NAMES:self.assertIn(f'`{name}` | ❌',output.getvalue())
    def test_valid_structure_is_not_runtime_success(self):
        rows=audit.formats(self.env())
        self.assertTrue(all(p and ok for _,p,ok,_ in rows))
        self.assertTrue(any('activation NOT verified' in detail for *_,detail in rows))
    def test_bad_formats(self):
        env=self.env();env.update(UNITY_LICENSE='not xml',UNITY_EMAIL='wrong',ANDROID_KEYSTORE_BASE64='!!!',PLAY_SERVICE_ACCOUNT_JSON='{}')
        rows={name:ok for name,_,ok,_ in audit.formats(env)}
        for name in ('UNITY_LICENSE','UNITY_EMAIL','ANDROID_KEYSTORE_BASE64','PLAY_SERVICE_ACCOUNT_JSON'):self.assertFalse(rows[name])
    def test_default_has_no_network(self):
        with patch.object(audit,'live_play_check') as live,patch.object(audit,'signing_check',return_value=(True,'Probe passed')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,audit.report(self.env()))
        live.assert_not_called()
    def test_values_never_logged_or_summarized(self):
        env=self.env();out=io.StringIO()
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'summary.md'
            with patch.object(audit,'signing_check',return_value=(True,'Probe passed')),contextlib.redirect_stdout(out):audit.report(env,str(path))
            text=out.getvalue()+path.read_text()
        for value in env.values():self.assertNotIn(value,text)
    def test_signing_missing_secrets_does_not_run_tools(self):
        with patch.object(audit,'run') as run:
            self.assertFalse(audit.signing_check({})[0])
        run.assert_not_called()
    def test_signing_subprocess_output_is_suppressed(self):
        from types import SimpleNamespace
        with patch.object(audit.shutil,'which',return_value='/bin/jarsigner'),patch.object(audit,'run',return_value=SimpleNamespace(returncode=1,stdout=b'PRIVATE',stderr=b'PASSWORD')):
            ok,detail=audit.signing_check(self.env())
        self.assertFalse(ok);self.assertNotIn('PRIVATE',detail);self.assertNotIn('PASSWORD',detail)
    def test_signing_passwords_not_in_command(self):
        from types import SimpleNamespace
        env=self.env()
        with patch.object(audit.shutil,'which',return_value='/bin/jarsigner'),patch.object(audit,'run',return_value=SimpleNamespace(returncode=0,stdout=b'',stderr=b'')) as run:
            self.assertTrue(audit.signing_check(env)[0])
            cmd=run.call_args_list[0].args[0]
            self.assertNotIn(env['KEYSTORE_PASSWORD'],cmd);self.assertNotIn(env['KEY_PASSWORD'],cmd)
            self.assertIn('-storepass:env',cmd);self.assertIn('-keypass:env',cmd)
    def test_invalid_live_json_cannot_trigger_network(self):
        with patch.object(audit,'request') as request:
            self.assertFalse(audit.live_play_check({},'com.example.test')[0][0])
        request.assert_not_called()
    def test_live_exception_not_exposed(self):
        from types import SimpleNamespace
        with patch.object(audit,'run',return_value=SimpleNamespace(returncode=0,stdout=b'FAKE',stderr=b'')),patch.object(audit,'request',side_effect=RuntimeError('PRIVATE-SENTINEL')):
            result=audit.live_play_check(self.env(),'com.example.test')
        self.assertFalse(result[0][0]);self.assertNotIn('PRIVATE-SENTINEL',str(result))
    def test_workflow_manual_main_only(self):
        workflow=(ROOT/'template/.github/workflows/secrets-check.yml').read_text()
        self.assertIn('workflow_dispatch:',workflow);self.assertIn("github.ref == 'refs/heads/main'",workflow)
        self.assertIn('default: false',workflow)
        for name in audit.NAMES:self.assertIn(name+': ${{ secrets.'+name+' }}',workflow)

if __name__=='__main__':unittest.main()
