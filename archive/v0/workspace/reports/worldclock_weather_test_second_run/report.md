# slice 3b 验证 · 第二跑 — NPC 是否真接住天候/时辰

真机 MiniMax 实连，每 tick 90s 看门狗 + provider 55s socket。**未改任何引擎/其它 pack 内容**（`git diff HEAD -- src/ fixtures/` 为空）。仅按授权在 `world_premise` 加声明式开关、注入**内存副本**，committed fixture 逐字节未改。全程自然语言、未用 `/inject`。**FALLBACK=0、tick 超时=0**，单测 `test_npc_dialogue/test_worldclock/test_weather` 53 passed/1 skipped。

## 改了哪些 pack 开关（仅 world_premise，授权）
- 主跑（雪夜对白）：`climate=寒带` · `opening_weather=雪` · `opening_time=深夜`。
  ⚠ 任务写的是 `opening_time=夜里`，但引擎命名时刻表 `worldclock._NAMED_OPENINGS` **没有"夜里"这个词**，未识别会回落默认 08:00（第一次跑确实落到 🌅晨 08:00）。改用引擎已识别的 `深夜`(=01:00)，它正落在**夜**时段、`time_phrase` 渲染为「夜里」——得到正是预期的雪+夜里，**只动声明值未改引擎**。实测开局即 `🌙 夜 第1天 01:00 天气 ❄️ 雪`，注入对白 prompt 的 env 行经脚本核实为 `'此刻是夜里，下着雪。'`。
- 过渡跑：`寒带/雪/opening_time=19:30`(暮，距夜20:00仅30min)`/npc_daily_rhythm=true`。
引擎=否；其它 pack 字段=否。

## 1. ⭐ NPC 接住天候/时辰 = **自然接住**
雪夜里对哨兵/队长连说 6 轮，真机原话：
- **[哨兵伏斯]**「老实说……看他们那样，我**夜里**都睡不踏实。」
- **[哨兵伏斯]**「**夜里**安静点好，能听见外头有没有动静……你快回去睡吧，**这风冷得很**。」
- **[队长布兰]**「谁的日子都不好过，但城墙不会因为我们苦就自己守自己。」

对照第一跑「哨兵只会模板腔『这鬼天气』、不接此刻真有的雪」——本跑哨兵**两次主动把"夜里"织进回话**、并带出"这风冷得很"（寒带雪夜体感），是与当下时辰/天候对齐的非模板回应。**判定：自然接住**（哨兵尤其明显；队长两条偏务实、未直接点雪，但无失语未跑题）。

## 2. 过渡叙述 = **上得来、不刷屏**（但有一道 /skip 缝）
**关键机制发现（真实，非脚本 bug）**：ambient 过渡 `Narration` 由 `run_tick → _emit_environment_transition` 发，这是 **/wait 与自然输入**路径；而 **`/skip` 的 `_handle_skip` 直接调 `_advance_tick_with_pacing`、绕过 `_emit_environment_transition`**（`session.py:555-556` vs `2555`）——**用 /skip 跨边界时过渡叙述是哑的**。改用 /wait 跨 暮→夜 后如期上来：
```
🌆 暮 19:57 天气 ❄️雪  →  🌙 夜 20:09 天气 ❄️雪
  ⏱☁ TIME/WX TRANSITION: 夜幕四合，天黑透了。   ← 跨界那一拍恰一句时段线，不刷屏
```
- **天气过渡线**：在 /skip 那版跑里实测天气确有变化 `❄️雪→🌨️小雪`(19:21)，证明天气会动；其 `天气变了，…。` 走与时段线**同一处 `_emit_environment_transition`**（`weather_change_line`，单测覆盖），同样只在 /wait 发不在 /skip 发。本跑 /wait 窗口内寒带雪 random-walk 多原地、未恰好撞上天气切换那一拍，故未抓到天气线**真机原话**；时段线已确证机制成立且不刷屏。
- ⚠ **附带发现（建议回流作者）**：`/skip` 快进路径不发过渡叙述——而玩家最可能用 /skip "等到天黑/天亮"，恰恰看不到那句过渡叙述。建议把 `_emit_environment_transition` 也接进 `_handle_skip`。本跑未改引擎、仅如实记录。

## 3. 沉浸缺口 = **对白侧合上、/skip 过渡侧仍缺**
哨兵在雪夜里主动说"夜里""这风冷得很"，时辰/天候第一次和已很有生气的 NpcMoved 进出场（本跑亦见 `难民卡泽:难民营->门楼`、`队长布兰:门楼->兵营` 带显示名）在同一场景对齐——"活世界"明显更完整。剩一道缝是 /skip 快进不发过渡叙述。

## 4. 零回归 / FALLBACK=0 / 超时=0
加这句对白 prompt **未引发任何 PARSE/VALIDATION 退化**：两段真机跑共 13 个对话/等待拍，**FALLBACK=0、tick 超时=0**，无 schema 校验失败、API 健康，未拖慢（对白拍 4–17s，远低于 90s）。fallback reason：无（计数 0）。

## 5. A5 = **无越界**
env 行只喂玩家可感知的当地时段+当地天气。抽查 NPC 原话：哨兵只就眼前的夜/风/补给/教会说话，未提远处别地点天气、未泄露玩家私有信息。`_environment_section` 也只列同地点实体。

## 一句话结论
`NPC接住天候/时辰=自然接住`（哨兵雪夜两次主动说"夜里"+"这风冷得很"，对照首跑模板腔已是情境内非模板回应）· `过渡叙述=上得来不刷屏`（跨暮→夜恰一句「夜幕四合，天黑透了。」；**但仅 /wait/自然拍发，/skip 快进路径不发——一致性缺口，建议回流**）· `沉浸缺口=对白侧合上、/skip过渡侧仍缺` · `零回归=是` · `FALLBACK=0`(超时=0) · `A5=无越界`。

## 产出（`reports/worldclock_weather_test_second_run/`）
- 日志 `run.log`/`transition.log`；raw `raw_ticks.txt`(含 start snapshot + prompt env 行 + 每条 NPC 对白原话 + Narration)、`transition_raw.txt`(逐 /wait 的 time/clock/weather + 跨界过渡 Narration 原文 + 机制说明)；`stdout.txt`/`transition_stdout.txt`。
- driver：`scripts/worldclock_3b_immersion_run.py`、`scripts/worldclock_3b_transition_run.py`。

## 两点需作者拍板
- (a) `opening_time=夜里` 未被引擎识别（用 `深夜` 代替达成同状态）——要不要把"夜里"等裸时段词补进 `worldclock._NAMED_OPENINGS`。
- (b) `/skip` 快进不发过渡叙述这个一致性缝——是否补 `_emit_environment_transition` 到 `_handle_skip`。
