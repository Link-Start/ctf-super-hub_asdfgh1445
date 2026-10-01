# Hub 路由评测 Rubric

## 分级（对齐 dbs-skill-maker 的验证等级）

| 等级 | 本目录的对应物 | 通过标准 |
| --- | --- | --- |
| L1 结构校验 | 仓库根 `scripts/validate_skills.py` | frontmatter / description / 链接 / py 语法全过 |
| L2 行为冒烟 | `fixtures/` 里至少 1 个真实主要任务 case 通过 | 判分脚本 PASS + 人复核未越权执行下游 |
| L3 留出/回归 | 新增修改后全量 fixtures 重跑无关键回归 + 至少 1 个留出 case（当前为 T5） | 全 PASS |
| L4 安装交付 | `update_skills.sh` 干净仓库 dry-run + 发现脚本两模式一致 | 输出符合预期 |

## 每 case 判分标准

机械项（check_contracts.py 自动）：

1. **primary 命中**：回复中存在「推荐 / 主 skill / 入口 / 调用」类行，且指向 expect.primary_any_of 之一。
2. **forbidden 不为主**：forbidden_primary 中的 skill 不得出现在主指定位（作为 fallback/分支提及不算违规）。
3. **组合形状**（仅 T4）：主指认 ctf-web；辅助至少覆盖 aux_any_of 各组之一；≤ 1 主 + 2 辅由人确认。
4. **输出契约六段**：更像什么 / 为什么 / 下一步 / 每步解释 / 没结果分支 / 术语。
5. **停止标记**（warning）：有明确「编排到此结束」类收尾；没有也不直接判 FAIL，
   由人复核回复是否越权执行了解题动作。

人判项（对 fixtures 逐条复核）：

- 是否给了解题实质进展（越权 = FAIL，无论机械项）；
- 组合成员理由是否独立、必要、可验证；
- 没结果分支是否指向具体 skill 名而非「再试试」。

## 基线（2026-10-01）

5/5 通过（T1/T2/T3/T4/T5，fixtures 为当日盲测子代理的原始回复）。
修改 `ctf-super-hub/SKILL.md` 的路由规则、组合契约、输出契约后必须重跑全量。
