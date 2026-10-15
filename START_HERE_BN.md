# শুরু করো এখান থেকে

১. Idea আলোচনা চাইলে [প্রথম agent prompt](template/docs/IDEA_START_BN.md) copy করো।
২. Idea clear হলে সে Captain-এর final prompt বানাবে। সরাসরি চাইলে
[Captain starter prompt](template/docs/CAPTAIN_START_BN.md) ব্যবহার করো।
৩. Captain ছোট ৩টি block দেবে: Agent A gameplay, Agent B 3D art, Agent C scene/UI/audio।
৪. তিনজন এক baseline থেকে আলাদা branch/checkout-এ একসঙ্গে কাজ করবে।
৫. নিজের branch push করে সর্বোচ্চ ৫ লাইনে report দেবে; তুমি Captain-কে দেবে।
৬. Captain review/check করে একটার পর একটা main-এ merge করবে। QA agent নেই।
৭. Captain কম কথা বলবে, বাংলায়; প্রতি ছোট task-এ full tests/build নয়।

Branches: work/agent-a/<task>, work/agent-b/<task>, work/agent-c/<task>।
Shared file edit করলে branch থাকলেও conflict হতে পারে—Captain ownership ঠিক করবে।

Kit install/setup: README এবং template/docs/SETUP.md। Secrets game repo-তে,
chat-এ নয়। CI/Play upload এখনো human-manual; কোনো agent auto-dispatch করবে না।
