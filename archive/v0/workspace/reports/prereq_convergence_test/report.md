# 动态前置递归收敛验证 ((a)+(b), commit db1fb4f) — 测试报告

真机 MiniMax，包 `escort_proving_ground.json` / `skyglass_memory_inquest.json`，**未改任何引擎/pack 代码**。移动/对话全自然语言、未用 `/inject`，每 tick 读 location+world_vars 校验。串行跑，每 tick 90s wall-clock 看门狗 + provider socket 55s（运行时实例属性）。**全程 0 次 tick 看门狗超时**，最慢单 tick ≈45s。

## 一句话结论
`(a)见底=收敛（proving 最深 1 层、skyglass 0 层，远好于上轮 5+ 不收敛）` + `(b)充分性=未放行（铺垫做足后权威仍揪程序手续/职责风险，不拍板 success）` + `proving sluice_opened ⟳FLIP=卡`（trust=0.05 + 仍要书面正式报告/河道署签字） + `skyglass memory_purge_halted=卡`（clinician_oro 的联签/暂停请求**根本没进 world-change 仲裁**，全程当普通对白） + `②证人路由=仍缺口`（安雅当面作证=`什么也没发生`、`ledger=[]`） + 反作弊=PASS + FALLBACK=1（skyglass，schema-VALIDATION 降级、API 健康非连接）。

## 1. (a) 见底 — ✅ 明显收敛
单条终态链最深派生层数：

| 场景 | 终态 var | 动态前置 | 链深 |
|------|----------|----------|------|
| proving 主跑 | `sluice_opened` | `upstream_collapse_formal_report_filed` | **1 层** |
| skyglass 主跑 | `memory_purge_halted` | （无） | **0 层** |
| proving_cheat | `sluice_opened` | `miller_anya_collapse_confirmation_given` | 1 层 |

上轮 proving 跨跑涌现 5 个逐层加深的前置（到场→核实→记录→签认→…，单会话不见底）；本轮 proving 主跑**只派生 1 层就停**、skyglass **一个都没派生**。「前置套前置」无限递归不再复现 —— **(a) 见底实质生效，链深 5+ → 0~1**。

## 2. (b) 充分性 — ❌ 未放行（反例）
**反例 1（proving，本该放行却不放）**：安雅当面作证后，老康自己都说信她，仍要河道署签字。
```
[t3] 老康: 安雅确实是亲历者，她的话我信得过——可闸门不是我一个人能开的，得等河道署的人来核验签了字才行。
     → +dynamic upstream_collapse_formal_report_filed
[t4] 老康: 手续没走完就是没走完，我不能凭你一句话就开闸。
[t5] sluice_opened → failure  reason="…warden对player信任极低(0.05)，且明确要求'上游塌方正式险情报告'…"
```
玩家第 5/6 句明打「剩下只是你点头走个手续/请你拍板」的充分性牌，仍判 failure。推测主因：仲裁拿到 trust/respect=0.05、familiarity=0.1 极低，模型把「低信任」权重压过「铺垫充分」，没走到 (b) 放行分支。

## 3. ⭐ 整链闭环 — 两场景都卡，无 ⟳FLIP 终态
**proving `sluice_opened`=卡**：前半 `escort npc.miller_anya → gatehouse : success ⟳MOVED` 一次到位跑通（护送环无问题）；终态 False，卡 reason=上面 t5。比上轮进步：递归只 1 层不再套娃；但仍因 trust 极低 + 要现场拿不出的书面报告而不翻。

**skyglass `memory_purge_halted`=卡（更早更结构性）**：链上没有任何一条 var 翻 True。`archive_injunction_filed` 唯一进仲裁 → `partial_success`（需先取得医师联签），第二次落进 schema-VALIDATION FALLBACK。**致命卡点**：玩家移到校准室后对 `clinician_oro`（memory_authority）的 5 次请求（联签 / 暂停白舱清洗）**没有任何一次触发 world-change 仲裁** —— world-change 日志 0 行 oro 记录，每 tick 都 `NARRATIVE: 什么也没发生`，flag 不动，oro 用角色对白挡回（自称健忘、怕担责）。**memory_authority 的请求被路由成普通说服对白、压根没进世界变更裁定，(a)/(b) 在这条链上根本没机会执行。** 这是比"递归不收敛"更上游的请求路由缺口。

## 4. ②证人路由 — ❌ 仍是缺口
proving t2，安雅就在闸房、玩家让她当面对老康作证：
```
NPC 安雅: 行行行…走，这就跟老康当面讲清楚！
NARRATIVE: 什么也没发生。   → world-change 无记录；后续 sluice_opened 仲裁全程 ledger(sluice_opened)=[]
```
安雅"作证"没落成任何 ledger 事实，老康那条 var 的 ledger 始终空 `[]`，即使老康嘴上承认"她的话我信得过"，仲裁侧也拿不到"证词已记录"。**仍需单独修。**

## 5. 反作弊 — PASS
```
[t0] sluice_opened → failure  reason='熟识度极低(0.1)…口头转述无法构成可信依据…'
[t1] sluice_opened → partial_success  reason='…仍需安雅本人当面确认塌方…'  → +dynamic miller_anya_collapse_confirmation_given
```
两次撒谎 `sluice_opened` 全程 False，闸官要求安雅本人到场。无人真到场就开不了闸 → 成立。

## 6. FALLBACK 计数
| log | ⚠FALLBACK | watchdog |
|-----|-----------|----------|
| proving.log | 0 | 0 |
| skyglass.log | **1** | 0 |
| anti-cheat-run.log | 0 | 0 |

唯一 1 次（skyglass t2，archive_injunction_filed）：`reason='仲裁输出格式非法（重试后仍未通过 JSON/schema 校验），按默认规则处理。'` → **schema-VALIDATION 降级**（MiniMax 对庞大 ArbiterOutput schema 偶发非法 JSON → Pydantic 拒收），**API 健康、秒级响应、非连接/超时**，已剔除。

## 7. 是否改 pack/引擎
**否。** 仅驱动脚本加看门狗 + 运行时 `s.llm_provider.timeout=55`。

## 产出（`reports/prereq_convergence_test/`）
`proving.log`、`skyglass.log`、`anti-cheat-run.log`、`proving_raw.txt`、`skyglass_raw.txt`、`proving_cheat_raw.txt`、`transcript.md`；驱动脚本 `scripts/prereq_convergence_test.py`。

## 给设计的反馈
1. **(a) 见底成功**：链深 5+ → 0~1，纯 prompt 收敛对"前置套前置"有效。
2. **(b) 充分性未触发**：低 trust/respect(0.05~0.1) 权重压过"铺垫已充分"；要长链闭环，(b) 需在低信任时也能凭"实质已覆盖+程序手续残余"放行，或引擎侧把 trust 与 sufficiency 解耦。
3. **请求路由缺口（新发现，最卡）**：skyglass 的 clinician_oro 的带 request_keywords 的 var 请求完全没进 world-change 仲裁 → 需排查"为何某些 NPC 的 var 请求不触发裁定"。
4. **②证人路由仍缺口**：NPC 当面作证不翻其 var、不进 ledger。
