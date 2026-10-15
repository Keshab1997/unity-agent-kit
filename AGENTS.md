# Unity Agent Kit — maintainer instructions
Read this file completely before editing. This repository is the reusable toolkit,
not a Unity game. Consumer instructions live in template/AGENTS.md.

- User-authorized public repo; push directly to main. No branches/PRs required.
- Never dispatch CI, wait for CI, upload to Play, or create releases automatically.
- Ask before settings/secrets/workflow changes not already covered by the task.
- Preserve user notes when installing/updating managed agent instructions.
- Batch implementation first. Run `python3 tool/preflight.py` before commit.
- Python/tooling changes: `python3 -m unittest discover -s tests -v` once per batch.
- Workflow changes: validate YAML, pinned action refs and action input names.
- No local Unity/Gradle builds. Unity validation is manual CI, explicitly unverified
  until that run exists. No claim that static checks catch all C# or gameplay bugs.
- Only integrator pushes. Workers use separate checkouts and hand off commits.
- No token, keystore, license, service-account JSON, or credential in git/logs.
- Conventional commits. Confirm local SHA equals remote SHA after push.
