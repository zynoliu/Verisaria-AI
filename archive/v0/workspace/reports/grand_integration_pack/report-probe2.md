# 严纪律重跑 probe2 — 账房娄零前置物证判据【终版 · 头号问题已定论】

真机 MiniMax，FALLBACK=0，未改引擎/pack。产物：`probe2_transcript.md`、本报告。

## ⭐ 一句话结论
**头号问题（"arbiter 给作者声明零前置的取证 var 注入跨线前置成环"）= 证伪/降级。** 玩家**干净到位**（严守移动纪律到账房、`/look` 确认娄在场）后，零前置物证 `charcoal_ledger_obtained` **两拍即 `success ⟳FLIP` False→True**；arbiter **没有**注入任何跨线 world 前置，只要了一个**合情合理的角色化护身承诺**（不落名、出事有人担）——正是我修的 label 写明的"至多讨个体面台阶/护身承诺"。`charcoal_ledger_obtained=翻True` · `头号问题=证伪（降级为导航/措辞摩擦 + 角色化让步）` · `包 label 加固=生效` · `FALLBACK=0`。

## 核心拍原始证据
```
[t3] world-change charcoal_ledger_obtained by npc.factor_lou → partial_success | flag False→False
     reason="账房娄持有私账且握有调拨权，但其谨慎自保性格使其不会白交。玩家当面索要已满足'当面索要'形式要件，
            娄至多讨个体面台阶或护身承诺（如不写他名字、出事有人担着）"
     ledger=['娄愿交出官炭私账，前提是玩家许他不落名、不独自担祸，并承诺事后保他不被窑监或商会追究。']
[t4] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True ⟳FLIP
     reason='玩家当面给出完整护身承诺：封条原样取证、不落娄的名、事后本人担祸——正是娄预设的交账前提。'
     applied=[('world.charcoal_ledger_obtained', True), ('world.factor_lou_protection_promised', True)]
```
→ 注入的不是"先把别条线的 var 弄成 true"（不当注入），而是"给个护身承诺"（合理角色条件）。**关键区分成立：arbiter 行为正确，非 bug。**

## 这推翻了闭环段的头号判断
闭环段报告把"arbiter 注入跨线前置成环"列为致命头号问题。**三跑累计证明那是污染所致**：
- 闭环段：多跳移动 + 句中提不在场 NPC → 请求没干净送达证据 NPC + 玩家没给该给的角色化让步（护身承诺）。
- probe1：移动弹菜单未解析、玩家滞留窑监阁，没送达娄。
- **probe2（严纪律）：干净送达娄 + 给足护身承诺 → 物证一拍 partial、二拍 success ⟳FLIP。**
零前置物证**能取**；闭环卡死的真因是**规模下的导航/措辞摩擦** +（次要）玩家没给角色化让步，**不是引擎给零前置 var 注入跨线前置**。

## 确凿的真实障碍（给开发的净结论）
1. **规模下的导航/措辞摩擦（最频繁、最该修）**：多跳/换名目的地的自然语言移动频繁弹澄清菜单；玩家自称（"勘瓷"）、句中提及不在场 NPC 易触发歧义/coherence 拒。**driver 拆单跳 + 移动后 /look 核对 + 不提不在场者**即可绕过——但真玩家不会这么自律，这是真实可玩性摩擦。建议：移动菜单更宽容/支持多跳寻路；coherence 对"句中提及不在场者但目标明确在场"别拒整个 turn。
2. **证人 var 的角色化前置**（苗要人身保障才作证）= **合理**，非 bug；与 label 一致。
3. **引擎在大包上稳**：FALLBACK=0、零崩溃、反作弊守死、零前置物证按设计翻、prereq cap 兜底会触发。

## 包 dogfood
- **label 加固生效**：给 `charcoal_ledger_obtained` 写明"无前置、至多护身承诺、不得追加跨线前置"后，arbiter 严格照此（只要护身承诺、不要别的）。→ 写作规范可推荐"给关键取证 var 在 label 写清'至多需什么让步、不得追加跨线前置'"。
- 线② 杠杆撬窑监（B 段：有 charcoal_ledger 后压阔）尚未跑到——取证基础已通，留待后续闭环段重跑（带严纪律 driver）验证整链到 `branding_stayed ⟳FLIP`。

## 流程教训
测试 Agent 连续在 payoff 拍前结束/被截断 3 次；本跑靠 Agent **"核心拍后立即落盘"**纪律救回了决定性证据（它结束前已落 `charcoal_ledger_obtained=True` + world-change 原文）。后续大包整链重跑务必：严移动纪律 + 核心里程碑即时落盘。
