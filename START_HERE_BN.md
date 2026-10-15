# শুরু করো এখান থেকে

## এই repo game নয়—সব game-এর common kit

নিজের game repo-র root-এ README-র one-command installer চালাবে। নতুন Unity project
না থাকলে `--new-project` ব্যবহার করবে। এই repo-তেই game files ঢোকাবে না।

## চার agent-এর workflow

১. একজন Head, দুজন implementation Worker, একজন Reviewer/QA। তুমি তাদের message copy-paste করবে।
২. Head একই baseline SHA দিয়ে আলাদা file ownership ঠিক করবে।
৩. Gameplay worker controls/physics/camera করবে। Content worker assets/UI/scene wiring করবে।
৪. Worker-রা Head-কে commit ও report দেবে। Head integrate করে QA-কে candidate diff review-এর brief দেবে।
৫. QA findings ও ছোট test/check recommendation দেবে; নিজে runtime/scene files বদলাবে না।
৬. শুধু Head fixes triage/integrate/push করবে। QA একই কাজ বারবার review/test করবে না।
৭. প্রতি ছোট edit-এ Unity test নয়। কাজের batch শেষে তুমি manual CI চালাবে।

Head-কে শুরুতে এই prompt দাও:

> তুমি এই Android game-এর Head agent। AGENTS.md সম্পূর্ণ এবং agents/HEAD.md পড়ো।
> মোট চার agent: তুমি + Gameplay + Content + Reviewer/QA; আমি message router। প্রথমে game brief
> ঠিক করো, তারপর ছোট playable batch-এর জন্য দুই worker-এর আলাদা copy-paste brief দাও।
> দুই worker-এর কাজ integrate হলে exact candidate SHA দিয়ে QA review brief দেবে।
> QA read-only থাকবে, শুধু আলাদা test files explicitly assign করলে লিখতে পারবে।
> Exclusive paths, exact shared API, acceptance criteria, baseline SHA ও handoff format
> থাকবে। Per-edit Unity tests/build নয়; batch ready হলে risk অনুযায়ী manual CI inputs
> দেবে। নিজে CI/upload/release করবে না। কোনো check না চললে passed বলবে না।

## একবার যা setup করতে হবে

- Mac-এ Unity Hub দিয়ে Personal activation; credentials chat-এ নয়, GitHub Secrets-এ।
- Game package ID, version name, Unity version ঠিক করা।
- Existing app হলে তার upload keystore; নতুন key/rotation নিজে থেকে নয়।
- Play service account permission + GitHub secret; internal environment protection।
- বিস্তারিত game-এ install হওয়ার পর `docs/SETUP.md`-তে।

## প্রথম validation

এই kit repo-তে চাইলে manual **Kit Self Check** চালাবে। এটি শুধু Python tooling।
Game repo-তে প্রথমে **Unity Android → preflight**, activation শেষে **full**।
তারপর signing ঠিক হলে **build**, সব প্রস্তুত হলে **internal**।
Internal-এ `UPLOAD INTERNAL` লিখতে হবে। Production option নেই।

প্রথম Unity build/test/upload এখনো চালানো হয়নি। সব bug স্বয়ংক্রিয়ভাবে ধরা সম্ভব নয়।
Phone-এ touch, camera, physics, pause/resume ও performance তোমাকে পরীক্ষা করতে হবে।
