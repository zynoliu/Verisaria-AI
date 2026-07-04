# 活世界子系统验证 — 完成报告

真机 MiniMax 实连，每 tick 90s 看门狗 + provider 55s socket。**未改任何引擎/其它 pack 内容**（`git diff HEAD -- src/ fixtures/` 为空）。唯一对 pack 的改动是按任务授权在 `world_premise` 加 `npc_daily_rhythm`/`opening_time`/`climate` 三个声明式开关——且注入**内存副本**，committed fixture 逐字节未改。全程自然语言，未用 `/inject`。**FALLBACK=0、tick 超时=0**。snapshot 字段名经核实即 `time_of_day`/`clock`/`weather`。

## 一句话结论
`回归(flag off)=零回归（escort ⟳MOVED → anya_testimony_given ⟳FLIP → sluice_opened ⟳FLIP，与上次盖章逐项一致）` · `flag on 被点名NPC不乱走=成立（in_conversation 优先，连续6拍0移动）` · `作息可信度=中上（白天散/夜里归方向对、NpcMoved带显示名感知好；暮夜采样稀、在家比例数字有噪声）` · `时钟变速=自然（对话/等待/移动+3min、空地/skip单步+30min、一次/skip≈+360min）` · `天气=合理可重放（阶梯内±1慢漂、无突变、温带无雪/寒带无雷雨；存档clock+weather一致、同pack同时刻可重放）` · `slice 3b=建议做（沉浸缺口明显）` · `FALLBACK=0`。

> ⚠ flag on 真实副作用（非违规）：完整 2b 跑里闸官老康作为**旁观NPC**（在家、晨相→离家乘子×2.5）自己游走到院子，引擎自发派生 `anya_and_kang_face_to_face`，链未闭合。这是"旁观NPC按作息动"的预期表现、**仅 flag on 出现**（flag off 同种子老康不动），不是"被点名NPC乱走"。

## 1. 作息观感
frostgate（寒带/清晨/rhythm ON），从第1天07:00推到第2天12:00。home 由 loader 默认锚到出生地。

| NPC | home | 晨在家% | 昼在家% | 暮 | 夜 | 位置变化 |
|---|---|---|---|---|---|---|
| 队长布兰 | 门楼 | 9/18(50%) | 10/15(66%) | 1/1 | 1/1 | 5 |
| 哨兵伏斯 | 门楼 | 15/18(83%) | 14/15(93%) | 1/1 | 1/1 | 4 |
| 军需官海尔 | 兵营 | 17/18(94%) | 12/15(80%) | 0/1 | 0/1 | 2 |
| 难民卡泽 | 难民营 | 16/18(88%) | 13/15(86%) | 1/1 | 1/1 | 4 |

方向可信但偏温和。白天确实离家散开（布兰最活跃），暮/夜多数在家——但**暮/夜每相只采到1样本**（推时间靠空地/skip单跳6h越过了暮夜，没"驻足整夜"），夜里在家比例统计意义弱，只能说方向对、给不出可信硬比例；海尔暮夜0%是单样本噪声。节律方向对但**戏剧性偏弱**（一天2–5次碎动，不像集体出门/归巢的强节拍）。

## 2. 自主进出场
成立且观感好。NpcMoved 稳定带**显示名**（非raw id），场景1共20例，如 `难民卡泽: 难民营->门楼`、`哨兵伏斯: 门楼->兵营`、`队长布兰: 门楼->难民营`；emergent NPC「老西布」也带名进出。护送链 `磨坊主安雅: 院子->闸房` 即 escort⟳MOVED 的可感知投影。

## 3. ⭐ 回归（最关键）
**3a flag OFF = 零回归**，链完整闭合，与第四跑盖章逐项一致：
```
[t3] escort npc.miller_anya → gatehouse : success ⟳MOVED
[t4] anya_testimony_given by npc.miller_anya → success | flag False→True ⟳FLIP | ledger=[]
[t5] sluice_opened by npc.warden_kang → success | flag False→True ⟳FLIP | reason='…条件已满足，无额外前置。' ledger=[]
RESULT: anya_testimony_given=True sluice_opened=True  （dynamic_vars 全程空）
```
证人本人翻testimony、闸官据自己人设/(c)直接开闸、无派生动态前置、voiced/verdict一致。**默认关对动态世界模型零回归**确认。

