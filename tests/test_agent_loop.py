import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('agent_loop',ROOT/'template/tool/agent_loop.py')
loop=importlib.util.module_from_spec(spec);spec.loader.exec_module(loop)

class BranchRoleTests(unittest.TestCase):
    def test_workers_cannot_push_main(self):
        for role in ('agent-a','agent-b','agent-c'):self.assertFalse(loop.valid_branch(role,'main'))
    def test_each_worker_owns_prefix(self):
        for role in ('agent-a','agent-b','agent-c'):
            self.assertTrue(loop.valid_branch(role,'work/'+role+'/task-1'))
            self.assertFalse(loop.valid_branch(role,'work/other/task'))
    def test_captain_owns_main_integration(self):
        self.assertTrue(loop.valid_branch('captain','main'))
        self.assertTrue(loop.valid_branch('captain','integration/batch1'))
        self.assertFalse(loop.valid_branch('captain','work/agent-a/task'))
    def test_head_cli_legacy_alias(self):self.assertTrue(loop.valid_branch('head','main'))
    def test_worker_branch_push_not_main(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'project';remote=Path(temp)/'remote.git';root.mkdir()
            def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL).decode().strip()
            subprocess.run(['git','init','--bare','-q',str(remote)],check=True)
            git('init','-b','main','-q');git('config','user.name','Fixture');git('config','user.email','fixture@example.test')
            (root/'tool').mkdir();(root/'tool/preflight.py').write_text('raise SystemExit(0)\n')
            (root/'tool/agent_loop.py').write_bytes((ROOT/'template/tool/agent_loop.py').read_bytes())
            git('add','.');git('commit','-qm','chore: fixture');baseline=git('rev-parse','HEAD')
            git('remote','add','origin',str(remote));git('push','-qu','origin','main');git('switch','-qc','work/agent-a/task')
            (root/'feature.txt').write_text('test-only feature')
            result=subprocess.run(['python3','tool/agent_loop.py','--role','agent-a','--files','feature.txt','-m','feat: fixture feature','--push'],cwd=root,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertEqual(baseline,git('ls-remote','origin','refs/heads/main').split()[0])
            self.assertEqual(git('rev-parse','HEAD'),git('ls-remote','origin','refs/heads/work/agent-a/task').split()[0])
            self.assertIn('No merge performed',result.stdout)
    def test_worker_main_rejected_before_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'tool').mkdir()
            (root/'tool/agent_loop.py').write_bytes((ROOT/'template/tool/agent_loop.py').read_bytes())
            subprocess.run(['git','init','-b','main','-q'],cwd=root,check=True)
            result=subprocess.run(['python3','tool/agent_loop.py','--role','agent-c','--files','x','-m','feat: x','--push'],cwd=root,capture_output=True,text=True)
            self.assertNotEqual(0,result.returncode);self.assertIn('Wrong branch',result.stderr)

if __name__=='__main__':unittest.main()
