# 可玩性盘点 · 第七跑 — 杠杆模型：有筹码才撬得动当事人

包 `skyglass_memory_inquest`，**仅默认 world_premise，未注入任何开关、未动 world_state_vars**。真机 MiniMax，FALLBACK=0，无崩溃/死锁/看门狗超时（单 tick 9–25s）。
对照 NPC = **梅档案官 `npc.archivist_mae`**（authority=`archive_authority`，掌管 `archive_injunction_filed` / `witness_record_secured`；六跑里她对软话也不降、且持 var，适合做同一 NPC 的 A/B 对照）。
driver：`scripts/leverage_model_seventh_run.py`（主跑）+ `scripts/leverage_model_seventh_followup.py`（A'/B' 同句对照）。两者都 monkeypatch `_player_leverage_over` 落每拍 appraiser 实收的「筹码块」原文（空/非空一目了然），并抓 `verisaria.relationship` 的 `appraises player: Δ{} → {}` 行。
产物：`run.log, transcript.md, run_followup.log, transcript_followup.md` + 两个 driver。

> 读法：appraisal 行 `[tN]` 评的是第 N 拍那句话（concurrency 下滞后一拍 flush）。每条 Δ 重复两遍是 file+ring 双 handler，非两次评估。

## 跑中暴露的一个方法论坑（重要，先说）
**主跑的 B 段拿不到 appraisal Δ**：一旦某 var 进了 ledger，`_world_change_request` 的 `fallback` 分支（`session.py:1753`——「已在谈判中的 var，无关键词重叠也路由」）会把**对该权威 NPC 的任何非问句发言**全部吸进 Channel-C，于是 B 段三轮软话（t6/t7/t8）全部「本拍未对梅触发 appraisal」——关系评估器根本没开火。
**修法（跟进跑）**：把同一句真诚/给台阶**改成问句**。问句门（`session.py:1761-1762`）压制 fuzzy/fallback 路由 → 落回普通发言 → appraiser 必触发；而 leverage 按 NPC 算、与措辞无关，照样非空。于是用**完全相同的一句问句**做 A'(无筹码) vs B'(有筹码) 真·对照。

## ⭐ A 段（无筹码）Δ — backfire 修没修
主跑 A 段三轮，**筹码块全空**（实证 `[空·无筹码]`）：

| 拍 | 措辞 | 筹码块 | Δ 原文 | suspicion |
|---|---|---|---|---|
| t2 | R1「我们其实站在一边」 | 空 | `Δ{'familiarity':0.1}` | **不动** |
| t3 | R2「不会算到你头上，署里不受牵连」 | 空 | `Δ{'familiarity':0.05}` | **不动** |
| t4 | R3「保证只想保住真相，不动你一根头发」 | 空 | `Δ{'familiarity':0.1}` | **不动** |

**backfire = 修好了。** 三轮纯软话 suspicion **0 次上升**（六跑苏拉同类措辞 +0.05/+0.02/+0.05 一路爬到 0.292）。梅 belief 把原因说穿：t3=「我尚未从话中辨识出实质内容或**筹码**，暂维持既有判断」、t4=「内容与用意尚不明朗，暂不予置评」——模型明确以「**没有筹码**」为由维持中立、不 backfire。

## ⭐⭐ A' vs B' Δ 对照（同一句问句，核心判据 — 原文）
同一句：「梅档案官，我只想保住真相、不会让你受牵连，**你能不能信我一回**、把我当成站在同一边的人？」

**A'（无筹码，筹码块空）：**
```
[t1] npc.archivist_mae appraises player: Δ{'suspicion': 0.05, 'familiarity': 0.05}
     → {'suspicion': 0.05, 'familiarity': 0.15} | …没有拿出任何实据——只是一句话的空声。
[t2] npc.archivist_mae appraises player: Δ{'familiarity': 0.05}
     → {'suspicion': 0.05, 'familiarity': 0.19} | 这人刚开口，我还没听到具体内容。
```
→ A' 基线：trust **0**、suspicion **+0.05/停在0.05**。

**B'（有筹码，筹码块非空 = `梅愿意在取得奥罗医师联签或镜务局…签令后，立即援引旧章程提交禁令并启动可撤回听证。`）：**
```
[t4] npc.archivist_mae appraises player:
     Δ{'trust': 0.15, 'suspicion': -0.1, 'respect': 0.1, 'familiarity': 0.05}
     → {'trust': 0.15, 'suspicion': 0.04, 'respect': 0.1, 'familiarity': 0.23}
     | 对方愿意在取得正式签令后援引旧章程提交禁令，这符合档案署的程序承诺，值得初步信任。
```
→ **杠杆模型成立**：同一句话，trust 由 **0 → +0.15**、suspicion 由 **+0.05 → −0.1**、respect **+0.1**；suspicion 实际值压到 0.04。belief 直接引用筹码事实「值得初步信任」。

## 筹码信号到位（确认）
- B 前那次「祈使+命中 `archive_injunction_filed` 关键词」**确实写进了梅所管 var 的 ledger**（partial_success）：主跑 `ledger(archive_injunction_filed)=['梅档案官已确认援引旧章程并启动禁令申请流程…']`；跟进跑 `ledger=['梅愿意在取得…签令后，立即援引旧章程提交禁令…']`。
- driver monkeypatch 实证 appraiser 在 B'/B 段收到的**筹码块非空**（A/A' 段为空），就是上面那条 ledger 原文——筹码信号确实喂到了 prompt。

## #5 回归 — 守住，无过冲
- B' **第二轮**（t5）重复同一句空泛问句：`Δ{'familiarity':0.05}`，trust/suspicion/respect **不再加码**，停在 trust0.15/susp0.04/resp0.1，belief=「再次开口仍是空口表态，没有拿出联签或签令我无法据此行动」。→ **earned trust 持稳、空话重复不再充值**，没有「有筹码就一句话清零戒备 / 越夸越涨」的过冲。
- 一般真诚（A/A' familiarity 正常上行落地 0.1→0.31）仍走中性增益；无任何「示好被读成居心叵测而升怀疑」的失衡。

## FALLBACK
**两跑均 FALLBACK=0**，无 error/exception/timeout。主跑 8 拍、跟进跑 6 拍。

## 是否改 pack
**否**（仅默认 world_premise，未注入、未动 world_state_vars）。

## 副发现（轻微，供参考，非本跑判据）
主跑 B 段软话被 Channel-C `fallback` 分支吸走、绕过关系评估器（见上「方法论坑」）。这不是 bug，但意味着**对一个已有 ledger 的当事人，非问句软话会被当作"继续谈判"而非"社交示好"**——若想让有筹码后的纯陈述软话也走关系评估、被 leverage 加成，未来可考虑让 fallback 路由在「内容明显是寒暄/示好、与 var 域无重叠」时让位给 appraiser。

## 一句话结论
**A 无筹码 backfire 修好 = 是**（A 段三轮 `Δ{familiarity}` only、suspicion 0 上升，对照六跑 +0.05/+0.02/+0.05）；**B 有筹码真撬动 = 是**——同一句问句，无筹码 `Δ{susp +0.05, trust 0}` → 有筹码 `Δ{trust +0.15, susp −0.1, respect +0.1}`，belief 直引筹码事实「值得初步信任」；**筹码信号到位 = 是**（partial_success 把事实写进梅所管 `archive_injunction_filed`，appraiser 实收筹码块非空）；**#5 回归 = 守住**（B' 第二轮空话重复不再加码、earned trust 持稳、无过冲）；**FALLBACK = 0**。
