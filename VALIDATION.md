# Implementation evidence — 2026-10-15

- 29 initial focused Python unit tests passed: installer dry-run/idempotency/conflicts,
  owner notes/settings preservation, symlink safety, installed starter preflight,
  syntax/secrets/meta/GUID checks, risk selection, release gates and NUnit evidence.
- After tightening the NotRunnable gate, all 6 result-gate tests passed (including a new NotRunnable case).
- Preflight passed; no Unity invocation.
- Both workflow YAML files parsed; triggers restricted to workflow_dispatch;
  every external action is pinned to a full commit SHA; all configured action inputs
  checked against that exact action.yml via GitHub source.
- Unity Test Framework 1.4.5 exists in Unity's package registry (baseline 2019.4).
- Docker Hub reports unityci/editor:6000.3.3f1-android-3 exists.
- Registry existence is NOT package-resolution, compile, test or Android-build evidence.

Not run: Unity Editor, C# compilation, EditMode/PlayMode, Android build, device QA,
GitHub Actions dispatch, Google Play API calls/upload. No secrets/settings configured,
no signing key generated, no tag/release created, no paid service enabled.

Kit is ready for owner-run validation after installing into an actual game repository
and configuring activation/signing. The generated prototype is a physics demo only.
