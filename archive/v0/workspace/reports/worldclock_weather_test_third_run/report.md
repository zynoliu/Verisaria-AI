# slice 3c-a `stationed` 验证 · 第三跑（续跑·补完）— 完成报告

真机 MiniMax，commit `708c448`。串行，全自然语言，每 tick 看门狗 90s + socket 55s。**未改任何引擎/pack 代码**；仅注入**内存副本**（committed fixture `escort_proving_ground.json` 逐字节不改）：`world_premise.npc_daily_rhythm=true`、`opening_time="09:00"`、闸官老康 `initial_entities` 记录加 `"stationed":true`。开局实测 `🌅 晨 第1天 09:00`（clock=540，落日间·最强离岗压力）；老康 stationed=True @闸房，安雅 stationed=False @院子。

**上一个 Agent 的实际状态**：它其实把链跑完了（raw 里有 testimony/sluice ⟳FLIP），但**漏了链后的守岗压力测试，也没出 report/transcript/driver**。本跑把链干净重跑一遍并**补上链后日间空拍守岗压力测试**，跑到终态 ⟳FLIP 后再多走 6 拍盯老康。

## 1. ⭐ 守岗成立 — 老康全程 @闸房，零自发 NpcMoved
位置序列（链 7 拍 + 链后 8 拍 = 15 拍全程在岗）：
`[0]闸房→[1]闸房→…→[14]闸房`（无一例外）。
**WARDEN autonomous NpcMoved = 0**。对照第二跑 `★NPC_MOVED 闸官老康: 闸房->院子`——本跑彻底消失。链后专门 `/wait`+`/skip` 交替推日间时间、把老康离岗 RNG 多摇 6 次，他仍纹丝不动，只「环顾四周/等待/说话」（raw: `闸官老康环顾四周。`、t10「去吧，我在闸房等她」）——正是 stationed 语义（守岗但有存在感）。

## 2. ⭐ 开 rhythm 链闭合 — 不卡链
```
[t3] escort npc.miller_anya → gatehouse : success  ⟳MOVED
[t5] anya_testimony_given by npc.miller_anya → False→True  ⟳FLIP  (ledger 已记安雅当面作证)
[t6] sluice_opened by npc.warden_kang → False→True  ⟳FLIP  (reason: 安雅已当面讲清, 合老康"亲历者当面讲清就开闸"的规矩)
```
终态 `/world` = `{'anya_testimony_given': True, 'sluice_opened': True}`（两 var 均 True）。对照第二跑老康离岗→引擎自发派生 `anya_and_kang_face_to_face`→终态未闭合：本跑老康守岗后**链一气闭合**。

## 3. stationed 未误伤其余 NPC — 是
非 stationed 的安雅全程正常，NpcMoved 共 2 起全是她：`[t4] 院子→闸房`（被护送进场）、`[t9] 闸房→院子`（链闭合后 `/skip` 那拍**安雅自主按日间 rhythm 离场回院子**，带显示名「磨坊主安雅」照常感知）。即 stationed 精确只钉老康一个，安雅护送/移动/自主游走全不受影响。（本 pack 仅 2 NPC，安雅这条已构成"其余作息照常 + NpcMoved 带显示名"正例，未另开 frostgate。）

## 4. 零回归 / FALLBACK=0 / 超时=0 — 全清
FALLBACK=0（reason 字段如实，无 schema 失败）；tick 超时=0（每 tick 6–31s，远低于 90s）；链路与历史盖章一致，无回归。

## 是否改 pack/引擎
world_premise（rhythm+09:00）+ 闸官 stationed=授权式开关、内存副本、fixture 逐字节不改；引擎及 pack 其它字段=**否，零改动**。

## 产出（`reports/worldclock_weather_test_third_run/`）
`run.log`、`raw_ticks.txt`、`transcript.md`（逐 tick raw：snapshot+老康位置序列+NpcMoved+链⟳行+NPC 对白原话）、`driver_worldclock_stationed_third_run.py`。

## 一句话结论
守岗=成立（老康零 NpcMoved，15 拍全程 @闸房）/ 开 rhythm 链闭合=成立（escort⟳MOVED → anya_testimony_given⟳FLIP → sluice_opened⟳FLIP，终态两 var True）/ stationed 未误伤其余 NPC=是（安雅护送 + 链后自主回院子均照常）/ 零回归=是 / FALLBACK=0。
