You are the agent executing a skill. Read <SKILL_DIR>/SKILL.md in full and follow its
procedure exactly (including any scripts it tells you to run). The user's message to
you is:

「{SCENARIO}」

Produce exactly the reply that the skill instructs you to give for this user message,
in the language the user used. Do NOT actually solve the challenge or do any
downstream skill's work — follow the skill's own stop rules. Your final message must
be only the complete reply text (no meta-commentary, no notes about being a test).

---
使用说明（给跑评测的人，不给执行者）：

1. `<SKILL_DIR>` 用安装位置 `~/.agents/skills/ctf-super-hub`（真实运行时上下文，
   顺带验证安装模式下的发现脚本），仓库内路径仅用于开发调试。
2. `{SCENARIO}` 从 `cases.json` 里取对应 case 的 `scenario` 字段，一字不改。
3. 每个 case 起一个全新的 general-purpose 子代理（盲测：执行者不得读取 cases.json、
   rubric.md 或 fixtures/）。并行不超过 3 个——超过会撞 user concurrency limit。
4. 把执行者的最终回复原样存进 `fixtures/<CASE_ID>.md`，然后跑：

       python3 evals/hub-routing/check_contracts.py

5. 判分脚本只做机械筛选（primary 命中、forbidden 不为主、契约段落存在、停止标记）；
   "停止标记"是 warning 级，最终是否越权执行下游由人对 fixtures 复核。
6. 新增 case：在 cases.json 加条目 → 起盲测代理 → 存 fixture → 判分；预期答案
   只写在 cases.json 的 notes/expect 里，永远不给执行者。
