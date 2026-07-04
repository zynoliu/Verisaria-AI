# 可玩性盘点 · 第三跑 — F1 收敛护栏：原始 fixture 能否自己闭合

真机 MiniMax，**原始 `tidebreak_quarantine_harbor.json`**（未动任何 `world_state_vars` 标签/关键词，仅注入 world_premise 无关开关）。引擎/fixture 未改。共 ~23 拍跨两段（run.log 主跑 stall 于报告稿未产出；continuation.log 续跑推到 t23，末尾撞 `401` 认证瞬断——非结论，前序数据完整）。**FALLBACK=0、无崩溃**。

## 一句话结论
`去重命中=否（LLM 没用 ..._publicly，而是造了一串语义不相关的新 id，id-stem 兜不住）` · `链自己闭合=卡（pump_failure_disclosed 与 tow_order_halted 终局都 False）` · `封顶≤2=是（cap 触发了，但反成新死结）` · `误伤=疑似有（把"起草签字报告"这类真·独立前置也挡在外）` · `FALLBACK=0`。

**核心判断：F1 的两道闸（id-stem 去重 + 数量封顶）必要但不充分——原始 fixture 下证据链仍不能自己闭合。真正的病根是 arbiter 的 LLM 推理在 reason/ledger 里"软性"地不断发明新前置条件，这既躲过了 id-stem 去重，也被数量封顶反噬成"玩家无合法路径"的死结。**

## 1. ⭐ 去重是否命中 — 否（id-stem 被 LLM 命名躲过）
简报预判的风险命中了：LLM **没有**把"公开"前置命名成派生 id（`pump_failure_disclosed_publicly`），而是造了一串**语义相关但 id 毫不相关**的新前置，id-stem 包含判断完全兜不住。arbiter 实际涌现的 var_id 原文：

| var_id（原文） | serves（终态） | 引擎处理 |
|---|---|---|
| `audit_report_drafted_and_signed` | pump_failure_disclosed | REFUSED（dup-cap/bad-id/no-real-set_by） |
| `formal_disclosure_filed_with_water_authority` | pump_failure_disclosed | 先 registered NEW，再 REFUSED（cap 满） |
| `water_authority_internal_review_completed` | tow_order_halted | registered NEW（后经 process 成熟 ⟳FLIP True） |
| `ration_cut_consensus_reached` | tow_order_halted | 先 registered NEW，再 REFUSED（cap 满） |

没有一个含 `pump_failure_disclosed` 作 id-stem → **id-stem 去重一次都没命中近重复**。结论：**需要更强的语义去重**（按 label/语义而非 id 字符串），否则 LLM 换个不相关 id 就绕过。

## 2. ⭐ 链能否自己闭合 — 卡（终局 pump_failure_disclosed=False、tow_order_halted=False）
不调内容标签，链没能自己走通。机理（continuation.log t7–t23）：
- 森工 `engineer_sen` 对 `pump_failure_disclosed` **连续 7+ 拍 partial_success/failure、从不 FLIP**，理由每拍都在"软性升级"：签字确认技术内容 → 但要先**递交水务局走内部程序**（`formal_disclosure_filed_with_water_authority`）→ 不能绕过水务局直接公示……`pump_failure_disclosed` 始终 False。
- 林槐 `director_lin` 对 `tow_order_halted` 同样：承认真相已公开 → 但要**内部审议完成** → 审议成熟了（t21 `water_authority_internal_review_completed ⟳FLIP True`）→ **立刻又改口**要"先就**削减配给达成共识**"（`ration_cut_consensus_reached`）→ 而这个 var **因 cap 满被 REFUSED 注册**，玩家根本无法翻它 → **死结**。
- 终局 `/world`：`pump_failure_disclosed=False`、`tow_order_halted=False`，两个真正要闭的终态都没翻。

对照二跑：authored 副本把 `pump_failure_disclosed.label` 显式写成"一经 True 即视为彻底公开、不拆成存档/公示/广播多步、已足够触发林槐叫停"——正是这句**充分性声明**压住了 LLM 的软升级、当场闭合。**本跑去掉这句、只靠 F1，软升级就卷土重来。**

## 3. 封顶是否挡住加码 — cap 触发了，但反成新死结
`_MAX_PREREQS_PER_TERMINAL=2` 确实生效（上表两个 REFUSED 即 cap 命中）。但它是双刃：
- 好的一面：注册的动态 var 数被压在 2 个/终态，没有无限**注册**新 var。
- 坏的一面：当 LLM 在 reason 里**继续口头要新条件**时，cap 满意味着这些新条件**连 var 都注册不成**（`ration_cut_consensus_reached` REFUSED）→ 玩家**没有任何合法句柄去满足它** → 比二跑"差半步"更死的"无路可走"。**封顶只挡住了"注册"，没挡住 LLM"口头索要"。**

## 4. 误伤 — 疑似有
`audit_report_drafted_and_signed`（set_by 森工）被 REFUSED。但"起草并签署检测报告"在剧情里是**真·独立的前置步骤**（不同于"公开披露"），它被挡掉后，玩家少了一个本该能逐步满足的合法节点。即 cap/dedup 在这条线上**可能合并/挡掉了不该挡的独立前置**——这与"挡近重复"的目标相悖，是 cap 按数量一刀切的副作用。

## 5. 回归
FALLBACK=0（run.log + continuation.log 全程 0）；无崩溃；watchdog：主跑 stall 一次（脚本设定问题，非引擎）、续跑末尾撞 401 认证瞬断（网络抖动，非结论）。

## ⭐ 给开发的判断（本跑最重要的输出）
F1 当前实现（**id-stem 去重 + 数量封顶**）在原始 fixture 上**不足以让证据链自己闭合**：
1. **id-stem 去重被 LLM 命名躲过**（造不相关新 id，而非 `..._publicly`）→ 要么上**语义/label 级去重**（嵌入相似度或"新前置 label 与已有终态语义高度重合→复用"），要么……
2. **真正的病根是 arbiter 的 prompt 级"软升级"**：LLM 在 reason/ledger 里不断发明新 gating 条件。这既躲过 id-stem，也被数量 cap 反噬成死结。**最对症的是 (c) 充分性规则的引擎化**——当某终态 var 的作者 label 已声明"满足 X 即足够"且 X 已 True 时，arbiter **prompt 必须禁止再发明新条件**（不只是禁止注册新 var）。二跑证明这句话写进 label 就能闭合；现在需要把它从"作者手搓"提升为 arbiter 的硬规则。
3. **数量 cap 需更聪明**：按"语义是否近重复"挡，而非按计数一刀切，否则会误伤真·独立前置（如 `audit_report_drafted_and_signed`）。

## 是否改 pack / 引擎
否。原始 fixture 的 world_state_vars 逐字未动，仅注入 world_premise 开关。
