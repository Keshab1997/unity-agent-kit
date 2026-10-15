# Unity Agent Kit
### Build in batches. Test with intent. Ship internal only when you say so.

[বাংলায় শুরু করার নির্দেশ](START_HERE_BN.md) · [Validation evidence](VALIDATION.md)

Reusable Android Unity tooling for **one Head + two implementation workers + one Reviewer/QA**.
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
| Head / Gameplay / Content / Reviewer-QA briefs | Human-copy-paste team; exclusive file ownership |
| preflight.py | Syntax/JSON, merge markers, common secrets, generated files, meta/GUID checks |
| kit_update.py | Read-only update check; pinned, conflict-safe apply with explicit workflow approval |
| plan_checks.py | Changed-file risk recommendation; never launches tests |
| doctor.py | Local readiness, no secret values |
| blender_props.py | Optional original procedural crate generator; Blender required, never auto-run |
| ci_gate.py | Missing config/secrets rejected before Unity downloads |
| verify_test_results.py | Reject missing/empty/failed test evidence |
| ci_watch.py | Read one real run / failed job log; no waiting or dispatch |
| agent_loop.py | Head-only explicit-path commit and optional serialized push |
| Secrets Check workflow | Manual ✅/❌ readiness report, local signing probe, opt-in Google OAuth/Play read check |
| Unity Android workflow | Manual preflight, targeted/full tests, tested AAB, opt-in internal upload |
| Minimal project source | Physics smoke tests + opt-in prototype scene creation at build |

## Fast daily loop
0. Optional: discuss with Idea Partner; forward its finalized prompt to Head.
1. Head writes two briefs; you forward them to workers.
2. Workers implement in separate checkouts, add tests and run cheap preflight.
3. Head integrates; Reviewer/QA reviews the candidate diff (read-only unless assigned test files).
4. Head triages findings, pushes main and recommends checks at a useful batch boundary.
   Tiny low-risk tasks may skip a separate QA handoff; record why. No full battery per edit.
5. **You** choose Actions → Unity Android → Run workflow.
6. If red: read log first; one focused fix; same failure twice → STOP and handoff.

```bash
python3 tool/doctor.py
python3 tool/preflight.py
python3 tool/plan_checks.py --base <batch-start-sha>
python3 tool/agent_loop.py --role head --files Assets/MyFeature.cs Assets/MyFeature.cs.meta -m "feat(gameplay): add feature" --push
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

## Existing installations: four-agent instructions
New installs include agents/QA.md automatically. For existing games, review/merge the
updated managed AGENTS block and role instructions, preserving all owner notes. The
installer deliberately refuses changed-file overwrites; use the safe updater for
reviewed toolkit changes (bootstrap instructions are in docs/UPDATING.md).
The optional Idea Partner and full Bengali Head prompt install alongside these roles.
Existing projects must also review/merge agents/IDEA.md and docs/*START_BN.md.
No new workflow, secret or SDK is required for these roles.

## Team names and Bengali communication
Head talks to the owner in Bengali, including questions, plans, worker briefs and reports.
**Agent A = Gameplay; Agent B = Content/UI; Agent C = Reviewer/QA.**
Code, paths, commands and secret names remain exact; role filenames are unchanged.
