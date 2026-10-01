# 叶子 SKILL.md 轻量化审计（2026-10-01）

dbskill 的「主入口保持轻」原则：SKILL.md 只放**共同决策、关键流程、停止条件**；
条件性细节进 `references/`，重复且确定的工作进 `scripts/`。本审计检查三个超过
300 行的叶子 skill 哪里偏离了这个原则。**本文件只给结论和建议，未动正文。**

## 判断基准：什么该留在 SKILL.md

- 模式判断 / 转向规则（When to Pivot）——决策内容，必留；
- 资源索引（Additional Resources）——路由到 references/ 的入口，必留；
- Prerequisites、Quick Start——高频执行内容，必留；
- 「一行技速查 + See X.md」的大面积罗列——条件性细节，应下沉。

## ctf-misc（496 行 → 建议 ~180 行，优先级最高）

**该下沉的（约 320 行）：**

1. **Linux 提权集群（L279–347，约 70 行）**——SUID / Docker group / Sudo 通配符 /
   Monit / PostgreSQL / Backup cronjob / PaperCut。这块一是内容已在
   `linux-privesc.md` 里有完整版，二是**偏离本 skill 使命**（misc 的核心是
   jail/编码/RF/杂题，不是主机提权）。整块下沉，留一行指针；提权题如果常见，
   考虑在 When to Pivot 加一条指向说明。
2. **Technique Quick References 子弹列表（L232–258，约 27 行）**——全部是
   「一行 + See X.md」指针，改成资源索引格式并入 Additional Resources，或独立
   `technique-index.md`。
3. **CTFd 导航（L351–361）**——`ctfd-navigation.md` 已有全文，留 2 行指针。
4. **编码/隐写散段（Common Encodings、IEEE-754、Unicode 隐写两段代码、UTF-16、
   Keyboard/Pigpen/ASCII-CSV/Backdoor、HISTFILE、Levenshtein、SECCOMP、rvim，
   合计约 110 行）**——下沉到 `encodings.md` / `encodings-advanced.md` /
   `games-and-vms-3.md` / `bashjails.md`。
   **注意**：Unicode Tags（UTCTF 2026）、Variation Selectors（Nullcon 2026）、
   3D 打印喷嘴跟踪（LACTF 2026）这几段是**只在 SKILL.md 里有细节的新增内容**——
   下沉是「搬移」不是「删除」，要先确认目标 reference 文件里有没有，没有就连细节
   一起搬过去。

## ctf-forensics（378 行 → 建议 ~190 行，优先级次之）

**该下沉的（约 180 行）：**

1. **Additional Technique Quick References（L272–346，约 75 行）**——37 条
   「一行 + See X.md」平铺指针表，是最大的单块。改成按 reference 文件分组的索引
   （每文件一行摘要），或者全部并进各 reference 文件的头部摘要区。
2. **Windows 细节段（Event ID 表、When Logs Are Cleared、WMI、密码 hash 提取，
   L100–134 与 L202–248，约 70 行）**——`windows.md` 已有全文；SKILL.md 保留
   Key Event IDs 的 6 行速查表即可（高频）。
3. **Steganography 块（L136–162，约 28 行）**——`steganography.md` 三兄弟已有
   全部细节；保留命令行速查（steghide/zsteg/stegsolve 4 行），子弹清单下沉。
4. **Network Quick Reference（L250–263）**——下沉到 `network.md` /
   `network-advanced.md`。

**必留的高价值小节**：Uncommon File Magic Bytes 表、Common Flag Locations、
Quick Start Commands——这些是 triage 阶段每题都用的高频内容。

## ctf-crypto（318 行 → 建议 ~230 行，优先级最低）

结构比前两个好：章节与 reference 文件一一对应（Classic/Modern/RSA/ECC/Lattice/
ZKP/PRNG），本质是「带一行攻击摘要的主题索引」，triage 价值真实存在。问题集中在
**尾部散段（L236–311，约 75 行）**：Modern Cipher Attacks (Additional)、
Introspective CRC、CBC Padding Oracle、Bleichenbacher、Birthday/MITM、CRC32 伪造、
Blum-Goldwasser、Hash Length Extension、Compression Oracle、RC4 bias、RSA 同态、
C srand/rand、V8 XorShift、MT float、Chaotic PRNG、SPN——都是后补的单段，与
`modern-ciphers-2/3.md`、`prng.md` 重复。建议合并回对应主题章节（去掉重复子弹），
**不**建议照搬前两个的激进下沉。

## 执行建议（如果要做）

1. **一次只动一个 skill**，misc 先行；每动一个跑一次该 skill 的 L2 行为冒烟
   （evals/ 目前只覆盖 hub 路由——给叶子补冒烟 case 是前置工作，见下）。
2. 下沉 = **搬移**。先 grep 目标 reference 文件确认细节是否已存在，只在缺失时
   连细节一起搬；绝不直接删「只在 SKILL.md 里有」的内容。
3. 动完跑 `python3 scripts/validate_skills.py`（链接检查会抓住搬移漏项）。
4. 前置工作：`evals/` 目前只有 hub 路由 case。下沉会改变叶子 skill 的内容分布，
   动手前应先给 misc/forensics 各加 1-2 个行为冒烟 case（给场景 → 检查 skill
   仍能指向正确 technique），否则回归无从判断。

## 其他叶子（行数健康的）

pwn 210 / osint 192 / reverse 182 / malware 179 / writeup 139 / web 152 /
ai-ml 117——无需处理。beginner-hub 已薄壳化（见其 SKILL.md）。
