# Unity Agent Kit
### Build in batches. Test with intent. Ship internal only when you say so.

[বাংলায় শুরু করার নির্দেশ](START_HERE_BN.md) · [Validation evidence](VALIDATION.md)

Reusable Android Unity tooling for **Captain + three parallel implementation workers (Agent A/B/C)**.
An optional **Game Idea / Design Partner** helps refine the concept before development.
Start with [Idea chat](template/docs/IDEA_START_BN.md), then forward its filled
[Head prompt](template/docs/HEAD_START_BN.md). These are role instructions for chats
you open, not background agents.

Python standard-library tools; pinned GitHub Actions; no automatic CI on push.

> **Status:** v1 source/tooling implementation. Unity compilation, package resolution,
> licensing, Android build and Play upload require the first owner-run validation.
> Static checks are not a claim that all C# errors or gameplay bugs are caught.

## One command: an existing Unity game
Run from the game's **repository root** (Python 3.10+ and Git required):

```bash
KIT_DIR=$(mktemp -d) && git clone --quiet https://github.com/Keshab1997/unity-agent-kit.git "$KIT_DIR" && python3 "$KIT_DIR/install.py" --project "$PWD"
```

For a brand-new starter in the current directory:

```bash
KIT_DIR=$(mktemp -d) && git clone --quiet https://github.com/Keshab1997/unity-agent-kit.git "$KIT_DIR" && python3 "$KIT_DIR/install.py" --project "$PWD" --new-project
```

These commands install current main for convenience. For reproducible/safer use,
review this source, select a known commit SHA, and add
`git -C "$KIT_DIR" checkout --detach <reviewed-sha>` BEFORE invoking install.py.
The installer records source revision in unity-kit.lock.json. No curl-pipe-shell.
Use `--dry-run` to preview. `--unity-version EXACT_VERSION` selects a starter Editor.
Default 6000.3.3f1 is a known baseline, not an assertion of latest patch/image support.

**Installer safety:** no Unity download, CI dispatch, git commit/push, secret setup or
Play upload. Refuses conflicting files and symlink paths before writing; merges
.gitignore, preserves existing AGENTS owner notes and project identity. Installs only
repo-root projects in v1. Existing projects keep settings/packages; kit includes
Editor build helper plus smoke tests. Review imports/dependencies before Unity run.
For existing installs use the [safe updater](template/docs/UPDATING.md): check first,
apply a reviewed exact commit, refuse conflicts. No forced overwrite.

## What's included
| Component | Job |
|---|---|
| Idea Partner + Head starter prompts | Discuss concept, then copy a self-contained brief to Head |
| Captain / Agent A / Agent B / Agent C briefs | Human-copy-paste team; exclusive file ownership |
| preflight.py | Syntax/JSON, merge markers, common secrets, generated files, meta/GUID checks |
| kit_update.py | Read-only update check; pinned, conflict-safe apply with explicit workflow approval |
| plan_checks.py | Changed-file risk recommendation; never launches tests |
| doctor.py | Local readiness, no secret values |
| blender_props.py | Optional original procedural crate generator; Blender required, never auto-run |
| ci_gate.py | Missing config/secrets rejected before Unity downloads |
| verify_test_results.py | Reject missing/empty/failed test evidence |
| ci_watch.py | Read one real run / failed job log; no waiting or dispatch |
| agent_loop.py | Role-checked branch commits/push; workers cannot use main |
| Secrets Check workflow | Manual ✅/❌ readiness report, local signing probe, opt-in Google OAuth/Play read check |
| Unity Android workflow | Manual preflight, targeted/full tests, tested AAB, opt-in internal upload |
| Minimal project source | Physics smoke tests + opt-in prototype scene creation at build |

## Fast daily loop
0. Optional Idea Partner returns a filled Captain prompt.
1. Captain gives THREE short Bengali copy-paste blocks (8–10 lines each), one small
   deliverable per Agent A/B/C, with one baseline and exclusive paths/shared APIs.
2. A (gameplay), B (3D art), C (scene/UI/audio) work concurrently in separate checkouts.
3. Workers push only work/agent-a/<task>, work/agent-b/<task>, work/agent-c/<task>.
4. Owner returns branch/SHA reports; Captain fetches, reviews, checks and merges main.
5. No separate QA agent. Captain performs review/testing; risk-based Unity checks at
   useful batch boundaries, human-dispatched CI only. Branches can still conflict.
6. No force-push, automatic conflict resolution, PR/tag/release or branch deletion.

```bash
python3 tool/doctor.py
python3 tool/preflight.py
python3 tool/plan_checks.py --base <batch-start-sha>
python3 tool/agent_loop.py --role captain --files Assets/MyFeature.cs Assets/MyFeature.cs.meta -m "feat(gameplay): add feature" --push
```

The above `tool/` commands apply AFTER installing into a game. This kit repo's
maintainer check is `python3 tool/preflight.py`; its focused tests are
`python3 -m unittest discover -s tests -v`.

## Set up once per game
Read **[setup guide](template/docs/SETUP.md)** for Mac Unity activation, signing,
Play API permissions, environment protection, current target SDK checks and first run.
No credentials belong in chat or git. You configure secrets in GitHub UI yourself.
Play Console account is required; no paid service or asset dependency is introduced.
Free CI depends on standard public-repo runners and applicable storage/LFS quotas;
Unity Personal depends on eligibility and activation. Zero-cost cannot be guaranteed.

## Deliberately outside v1
No production publishing, tags/releases, autonomous agent messaging, multiplayer
backend, paid AI generation, complete character controller, Blender installation,
visual/device certification, or automatic Unity upgrades. Add these only when the
actual game needs them and the owner approves.

MIT licensed. See [agent contract](AGENTS.md) and [consumer rules](template/AGENTS.md).

## Current team and older installations
**Captain** (formerly Head) talks briefly in Bengali. **Agent A = gameplay/physics/camera;
Agent B = 3D art/materials/animation; Agent C = scene/level/UI/audio.** There is no
separate QA agent. Workers branch/push; only Captain reviews/merges/pushes main.
Role policy is coordination, not GitHub branch-protection enforcement.
Read [Captain prompt](template/docs/CAPTAIN_START_BN.md). Legacy HEAD.md points to
CAPTAIN.md; QA.md is retired. Existing games use the safe updater/manual merge;
no forced overwrite. Shared files/folder meta still need exclusive ownership.