**3b flag ON**：链未闭合（两var均False）。根因：`[t2] ★NPC_MOVED 闸官老康: 闸房->院子`——老康在家+晨相×2.5离家乘子放大其base move_chance，作为旁观NPC（玩家当时在对**安雅**说话）溜达走了，二人异处 → 引擎派生 `anya_and_kang_face_to_face` 卡链。flag off 同种子老康不动。这正是设计预警的"常开扰动护送pack"。
**但被点名/对话中NPC不乱走 = 成立**（独立附测 `named_npc_test.txt`）：flag ON 晨相连续6拍持续对老康说话，`warden@gatehouse 全程 moved=False`，TOTAL=0。机制对得上 `_generate_for_npc` 的 in_conversation 分支直接走speech、永不movement。结论：被点名不乱走成立；但"旁观即闲置的关键NPC会按作息走开"在窄拓扑下确能拖累链——这是flag on才有的真实副作用，也解释slice3a为何默认关。

## 4. 时钟变速
```
对话SLOW: +3min  | WAIT: +3min | 移动: +3min | /skip空地单步: +30min | /skip一次(满12tick): +360min(≈6h)
```
对话/普通拍分钟量级、安静空地/skip半小时~6小时量级，非线性流读着自然。`/skip` 仅在玩家独处无战斗无他人时放行（有人/有压力回"周围并不安全，无法快进"），门合理但意味着热闹场景只能靠对话拍慢推。

## 5. 天气
寒带长序列（每6h）：`小雪→多云→多云→多云→小雪→雪`，温带整段只在「晴」。慢、阶梯内、无突变；**温带含雪=False、寒带含雷雨=False**（气候门生效）。存档：`SAVED clock=2610 weather=雪 weather_hour=43` → 再skip变2970 → `/load` 回到 2610/雪/43（clock+weather一致）→ 全新session推进到同一世界小时同样落到「雪」（**可重放=True**，种子=stable_seed(pack_id)+hour）。

## 6. ⭐ 沉浸缺口：slice 3b —— 建议做
缺口真机明显、确实削弱沉浸：①frostgate核心张力是"风雪封山"，状态条已显「🌨️小雪/❄️雪」但叙述+NPC对白完全不提雪（哨兵只会说模板式"这鬼天气"，没接上引擎此刻真有的雪）；②把时间推到深夜次日，叙述/对白对"天黑了""这么晚还在城门口"毫无反应，时间推进体感只剩状态条数字；③NpcMoved已让进出场很有生气，时辰/天气却是哑的，落差让"活世界"只活了一半。最小有效切法：把已是player-perceivable的 `time_of_day`+`weather` 作一两句环境上下文注入叙述prompt与NPC对白prompt即可，数据现成、成本只是拼接，对天候/时辰即张力的pack收益大。**并列建议**：作息"暮夜采样稀+节拍碎"一并调（/skip跨暮夜留一两拍驻足，或给关键岗位NPC更强home黏性）。

## 改动 / 异常计数
- 引擎=否；其它pack字段=否；pack world_premise开关=是（授权，注入内存副本，fixture逐字节未改）。
- FALLBACK=0、tick超时=0（全场景）。最慢单拍42.2s<90s。

## 产出（`reports/worldclock_weather_test/`）
日志 `rhythm.log`/`regression_flagoff.log`/`regression_flagon.log`/`clock_weather_save.log`；raw逐tick `*_raw.txt`、附测 `named_npc_test.txt`、`transcript.md`(708行)；驱动脚本 `scripts/worldclock_rhythm_run.py`、`scripts/worldclock_escort_regression.py`(--flag on/off)、`scripts/worldclock_named_npc_test.py`、`scripts/worldclock_clock_weather_save.py`。
