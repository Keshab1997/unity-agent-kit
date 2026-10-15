#!/usr/bin/env python3
"""Offline, conservative installer. Run from a reviewed/pinned clone. Python >=3.10."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
START='<!-- unity-agent-kit:start -->'
END='<!-- unity-agent-kit:end -->'

def merge_agents(existing,incoming):
    block=incoming.split(END)[0]+END
    if START in existing:
        if existing.count(START)!=1 or existing.count(END)!=1: raise ValueError('Malformed managed AGENTS block')
        a=existing.index(START);b=existing.index(END)+len(END)
        if existing[a:b]!=block: raise ValueError('Existing managed AGENTS differs; review upgrade manually (owner notes preserved)')
        return existing
    return existing.rstrip()+'\n\n'+block+'\n' if existing else incoming

def install(project,new=False,version='6000.3.3f1',dry=False):
    project=Path(project).absolute()
    if project.is_symlink(): raise ValueError('Project root cannot be a symlink')
    if not re.fullmatch(r'\d+\.\d+\.\d+[abfp]\d+',version): raise ValueError('Exact Unity version required')
    if not new and not (project/'ProjectSettings/ProjectVersion.txt').exists():
        raise ValueError('Existing project must have ProjectSettings/ProjectVersion.txt; use --new-project for a starter')
    payload={}
    for base in ('template','project'):
        for file in (SOURCE/base).rglob('*'):
            if not file.is_file() or '__pycache__' in file.parts: continue
            rel=file.relative_to(SOURCE/base)
            if base=='project' and not new and rel.parts[0]!='Assets':continue
            payload[rel.as_posix()]=file.read_bytes()
    if new: payload['ProjectSettings/ProjectVersion.txt']=f'm_EditorVersion: {version}\n'.encode()
    changes={};conflicts=[]
    for name,data in payload.items():
        dest=project/name
        if any(p.is_symlink() for p in [dest,*dest.parents]): raise ValueError(f'Symlink path rejected: {name}')
        if dest.exists():
            if not dest.is_file(): conflicts.append(name);continue
            old=dest.read_bytes()
            if name=='AGENTS.md': data=merge_agents(old.decode(),data.decode()).encode()
            elif name=='.gitignore':
                lines=old.decode().splitlines();extra=[s for s in data.decode().splitlines() if s and s not in lines]
                data=old+(b'\n' if old and not old.endswith(b'\n') else b'')+'\n'.join(extra).encode()+(b'\n' if extra else b'')
            elif name=='unity-kit.json': continue # project identity belongs to owner
            elif old!=data: conflicts.append(name);continue
            if old==data: continue
        changes[name]=data
    if conflicts: raise ValueError('Refusing to overwrite existing files: '+', '.join(conflicts))
    try: revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError: revision='uncommitted-local-source'
    receipt={'source':'Keshab1997/unity-agent-kit','revision':revision,
             'files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(payload.items())}}
    changes['unity-kit.lock.json']=(json.dumps(receipt,indent=2)+'\n').encode()
    for name in sorted(changes): print(('WOULD WRITE ' if dry else 'WRITE ')+name)
    if not dry:
        for name,data in changes.items():
            path=project/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Dry run complete.' if dry else 'Installed. No git commit/push, network, CI, secrets or Play upload performed.')
    print('Next: read AGENTS.md and docs/SETUP.md; configure unity-kit.json; run tool/doctor.py and tool/preflight.py.')
    return changes
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',required=True);p.add_argument('--new-project',action='store_true');p.add_argument('--unity-version',default='6000.3.3f1');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    try: install(a.project,a.new_project,a.unity_version,a.dry_run)
    except ValueError as e: sys.exit('ERROR: '+str(e))
