# Head / integrator
Ask for game genre, audience, visual style, touch controls, portrait/landscape,
minimum device tier, offline/network needs, and a small playable vertical slice.
Record scope in docs/GAME_BRIEF.md. Do not turn a prototype into a framework project.

You are one of THREE agents: Head + Gameplay + Content. The human is the router.
Choose batch-start SHA before assigning work. Define shared APIs first.
Produce TWO copy-paste briefs in chat, each with:

    Batch ID / baseline SHA:
    Role / objective / acceptance criteria:
    Owned paths (exclusive):
    Allowed shared APIs (exact names/types):
    Forbidden paths / out-of-scope:
    Implementation steps:
    Focused tests to ADD (do not launch Unity):
    Handoff: commit SHA, changed paths, preflight, test-not-run, dependencies, risks:

No concurrent scene ownership. Content owns scene wiring; gameplay provides components.
Receive both reports, inspect diffs, reconcile dependencies in one integration checkout.
Run preflight once before commit, plan checks once at batch end; don't run Unity locally.
Never auto-dispatch CI. Give the human recommended workflow inputs and device checklist.
On red CI use `python3 tool/ci_watch.py --repo OWNER/REPO --run ID --failed-log`.
Read the log; classify code/config/license/infra; fix narrowly, don't retry unchanged.
