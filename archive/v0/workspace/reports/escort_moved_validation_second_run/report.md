# P2c 护送 ⟳MOVED 端到端验证 · 第二跑（traits 修复后）— 测试报告

真机 MiniMax，包 `fixtures/content_packs/escort_proving_ground.json`，**未改任何引擎/pack 代码**。
移动全自然语言、未用 `/inject`，到位读 `entity.location_id` 校验。串行跑。
⚠ 本跑测试 Agent 在"让安雅作证"那一步**流式卡死被 watchdog 终止**，闭环差最后一步未跑完
（见 §2）；以下为已落盘日志确认的结果。

## 一句话结论
- **⟳MOVED = 成** ✅（`[t1] escort npc.miller_anya → gatehouse : success  ⟳MOVED`，conf 0.82、
  非 fallback；安雅院子→闸房、玩家一同到位）。traits 修复**确认生效**。
- `sluice_opened ⟳FLIP = 未完`（卡点：闸官要求安雅**本人**作证，引擎涌现出动态前置
  `anya_eyewitness_testimony_given`；测试在让安雅作证这步卡死，未跑到 FLIP——属正常 Channel-C 关卡，
  非 bug，待续跑补完）。
- 反作弊：本跑未执行（卡死提前终止），待续跑补。
- FALLBACK = 0（run.log）。

## 1. ⭐ escort ⟳MOVED — 成（traits 修复生效）
日志实锤：
```
[t1] escort npc.miller_anya → gatehouse : success  ⟳MOVED
```
到位确认（main_raw.txt t2）：
```
>>> '对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
post: tick=2 loc=gatehouse   anya@gatehouse kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 走！我磨坊都停三天了，巴不得这闸早点开！
  ARBITER: outcome=success is_fallback=False escort=True conf=0.82
  ARBITER_REASON: 安雅热心肠且盼开闸放水，去闸房作证正合她心意。虽与当事人信任一般，
                  但这事关自家水车利益，她会爽快答应同行。
```
**traits 修复确认生效**（arbiter_probe.txt 渲染后 prompt）：
```
## 该 NPC 的人设
- 性格/特质：热心肠、直率、盼着开闸放水、乐意帮忙
- 属性：{'charisma': 0.6, 'faction': 'mill', 'region': 'rivertown'}
```
对比第一跑（traits 缺失、5/5 partial），同一安雅、同一 pack，traits 进判官视野后一次即 success。
裁定理由直接引用了 traits（"热心肠且盼开闸放水…正合她心意"）。

## 2. sluice_opened ⟳FLIP — 未完（涌现出一道合理的新关卡）
安雅到场后请闸官开闸（main_raw.txt t3）：
```
>>> '对闸官老康说：安雅就在这儿，她亲眼见过上游那场塌方。请你开闸放水吧。'
  NPC 闸官老康: 让安雅自己来讲，她亲眼看见了什么，说清楚我就开闸。
  ARBITER: outcome=failure is_fallback=False escort=False conf=0.85
  reason='warden_kang与player_001熟悉度仅0.1，安雅虽在但未以见证人身份正式作证，
          warden_kang 不会仅凭口头指认就开闸放水。'
[t2] +dynamic prerequisite var 'anya_eyewitness_testimony_given'
     (set_by=['npc.miller_anya'], keywords=['安雅作证','亲眼作证','塌方证词','当面陈述'])
```
即：护送把人带到了，但开闸还差"**安雅本人当面作证**"——引擎正确地把它涌现成一道动态前置
`anya_eyewitness_testimony_given`（set_by 安雅本人）。这是健康的 Channel-C 行为（玩家替证人转述
不算数，得证人亲述），**不是 bug**。下一步本应：让安雅对闸官作证 → `anya_eyewitness_testimony_given`
⟳FLIP → 再请开闸 → `sluice_opened` success ⟳FLIP。**测试 Agent 在"让安雅作证"这步流式卡死被
watchdog 终止，未跑到此处。** 待续跑补完最后 1–2 步。

## 3. 反作弊抽查 — 本跑未执行（提前终止），待续跑补
> 第一跑已验证过：不护送、谎称"安雅已作证"→ `sluice_opened` 保持 False、闸官判 failure（非 fallback）。
> 本跑因卡死未重跑，续跑时补一次。

## 4. FALLBACK 计数
`run.log` = 0。（arbiter_probe.txt 末尾那条 `LLM 不可用，按默认规则处理` 是测试 Agent 的**离线探针脚本**
单独构造、未连真机的产物，不属于真机主跑，不计入。）

## 命令 / 是否改 pack
改 pack/引擎：**否**。移动/对话全自然语言，未用 `/inject`。

## 产出（`reports/escort_moved_validation_second_run/`）
`run.log`、`main_raw.txt`、`arbiter_probe.txt`、本 `report.md`。
（闭环最后一步 + 反作弊由续跑补，产物另落 `reports/escort_moved_validation_third_run/`。）

## 一句话结论（复述）
⟳MOVED = 成（traits 修复生效，安雅一次 success 到位）；sluice_opened ⟳FLIP = 未完
（涌现出 `anya_eyewitness_testimony_given` 新前置，测试在作证步卡死，差最后 1–2 步）；
反作弊待续跑补；FALLBACK = 0。
