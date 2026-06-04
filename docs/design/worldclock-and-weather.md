# 世界时钟与天气（活世界 · 时间/天气模拟）

> 目标（用户拍板）：时间与天气**尽可能模拟真实**。关键洞察：我们的行为以 **tick** 为
> 基本单位，而**每个 tick 的时间尺度并不相同**——一段紧张对话的一拍只是几分钟，一次
> 「等到天亮」的快进却是几小时。所以时间不能用 `tick × 常量`，而要按这一拍的**情境密度**
> 推进一个真实的世界时钟。

## 1. 核心模型：时间挂在 Pacing 上，而非 tick 计数

引擎**已经**在为每一拍判定情境密度——`PacingSpeed`（见 `scheduler.py` /
`_advance_tick_with_pacing`）：

| PacingSpeed | 触发情境 | 步数 | 我们赋予的「每步分钟」 |
|---|---|---|---|
| `PAUSE`   | 战斗中（玩家回合仍强制 1 步） | 0→1 | 极短（≈1 分钟，命悬一线） |
| `SLOW`    | 对话 / 常规一拍（默认） | 1 | 短（≈3 分钟，一来一回） |
| `FAST`    | 安静无人、`/skip`·`/wait` 放行 | 2 | 长（≈30 分钟/步，时间流走） |
| `FORCE`   | 战役高压事件 | 3 | 中（≈12 分钟/步，事件压缩） |

> 步数本身已编码了「加速」（安静 → 更多步）；再给每步一个**与情境匹配的分钟权重**，
> 二者相乘就得到可信的、非线性的时间流。一段对话（SLOW×1 步×3 分）= 3 分钟；一次安静
> 快进（FAST×2 步×30 分）= 1 小时。这正是用户要的「每拍尺度不同」。

实现：`WorldState.clock_minutes`（自开场起的累计分钟，持久化）。`tick_advance(minutes)`
同时推进 `tick` 与 `clock_minutes`；`_advance_tick_with_pacing` 按 `speed` 取
`worldclock.minutes_for_step(speed)` 逐步推进。其他直接 `tick_advance()` 的单步路径
（仲裁/战斗）取默认 SLOW 权重。

## 2. 时段（slice 1，本期）

由 `clock_minutes` 推导，纯函数 `worldclock.time_of_day(clock_minutes)`：

| 小时（当地） | 时段 | 状态条 |
|---|---|---|
| 5–10  | 晨 | 🌅 晨 |
| 10–17 | 昼 | ☀️ 昼 |
| 17–20 | 暮 | 🌆 暮 |
| 20–5  | 夜 | 🌙 夜 |

`hour = (clock_minutes // 60) % 24`；`day = clock_minutes // 1440 + 1`（「第 N 天」）。
状态条把原本灰显的 `时段*` 占位换成真实值（如 `🌅 晨 · 第1天 06:30`）。

**开场时刻**：`pack.world_premise.opening_time`（可选，graceful）——"18:30" / "黄昏" 等，
解析为起始 `clock_minutes`；未声明则默认 08:00。当前所有包都未声明 → 落到默认，无破坏。
（把它升为一等 pack 字段是后续小活。）

## 3. 天气（slice 2，已落地）

慢变随机状态，按**流逝的世界时间**推进（不是按 tick），持久化（`engine/weather.py`）：
- `WorldState.weather`（当前条件标签）+ `weather_hour`（上次推进到的小时桶，让长跳一次补齐）。
- 包可声明 `world_premise.climate`（温带/寒带/热带/干旱/海洋）与 `opening_weather`；缺省温带、平和开局。
- **气候阶梯**取代完整马尔可夫矩阵：每个气候是一条「温和→恶劣」有序阶梯，每小时做一次
  **钳制 ±1 的随机游走**（多数原地，偶尔进/退一档）——慢演化、可信，且只需一条数组就能参数化一个气候。
  气候只会出现自己阶梯上的条件（热带无雪、寒带无雷雨）。
- 可复现：每小时一步，种子 = `stable_seed(content_pack_id) + 小时序号`（`stable_seed` 用 sha1，
  不用 Python 加盐 `hash`），存档重放落到同一片天；长跳上限 `_MAX_WEATHER_STEPS=24` 步，避免补整天历史。

## 4. 未来钩子（不在本期）

时段是「活世界」的接缝：日后可驱动 NPC **作息**（`home_location` 回归 P1.8 已是雏形——
夜里回家、白天就位）、限时事件（宵禁、换岗）、以及天气对行动/能见度的影响。本期只把
**时钟 + 时段**做实并上屏，不引入对 NPC 行为的耦合。

## 5. 落位与持久化

- 新增纯模块 `engine/worldclock.py`：`minutes_for_step` / `time_of_day` / `clock_label` /
  `parse_opening_time`（全部纯函数，单测覆盖，零引擎依赖）。
- `WorldState.clock_minutes` 字段（默认 480 = 08:00）；`tick_advance(minutes)`。
- `persistence` 存/取 `clock_minutes`（与 `tick` 并列）。
- `GameSession.__init__` 在新开局时按 `opening_time` 覆盖默认；`/load` 由存档恢复。
- 协议 `WorldSnapshot` 增 `time_of_day` / `clock`（player-perceivable，过 A5）；状态条渲染。

## 6. 增量计划

- ✅ **slice 1**：worldclock 纯模块 + 时钟字段 + pacing 挂钩 + 持久化 + 时段上状态条。
- ✅ **slice 2**：weather 纯模块（气候阶梯随机游走）+ 天气状态 + 按世界时推进 + 包气候字段 + 状态条天气位。
- **slice 3（远期）**：时段/天气驱动 NPC 作息与限时事件；天气影响行动/能见度；季节使阶梯随月份偏移。
