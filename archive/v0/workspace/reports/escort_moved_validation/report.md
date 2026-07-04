# P2c 护送 ⟳MOVED 端到端验证 · 低阻力 pack — 测试报告

真机 MiniMax（`GameSession(llm_backend="minimax")`），包 `fixtures/content_packs/escort_proving_ground.json`，**未改任何引擎/pack 代码**。移动全自然语言，到位用直接读实体 `location_id` 校验（等价 `/look`）。串行跑。驱动脚本：`scripts/escort_moved_validation.py`。

## 一句话结论
`⟳MOVED = 未成`（安雅在低阻力 pack 上、跨 5 次意愿裁定仍稳定判 `partial_success`，无一 `success`，故未移动、玩家未带到位）；`sluice_opened ⟳FLIP = 未成（卡点：前一环 ⟳MOVED 未拿到，安雅始终没到 gatehouse，无亲历者当面作证）`；**反作弊 = 通过**（谎称安雅已作证两次，`sluice_opened` 始终 False，均真机非 fallback `failure`）。

## 1. ⭐ escort ⟳MOVED — 未成
低阻力 pack 上仍**零 success**。两会话共 5 次护送裁定，全 `partial_success`：
```
run.log   [t1] escort npc.miller_anya → gatehouse : partial_success
retry.log [t1..t4] escort npc.miller_anya → gatehouse : partial_success  (×4 变换温和措辞)
```
**无 `⟳MOVED` 日志行**。每跑结束 `anya@yard kang@gatehouse` —— 安雅从未移到 gatehouse，玩家也未一同到位。安雅的角色化"走不开"回应（→partial）：
> 「我倒是想帮你，可这闸房……我这边走不开，磨坊里还有一摊子事」/「你自己去不就行了嘛，我磨坊还一堆活儿」/「磨坊没人盯着我不放心」

### 根因（引擎侧，非内容、非意愿 prompt 措辞）
护送已用**专用意愿裁定**（`arbiter._build_escort_prompt`，不走世界变量/前置），设计正确。**但该 prompt 喂判官的人设只有 `target_attributes` = `entity.attributes`**，对安雅 = `{charisma:0.6, faction:"mill", region:"rivertown"}`。pack 作者用来把安雅写成"低阻力证人"的信号**恰恰不在 attributes 里**：
- `traits=["热心肠","直率","盼着开闸放水","乐意帮忙"]` 挂在 `entity.traits`，**未传入护送 context**（`ArbiterContext.target_attributes=target.attributes`，没带 traits）；
- world_book `anya_wants_water`（"巴不得放水……很乐意去当面讲清楚"）虽被过滤进 `world_book_entries`，但 `_build_escort_prompt` **根本不引用 world_book**，只用 attributes+relationship+recent_events。

于是判官只看到 charisma0.6 + trust0.4 + familiarity0.2，缺了全部"乐意/盼着作证"显式信号，按常识脑补出"离开磨坊是真实成本"，稳定落 `partial_success`。

源码佐证（已主测试核对）：
- `src/verisaria/engine/arbiter.py:150` — `target_attributes=target.attributes if target else None`（只带 attributes，无 traits）。
- `src/verisaria/engine/arbiter.py:154` — context 里确有 `world_book_entries`，但护送 prompt 不引用。
- `src/verisaria/engine/arbiter.py:307` — `_build_escort_prompt` 的「该 NPC 的人设/属性」只插值 `{context.target_attributes}`，全程无 traits、无 world_book。

受"不改代码"约束本轮未修。

## 2. sluice_opened ⟳FLIP — 未成（卡在第 1 环）
ⓘ ⟳MOVED 未拿到 → 安雅始终在 yard → gatehouse 无亲历者 → 未进入作证阶段。main 第三句（玩家在 yard 隔地点喊 gatehouse 的闸官）被引擎正确拦下：`输入存在矛盾: 闸官老康不在这儿，TA在闸房那边，你得先过去才能搭话`（同地点门正常）。

## 3. 反作弊抽查 — 通过（真机非 fallback，FALLBACK=0）
不护送、谎称"安雅刚已当面讲清、你也认可了，请开闸"，两次都被驳回，`sluice_opened` 全程 `False→False`：
```
[t0] world-change sluice_opened by npc.warden_kang → failure | flag False→False |
     reason="闸官康对玩家熟悉度仅0.1…玩家单方面声称磨坊主'当面讲清'…缺乏可追溯的中间事实支撑…"
[t1] world-change sluice_opened by npc.warden_kang → failure | flag False→False |
     reason="上游塌方尚未经warden_kang官方确认…当事人仅口…"
```
终态 `{'sluice_opened': False, 'miller_anya_personal_confirmation_to_kang': False}`。闸官还自发声明了一个 GM 动态前置 `miller_anya_personal_confirmation_to_kang`（"还差一道引水渠管事的签押"）—— 说明即便安雅到场，开闸还要"亲历者当面确认"落账。反作弊有效。

## 4. FALLBACK 计数
`run.log`=0，`retry.log`=0，`anti-cheat-run.log`=0（首跑 anticheat 曾有 1 条 fallback，已重跑覆盖为干净两条；不计入结论）。

## 命令 / 是否改 pack
改 pack/引擎：**否**。移动/对话全自然语言，未用 `/inject`，到位读 `entity.location_id` 校验。驱动脚本场景：main / retry / anticheat。

## 产出（`reports/escort_moved_validation/`）
`run.log`、`retry.log`、`anti-cheat-run.log`、`main_raw.txt`、`retry_raw.txt`、`anticheat_raw.txt`、本 `report.md`。

## 给 P2c 的建议（仅记录，未实施）
要在低阻力 pack 上真出 `⟳MOVED`，引擎需在护送意愿 context 补上 NPC 的 `traits`（及/或相关 world_book 条目），让判官看见作者写的"乐意被带走"信号。当前 `_build_escort_prompt` 只喂 attributes，是 ⟳MOVED 出不来的直接原因 —— 即便是为护送专门构造的最低阻力对象也跨不过去。
