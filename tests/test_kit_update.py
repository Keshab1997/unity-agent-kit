import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kit_update',ROOT/'template/tool/kit_update.py')
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)

class UpdateTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def put(self,name,data):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    def plan(self,new,old=None,**kw):return u.plan(self.root,new,old or {},{'files':{}},**kw)
    def test_check_plan_no_writes(self):
        changes,*_=self.plan({'tool/a.py':b'new'})
        self.assertEqual({'tool/a.py':b'new'},changes);self.assertFalse((self.root/'tool').exists())
    def test_unmodified_tool_updates(self):
        self.put('tool/a.py',b'old');result=self.plan({'tool/a.py':b'new'},{'tool/a.py':b'old'})
        self.assertEqual(b'new',result[0]['tool/a.py']);self.assertFalse(result[1])
    def test_customized_changed_tool_conflicts(self):
        self.put('tool/a.py',b'owner');result=self.plan({'tool/a.py':b'new'},{'tool/a.py':b'old'})
        self.assertEqual(['tool/a.py'],result[1]);self.assertFalse(result[0])
    def test_upstream_unchanged_preserves_customization(self):
        self.put('tool/a.py',b'owner');result=self.plan({'tool/a.py':b'old'},{'tool/a.py':b'old'})
        self.assertFalse(result[0]);self.assertFalse(result[1])
    def test_workflow_explicit_approval(self):
        new={'.github/workflows/a.yml':b'workflow'}
        self.assertTrue(self.plan(new)[2]);self.assertFalse(self.plan(new,allow_workflows=True)[2])
    def test_owner_notes_preserved(self):
        old=(u.START+'\nold\n'+u.END+'\nDefault notes').encode()
        new=(u.START+'\nnew\n'+u.END+'\nDifferent default notes').encode()
        current=(u.START+'\nold\n'+u.END+'\nOWNER CUSTOM NOTES').encode()
        self.put('AGENTS.md',current);result=self.plan({'AGENTS.md':new},{'AGENTS.md':old})
        self.assertIn(b'OWNER CUSTOM NOTES',result[0]['AGENTS.md']);self.assertNotIn(b'Different default notes',result[0]['AGENTS.md'])
    def test_custom_managed_block_conflicts(self):
        self.put('AGENTS.md',(u.START+'CUSTOM'+u.END).encode())
        self.assertTrue(self.plan({'AGENTS.md':(u.START+'NEW'+u.END).encode()},{'AGENTS.md':(u.START+'OLD'+u.END).encode()})[1])
    def test_game_paths_never_update(self):
        for name in ('unity-kit.json','docs/GAME_BRIEF.md','Assets/Game.cs','Packages/manifest.json','ProjectSettings/ProjectVersion.txt','../secret','tool/../secret','secrets/key.txt',''):
            self.assertFalse(u.eligible(name),name)
    def test_gitignore_preserves_user_lines(self):
        self.put('.gitignore',b'owner-cache/\n');result=self.plan({'.gitignore':b'Library/\n'})
        self.assertEqual(b'owner-cache/\nLibrary/\n',result[0]['.gitignore'])
    def test_symlink_rejected(self):
        (self.root/'tool').symlink_to(self.root/'elsewhere')
        with self.assertRaises(ValueError):self.plan({'tool/a.py':b'x'})
    def test_removed_upstream_not_deleted(self):
        self.put('tool/legacy.py',b'old');result=self.plan({}, {'tool/legacy.py':b'old'})
        self.assertTrue(result[3]);self.assertTrue((self.root/'tool/legacy.py').exists())
    def test_apply_success(self):
        u.apply_transaction(self.root,{'tool/a.py':b'new'},b'{"revision":"new"}',preflight=False)
        self.assertEqual(b'new',(self.root/'tool/a.py').read_bytes())
    def test_failed_preflight_restores_contents_and_lock(self):
        self.put('tool/a.py',b'old');self.put('unity-kit.lock.json',b'old-lock')
        with patch.object(u.subprocess,'run',side_effect=subprocess.CalledProcessError(1,'preflight')):
            with self.assertRaises(ValueError):u.apply_transaction(self.root,{'tool/a.py':b'new','agents/NEW.md':b'new'},b'new-lock')
        self.assertEqual(b'old',(self.root/'tool/a.py').read_bytes());self.assertEqual(b'old-lock',(self.root/'unity-kit.lock.json').read_bytes())
        self.assertFalse((self.root/'agents/NEW.md').exists())
    def test_new_unowned_path_conflict(self):
        self.put('tool/custom.py',b'mine');self.assertTrue(self.plan({'tool/custom.py':b'upstream'})[1])
    def test_manual_synced_file_accepted(self):
        self.put('tool/a.py',b'new');result=self.plan({'tool/a.py':b'new'},{'tool/a.py':b'old'})
        self.assertFalse(result[0]);self.assertFalse(result[1])
    def test_apply_requires_pinned_ref_before_network(self):
        result=subprocess.run(['python3',str(ROOT/'template/tool/kit_update.py'),'--apply'],capture_output=True,text=True)
        self.assertEqual(2,result.returncode);self.assertIn('--apply requires --ref',result.stderr)

if __name__=='__main__':unittest.main()
