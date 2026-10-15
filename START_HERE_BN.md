# শুরু করো এখান থেকে

## এই repo game নয়—সব game-এর common kit

নিজের game repo-র root-এ README-র one-command installer চালাবে। নতুন Unity project
না থাকলে `--new-project` ব্যবহার করবে। এই repo-তেই game files ঢোকাবে না।

## চার agent-এর workflow

১. Head + Agent A (Gameplay) + Agent B (Content/UI) + Agent C (Reviewer/QA)।
Head সব plan, প্রশ্ন, brief ও report বাংলায় দেবে; তুমি message copy-paste করবে।
২. Head একই baseline SHA দিয়ে আলাদা file ownership ঠিক করবে।
৩. Gameplay worker controls/physics/camera করবে। Content worker assets/UI/scene wiring করবে।
৪. Worker-রা Head-কে commit ও report দেবে। Head integrate করে QA-কে candidate diff review-এর brief দেবে।
৫. QA findings ও ছোট test/check recommendation দেবে; নিজে runtime/scene files বদলাবে না।
৬. শুধু Head fixes triage/integrate/push করবে। QA একই কাজ বারবার review/test করবে না।
৭. প্রতি ছোট edit-এ Unity test নয়। কাজের batch শেষে তুমি manual CI চালাবে।

## আগে idea আলোচনা করতে চাইলে

আলাদা **Game Idea / Design Partner** role যোগ হয়েছে। তার সঙ্গে idea আলোচনা করবে;
সে final copy-paste prompt বানাবে, তুমি সেটা Head-কে দেবে। এটি optional পঞ্চম role;
মূল development team আগের চারজনই। কোনো agent নিজে থেকে চালু বা যোগাযোগ করে না।

- **[Idea agent শুরু করার prompt](template/docs/IDEA_START_BN.md)**
- **[Idea agent-এর সম্পূর্ণ instructions](template/agents/IDEA.md)**
- **[Head-এর সম্পূর্ণ copy-paste prompt](template/docs/HEAD_START_BN.md)**

Idea পরিষ্কার থাকলে সরাসরি Head prompt ব্যবহার করো। নতুন project-এ install করলে
এগুলো `docs/IDEA_START_BN.md`, `agents/IDEA.md` ও `docs/HEAD_START_BN.md` হবে।

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
