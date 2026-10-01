# 导出的 Skill 索引

## 编排契约（所有 skill 共同遵守）

- **唯一编排中心**：`ctf-super-hub`。它用 `scripts/list-installed-skills.py` 动态发现已安装 skill（离线兜底：`ctf-super-hub/references/routing-table.md`），先判断单 skill 能否覆盖，需要时最多编排 1 主 + 2 辅（角色：前置筛选 / 证据补充 / 验收约束）。
- **交接规则**：下游 skill 任务未完成不讨论下一站；完成后输出结论即结束，仅当用户明确询问下一步才提示回到编排中心；不预设默认长链。
- **质量校验**：改完 skill 跑 `python3 scripts/validate_skills.py`（L1 结构校验：frontmatter、description、相对链接、仓库文件）。行为级验证需实际做题冒烟。
- **版本与更新**：`ctf-super-hub` 进入时自动跑 `scripts/check-update.sh`（读 GitHub 上的 `UPDATE.json`，24h 缓存，失败静默）；有新版本时按提醒回复 1，由 `scripts/update_skills.sh` 执行 `git pull` + 重新同步（工作区有未提交修改时拒绝更新）。

| 目录 | 用途 |
|---|---|
| `ctf-super-hub` | 超级总控入口：自动分流 / 先头脑风暴 / 手动指定 / 教学模式 / 比赛模式 / hints-only |
| `ctf-beginner-hub` | 新手总入口：自动分流 / 先头脑风暴再分流 |
| `solve-challenge` | CTF 首轮分类与路由 |
| `brainstorming` | 先澄清题意、材料、目标、卡点 |
| `ctf-web` | Web 漏洞题 |
| `ctf-crypto` | 密码学题 |
| `ctf-reverse` | 逆向工程题 |
| `ctf-pwn` | 二进制漏洞利用题 |
| `ctf-forensics` | 取证/隐写/流量/内存题 |
| `ctf-osint` | 开源情报题 |
| `ctf-malware` | 恶意软件分析题 |
| `ctf-misc` | 杂项、jail、编码、RF 等 |
| `ctf-ai-ml` | AI/ML 相关 CTF 题 |
| `ctf-writeup` | 赛后 writeup |
| `strix-beginner-hub` | Strix 增强入口：在原有 CTF 双模式里辅助判断该先用工具还是漏洞专项 |
| `strix-quick` `strix-standard` | Strix 增强模式：在 Web/接口题里补高价值快扫与平衡覆盖 |
| `strix-httpx` `strix-katana` `strix-ffuf` `strix-nuclei` `strix-sqlmap` | Strix 增强工具链：探测、爬取、模糊测试、模板扫描、SQL 自动验证 |
| `strix-sql-injection` `strix-xss` `strix-ssrf` `strix-rce` 等 | Strix 增强漏洞专项：在 Web/接口题里补足更强的验证能力 |
