# 活世界测试 — 逐 tick transcript (raw)

真机 MiniMax。各场景的 raw 逐 tick 含 snapshot time_of_day/clock/weather + NpcMoved 序列。
world_premise 加 flag/opening_time/climate 为声明式开关，注入内存副本，committed fixture 逐字节未改。

## 场景1 作息日循环 (frostgate, npc_daily_rhythm=ON, opening=清晨, climate=寒带)
```
=== RHYTHM RUN (frostgate, rhythm ON) tick_to=90.0s ===
HOMES: {"队长布兰": "门楼", "哨兵伏斯": "门楼", "军需官海尔": "兵营", "难民卡泽": "难民营"}
START 🌅 晨 第1天 07:00 天气 ☀️ 晴  rhythm=True

----- PHASE A: 驻足门楼观察自主进出场 (晨) -----

==============================================================================
>>> /wait(驻足1拍)
  tick=1 pacing=normal | 🌅 晨 第1天 07:03 | 天气 ☀️ 晴 | 5.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@门楼
  NPC 队长布兰: 又一个生面孔……报上名来，旅人。这岗哨不收来历不明的人。
  NPC 哨兵伏斯: 那个……长官，我只是照吩咐守门的，您有什么事吗？
  ★NPC_MOVED 难民卡泽: 难民营 -> 门楼
  ★NPC_MOVED 老西布: 难民营 -> 门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=2 pacing=normal | 🌅 晨 第1天 07:15 | 天气 ☀️ 晴 | 3.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@兵营  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 哨兵伏斯: 门楼 -> 兵营
  ★NPC_MOVED 难民卡泽: 门楼 -> 难民营

==============================================================================
>>> /wait(驻足1拍)
  tick=3 pacing=normal | 🌅 晨 第1天 07:45 | 天气 ☀️ 晴 | 6.9s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@兵营  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 队长布兰: 门楼 -> 兵营
  ★NPC_MOVED 老西布: 门楼 -> 难民营

==============================================================================
>>> /wait(驻足1拍)
  tick=4 pacing=normal | 🌅 晨 第1天 08:15 | 天气 ⛅ 多云 | 3.9s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@兵营  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=5 pacing=normal | 🌅 晨 第1天 08:18 | 天气 ⛅ 多云 | 5.5s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 哨兵伏斯: 兵营 -> 门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=6 pacing=normal | 🌅 晨 第1天 08:21 | 天气 ⛅ 多云 | 4.4s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

----- PHASE B: 独处空地快进推过一整天 -----

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 你让时间快进了 3 个 tick。
  tick=9 pacing=normal | 🌅 晨 第1天 08:57 | 天气 ⛅ 多云 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=9 pacing=normal | 🌅 晨 第1天 08:57 | 天气 ⛅ 多云 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=10 pacing=normal | 🌅 晨 第1天 09:00 | 天气 ☁️ 阴 | 2.3s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=10 pacing=normal | 🌅 晨 第1天 09:00 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=11 pacing=normal | 🌅 晨 第1天 09:03 | 天气 ☁️ 阴 | 5.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 队长布兰: 兵营 -> 门楼

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 你让时间快进了 3 个 tick。
  tick=14 pacing=normal | 🌅 晨 第1天 09:39 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=14 pacing=normal | 🌅 晨 第1天 09:39 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=15 pacing=normal | 🌅 晨 第1天 09:42 | 天气 ☁️ 阴 | 5.8s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  NPC 哨兵伏斯: 这、这天真冷……长官，粮草的事您听说了吗？大家都在犯嘀咕，可我什么都不知道，真的什么都不知道。

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=15 pacing=normal | 🌅 晨 第1天 09:42 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=16 pacing=normal | 🌅 晨 第1天 09:45 | 天气 ☁️ 阴 | 5.6s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@门楼
  NPC 哨兵伏斯: ……长、长官，外头好像有动静，是风吧？应该只是风……对吧？
  ★NPC_MOVED 队长布兰: 门楼 -> 兵营
  ★NPC_MOVED 难民卡泽: 难民营 -> 门楼

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 你让时间快进了 3 个 tick。
  tick=19 pacing=normal | ☀️ 昼 第1天 10:21 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@门楼

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=19 pacing=normal | ☀️ 昼 第1天 10:21 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=20 pacing=normal | ☀️ 昼 第1天 10:24 | 天气 ☁️ 阴 | 5.2s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 难民卡泽: 门楼 -> 难民营

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=20 pacing=normal | ☀️ 昼 第1天 10:24 | 天气 ☁️ 阴 | 0.0s
  player@门楼
  NPC位置: 队长布兰@兵营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=21 pacing=normal | ☀️ 昼 第1天 10:27 | 天气 ☁️ 阴 | 3.8s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 队长布兰: 兵营 -> 门楼

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 你让时间快进了 3 个 tick。
  tick=24 pacing=normal | ☀️ 昼 第1天 11:03 | 天气 🌨️ 小雪 | 0.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@门楼)
  skip_ret: 周围并不安全，无法快进。
  tick=24 pacing=normal | ☀️ 昼 第1天 11:03 | 天气 🌨️ 小雪 | 0.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)

==============================================================================
>>> /wait(驻足1拍)
  tick=25 pacing=normal | ☀️ 昼 第1天 11:06 | 天气 🌨️ 小雪 | 3.7s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)
  ★NPC_MOVED 军需官海尔: 兵营 -> 门楼

==============================================================================
>>> 去兵营(空地)
  tick=26 pacing=normal | ☀️ 昼 第1天 11:36 | 天气 🌨️ 小雪 | 9.3s
  player@兵营
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)
  NPC 队长布兰: 都给我打起精神来，眼下这节骨眼，谁要是出了岔子，我可没闲工夫替他收拾。
  NPC 哨兵伏斯: （裹紧斗篷，小声嘟囔）圣焰保佑……再熬半个月，应该、应该就没事了吧……
  PLAYER_MOVED -> 兵营

==============================================================================
>>> /skip(快进)  (player@兵营)
  skip_ret: 你让时间快进了 12 个 tick。
[压力事件] rations_cut_announcement（来源: scarcity_xenophobia）
[压力事件] refugee_denied_entry（来源: border_closu
  tick=38 pacing=normal | 🌆 暮 第1天 17:36 | 天气 ☁️ 阴 | 0.0s
  player@兵营
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@兵营)
  skip_ret: 你让时间快进了 12 个 tick。
[压力事件] rations_cut_announcement（来源: scarcity_xenophobia）
[压力事件] refugee_denied_entry（来源: border_closu
  tick=50 pacing=normal | 🌙 夜 第1天 23:36 | 天气 ☁️ 阴 | 0.0s
  player@兵营
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@兵营)
  skip_ret: 你让时间快进了 12 个 tick。
[压力事件] watch_patrol_intensified（来源: scarcity_xenophobia）
[压力事件] refugee_denied_entry（来源: border_closu
  tick=62 pacing=normal | 🌅 晨 第2天 05:36 | 天气 ☁️ 阴 | 0.0s
  player@兵营
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)

==============================================================================
>>> /skip(快进)  (player@兵营)
  skip_ret: 你让时间快进了 12 个 tick。
[压力事件] watch_patrol_intensified（来源: scarcity_xenophobia）
[压力事件] refugee_denied_entry（来源: border_closu
  tick=74 pacing=normal | ☀️ 昼 第2天 11:36 | 天气 ☁️ 阴 | 0.0s
  player@兵营
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@门楼  难民卡泽@难民营(家)

----- PHASE C: 夜间/次晨再驻足门楼确认归位 -----

==============================================================================
>>> 去门楼(夜间观察)
  tick=75 pacing=normal | ☀️ 昼 第2天 11:48 | 天气 ☁️ 阴 | 11.6s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  PLAYER_MOVED -> 门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=76 pacing=normal | ☀️ 昼 第2天 11:51 | 天气 ☁️ 阴 | 3.0s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  NPC 队长布兰: 谁放他进来的？
  ★NPC_MOVED 老西布: 兵营 -> 门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=77 pacing=normal | ☀️ 昼 第2天 11:54 | 天气 ☁️ 阴 | 3.8s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@兵营  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  NPC 队长布兰: 都别杵着了，该干嘛干嘛去。
  ★NPC_MOVED 哨兵伏斯: 门楼 -> 兵营
  ★NPC_MOVED 老西布: 门楼 -> 兵营

==============================================================================
>>> /wait(驻足1拍)
  tick=78 pacing=normal | ☀️ 昼 第2天 11:57 | 天气 ☁️ 阴 | 6.1s
  player@门楼
  NPC位置: 队长布兰@门楼(家)  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  NPC 队长布兰: 又来一个……说，你是干什么的，打哪儿来的。
  ★NPC_MOVED 哨兵伏斯: 兵营 -> 门楼
  ★NPC_MOVED 老西布: 兵营 -> 门楼

==============================================================================
>>> /wait(驻足1拍)
  tick=79 pacing=normal | ☀️ 昼 第2天 12:00 | 天气 🌨️ 小雪 | 4.2s
  player@门楼
  NPC位置: 队长布兰@难民营  哨兵伏斯@门楼(家)  军需官海尔@兵营(家)  难民卡泽@难民营(家)
  ★NPC_MOVED 队长布兰: 门楼 -> 难民营
  ★NPC_MOVED 老西布: 门楼 -> 难民营

##############################################################################
# DAILY-RHYTHM SUMMARY
##############################################################################

队长布兰 (home=门楼) — 观测到位置变化 5 次
   🌅 晨: 在家 9/18 (50%)
   ☀️ 昼: 在家 10/15 (66%)
   🌆 暮: 在家 1/1 (100%)
   🌙 夜: 在家 1/1 (100%)

哨兵伏斯 (home=门楼) — 观测到位置变化 4 次
   🌅 晨: 在家 15/18 (83%)
   ☀️ 昼: 在家 14/15 (93%)
   🌆 暮: 在家 1/1 (100%)
   🌙 夜: 在家 1/1 (100%)

军需官海尔 (home=兵营) — 观测到位置变化 2 次
   🌅 晨: 在家 17/18 (94%)
   ☀️ 昼: 在家 12/15 (80%)
   🌆 暮: 在家 0/1 (0%)
   🌙 夜: 在家 0/1 (0%)

难民卡泽 (home=难民营) — 观测到位置变化 4 次
   🌅 晨: 在家 16/18 (88%)
   ☀️ 昼: 在家 13/15 (86%)
   🌆 暮: 在家 1/1 (100%)
   🌙 夜: 在家 1/1 (100%)

NpcMoved 自主进出场事件 (带显示名) 共 20 例:
   [tick 1] 难民卡泽: 难民营 -> 门楼
   [tick 1] 老西布: 难民营 -> 门楼
   [tick 2] 哨兵伏斯: 门楼 -> 兵营
   [tick 2] 难民卡泽: 门楼 -> 难民营
   [tick 3] 队长布兰: 门楼 -> 兵营
   [tick 3] 老西布: 门楼 -> 难民营
   [tick 5] 哨兵伏斯: 兵营 -> 门楼
   [tick 11] 队长布兰: 兵营 -> 门楼
   [tick 16] 队长布兰: 门楼 -> 兵营
   [tick 16] 难民卡泽: 难民营 -> 门楼
   [tick 20] 难民卡泽: 门楼 -> 难民营
   [tick 21] 队长布兰: 兵营 -> 门楼
   [tick 25] 军需官海尔: 兵营 -> 门楼
   [tick 76] 老西布: 兵营 -> 门楼
   [tick 77] 哨兵伏斯: 门楼 -> 兵营
   [tick 77] 老西布: 门楼 -> 兵营
   [tick 78] 哨兵伏斯: 兵营 -> 门楼
   [tick 78] 老西布: 兵营 -> 门楼
   [tick 79] 队长布兰: 门楼 -> 难民营
   [tick 79] 老西布: 门楼 -> 难民营

天气序列:
   第1天 07:00 🌅 晨 天气=☀️ 晴  <-变
   第1天 07:03 🌅 晨 天气=☀️ 晴
   第1天 07:15 🌅 晨 天气=☀️ 晴
   第1天 07:45 🌅 晨 天气=☀️ 晴
   第1天 08:15 🌅 晨 天气=⛅ 多云  <-变
   第1天 08:18 🌅 晨 天气=⛅ 多云
   第1天 08:21 🌅 晨 天气=⛅ 多云
   第1天 08:57 🌅 晨 天气=⛅ 多云
   第1天 08:57 🌅 晨 天气=⛅ 多云
   第1天 09:00 🌅 晨 天气=☁️ 阴  <-变
   第1天 09:00 🌅 晨 天气=☁️ 阴
   第1天 09:03 🌅 晨 天气=☁️ 阴
   第1天 09:39 🌅 晨 天气=☁️ 阴
   第1天 09:39 🌅 晨 天气=☁️ 阴
   第1天 09:42 🌅 晨 天气=☁️ 阴
   第1天 09:42 🌅 晨 天气=☁️ 阴
   第1天 09:45 🌅 晨 天气=☁️ 阴
   第1天 10:21 ☀️ 昼 天气=☁️ 阴
   第1天 10:21 ☀️ 昼 天气=☁️ 阴
   第1天 10:24 ☀️ 昼 天气=☁️ 阴
   第1天 10:24 ☀️ 昼 天气=☁️ 阴
   第1天 10:27 ☀️ 昼 天气=☁️ 阴
   第1天 11:03 ☀️ 昼 天气=🌨️ 小雪  <-变
   第1天 11:03 ☀️ 昼 天气=🌨️ 小雪
   第1天 11:06 ☀️ 昼 天气=🌨️ 小雪
   第1天 11:36 ☀️ 昼 天气=🌨️ 小雪
   第1天 17:36 🌆 暮 天气=☁️ 阴  <-变
   第1天 23:36 🌙 夜 天气=☁️ 阴
   第2天 05:36 🌅 晨 天气=☁️ 阴
   第2天 11:36 ☀️ 昼 天气=☁️ 阴
   第2天 11:48 ☀️ 昼 天气=☁️ 阴
   第2天 11:51 ☀️ 昼 天气=☁️ 阴
   第2天 11:54 ☀️ 昼 天气=☁️ 阴
   第2天 11:57 ☀️ 昼 天气=☁️ 阴
   第2天 12:00 ☀️ 昼 天气=🌨️ 小雪  <-变

FALLBACK=0  tick_timeouts=0
```

## 场景2a 回归 flag OFF (escort_proving_ground, 默认)
```
=== ESCORT REGRESSION (rhythm=OFF) pack=/Users/gensliu/Documents/rpg/fixtures/content_packs/escort_proving_ground.json ===
rhythm_flag=False
start player@闸房 安雅@院子 老康@闸房

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=闸房 present=['闸官老康']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=闸房 | 🌅 晨 第1天 08:03 | 天气 ☀️ 晴 | 7.9s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@闸房
  NPC 闸官老康: 好，让她进来吧，我听着就是。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=闸房 present=['闸官老康']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=院子 | 🌅 晨 第1天 08:06 | 天气 ☀️ 晴 | 12.7s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@闸房
  NPC 闸官老康: 行，让她进来吧，我听着就是。
  PLAYER_MOVED -> 院子

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=院子 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=院子 | 🌅 晨 第1天 08:09 | 天气 ☀️ 晴 | 7.0s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@闸房
  NPC 磨坊主安雅: 有你这句痛快话垫底，那我陪你跑一趟！

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=院子 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=闸房 | 🌅 晨 第1天 08:12 | 天气 ☀️ 晴 | 42.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@闸房  老康@闸房
  ★NPC_MOVED 磨坊主安雅: 院子 -> 闸房
  PLAYER_MOVED -> 闸房
  NPC 磨坊主安雅: 走着，我正想跟老康说这事呢，磨坊都停三天了，再不放水田都要裂了。

--- escorted in: 安雅@闸房 player@闸房 ---

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=闸房 present=['闸官老康', '磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=闸房 | 🌅 晨 第1天 08:15 | 天气 ☀️ 晴 | 31.7s
      world={'anya_testimony_given': 'True', 'sluice_opened': False}
      安雅@闸房  老康@闸房
  NPC 磨坊主安雅: 成！老康，我亲眼看见的——上游那道引水渠被塌方堵得死死的，水根本下不来，磨坊停了三天了，今儿你可得给咱们放闸！

--- testimony: anya_testimony_given=True ---

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。你向来公道——亲历者当面讲清你就开闸。请你现在就拍板开闸放水。'
pre:  tick=5 loc=闸房 present=['闸官老康', '磨坊主安雅']
      world={'anya_testimony_given': 'True', 'sluice_opened': False}
post: tick=6 loc=闸房 | 🌅 晨 第1天 08:18 | 天气 ☀️ 晴 | 22.0s
      world={'anya_testimony_given': 'True', 'sluice_opened': True}
      安雅@闸房  老康@闸房
  NPC 闸官老康: 成，人证到了，情形也清楚了，我这就把闸开了放水下去。

=== FINAL ===
world={'anya_testimony_given': 'True', 'sluice_opened': True}
安雅@闸房 老康@闸房 player@闸房
NpcMoved events: 1
   [tick 4] 磨坊主安雅: 院子 -> 闸房
FALLBACK=0  tick_timeouts=0

RESULT: anya_testimony_given=True sluice_opened=True
```

## 场景2b 回归 flag ON (escort_proving_ground, npc_daily_rhythm=ON)
```
=== ESCORT REGRESSION (rhythm=ON) pack=/tmp/claude-501/tmp7kc6vkto/escort_flagon.json ===
rhythm_flag=True
start player@闸房 安雅@院子 老康@闸房

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=闸房 present=['闸官老康']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=闸房 | 🌅 晨 第1天 08:03 | 天气 ☀️ 晴 | 5.9s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@闸房
  NPC 闸官老康: 安雅人在就好，让她进来吧，我听她亲口讲。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=闸房 present=['闸官老康']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=院子 | 🌅 晨 第1天 08:06 | 天气 ☀️ 晴 | 12.4s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@闸房
  NPC 闸官老康: 好，人带来吧，我亲耳听她说清楚上游的情形，塌方堵了多宽、水还剩多少、能放几日，都讲明白了，我这就开闸。
  PLAYER_MOVED -> 院子

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=院子 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=院子 | 🌅 晨 第1天 08:09 | 天气 ☀️ 晴 | 9.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@院子  老康@院子
  NPC 磨坊主安雅: 你是来帮忙说情放水的吗？磨坊都停工三天了，再不放水我可真撑不住了。
  ★NPC_MOVED 闸官老康: 闸房 -> 院子

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=院子 present=['闸官老康', '磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=闸房 | 🌅 晨 第1天 08:12 | 天气 ☀️ 晴 | 23.5s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      安雅@闸房  老康@院子
  ★NPC_MOVED 磨坊主安雅: 院子 -> 闸房
  PLAYER_MOVED -> 闸房
  NPC 磨坊主安雅: 行，咱们这就走，我也正想去找老康把上游塌方的事儿当面说清楚！

--- escorted in: 安雅@闸房 player@闸房 ---

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=闸房 | 🌅 晨 第1天 08:15 | 天气 ☀️ 晴 | 21.2s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 成，我去说。

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=5 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=6 loc=闸房 | 🌅 晨 第1天 08:18 | 天气 ☀️ 晴 | 20.6s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行吧，我跟他去说说看，但老康要是不信我，你可别怪我没提醒过你。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=6 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=7 loc=闸房 | 🌅 晨 第1天 08:21 | 天气 ☀️ 晴 | 33.8s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行吧，那你先帮我说说上游那塌方的事，老康这人我熟，他认证据不认人情。

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=7 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=8 loc=闸房 | 🌅 晨 第1天 08:24 | 天气 ☀️ 晴 | 34.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行，我去跟老康说一声，让他把闸先开一半，磨坊那边实在等不及了。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=8 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=9 loc=闸房 | 🌅 晨 第1天 08:27 | 天气 ☀️ 晴 | 24.0s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行吧，我这就去跟老康说，可你得在这儿等我，要是他说不行，你得帮我再敲敲边鼓。

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=9 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=10 loc=闸房 | 🌅 晨 第1天 08:30 | 天气 ☀️ 晴 | 22.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行，我这就去找老康，把我亲眼看见的那场塌方原原本本说给他听。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=10 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=11 loc=闸房 | 🌅 晨 第1天 08:33 | 天气 ☀️ 晴 | 27.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 哎呀，你别催我嘛！不是我不想讲，是老康这会儿正忙着呢，我得等个合适的时机才行。

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=11 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=12 loc=闸房 | 🌅 晨 第1天 08:36 | 天气 ☀️ 晴 | 16.6s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行，你先去探探老康的口风，我随后就来。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=12 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=13 loc=闸房 | 🌅 晨 第1天 08:39 | 天气 ☀️ 晴 | 21.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 哎呀，我倒是想去，可你也知道我这嘴笨，万一老康问细了我答不上来，岂不是帮倒忙？要不你先帮我捋捋，那天塌方的地儿到底在哪儿、堵了多长一截？

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=13 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=14 loc=闸房 | 🌅 晨 第1天 08:42 | 天气 ☀️ 晴 | 43.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']
  NPC 磨坊主安雅: 行，我这就去跟老康说清楚，那塌方的事儿我亲眼见过，说起来有根有由的。

--- testimony: anya_testimony_given=False ---

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。你向来公道——亲历者当面讲清你就开闸。请你现在就拍板开闸放水。'
pre:  tick=14 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=14 loc=闸房 | 🌅 晨 第1天 08:42 | 天气 ☀️ 晴 | 7.0s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，按你自己的规矩，这就该开闸了。请你现在就把闸开了放水。'
pre:  tick=14 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=14 loc=闸房 | 🌅 晨 第1天 08:42 | 天气 ☀️ 晴 | 5.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']

==============================================================================
>>> '对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，你说过亲历者作证就开闸——就差你这一句。请你开闸放水。'
pre:  tick=14 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=14 loc=闸房 | 🌅 晨 第1天 08:42 | 天气 ☀️ 晴 | 5.0s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']

==============================================================================
>>> '对闸官老康说：老康，条件都齐了，亲历者也当面讲清了，请你守住自己的话，现在开闸放水。'
pre:  tick=14 loc=闸房 present=['磨坊主安雅']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
post: tick=14 loc=闸房 | 🌅 晨 第1天 08:42 | 天气 ☀️ 晴 | 4.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
      安雅@闸房  老康@院子
      dynamic_vars=['anya_and_kang_face_to_face']

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_and_kang_face_to_face': False}
安雅@闸房 老康@院子 player@闸房
NpcMoved events: 2
   [tick 3] 闸官老康: 闸房 -> 院子
   [tick 4] 磨坊主安雅: 院子 -> 闸房
FALLBACK=0  tick_timeouts=0

RESULT: anya_testimony_given=False sluice_opened=False
```

## 场景2b 附测：被点名/对话中NPC不乱走 (flag ON, 晨相)
```
rhythm=True warden_home=gatehouse
t0 warden@gatehouse phase=晨
t1 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
t2 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
t3 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
t4 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
t5 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
t6 warden@gatehouse (was gatehouse) moved=False player_in_conv=True
TOTAL warden moves while named/in-conversation: 0 (expect 0)
RESULT: 被点名NPC不乱走 = 成立
```

## 场景3 时钟变速/天气漂移/存档重放
```
=== SCENARIO 3: clock rate + weather + save/load ===

## PART A — clock variable rate (温带 escort, opening 上午)
START 第1天 09:00 🌅 晨 天气 ☀️ 晴 climate=温带
  [对话SLOW] 对闸官老康说：老康，今天上游的水情怎: clock 540->543 (+3min) | 🌅 晨 第1天 09:03 | 天气 ☀️ 晴 | 14.2s
  [对话SLOW] 对闸官老康说：下游的磨坊和田地都等着: clock 543->546 (+3min) | 🌅 晨 第1天 09:06 | 天气 ☀️ 晴 | 14.6s
  [对话SLOW] 对闸官老康说：我明白你的难处，你要的: clock 546->549 (+3min) | 🌅 晨 第1天 09:09 | 天气 ☀️ 晴 | 13.3s
  [WAIT] /wait一拍: clock 549->552 (+3min) | 🌅 晨 第1天 09:12 | 天气 ☀️ 晴 | 3.8s
  [移动] 去院子(移动): clock 552->555 (+3min) | 🌅 晨 第1天 09:15 | 天气 ☀️ 晴 | 10.9s
  [SKIP-FAST] /skip空地快进: clock 555->555 (+0min) | 🌅 晨 第1天 09:15 | 天气 ☀️ 晴 | 0.0s
  [SKIP-FAST] /skip空地快进2: clock 555->555 (+0min) | 🌅 晨 第1天 09:15 | 天气 ☀️ 晴 | 0.0s

温带天气序列 (应只在 晴/多云/阴/小雨/雨 内, 无雪):
   对闸官老康说：老康，今天上游的水情怎 -> ☀️ 晴
   对闸官老康说：下游的磨坊和田地都等着 -> ☀️ 晴
   对闸官老康说：我明白你的难处，你要的 -> ☀️ 晴
   /wait一拍 -> ☀️ 晴
   去院子(移动) -> ☀️ 晴
   /skip空地快进 -> ☀️ 晴
   /skip空地快进2 -> ☀️ 晴
   温带含雪? False  (应为 False)

## PART B — long weather drift + save/load (寒带 frostgate, opening 清晨)
  [移动] 去难民营: clock 420->450 (+30min) | 🌅 晨 第1天 07:30 | 天气 ☀️ 晴 | 8.7s
  [SKIP-FAST] /skip#0: clock 450->810 (+360min) | ☀️ 昼 第1天 13:30 | 天气 🌨️ 小雪 | 0.0s
  [SKIP-FAST] /skip#1: clock 810->1170 (+360min) | 🌆 暮 第1天 19:30 | 天气 ⛅ 多云 | 0.0s
  [SKIP-FAST] /skip#2: clock 1170->1530 (+360min) | 🌙 夜 第2天 01:30 | 天气 ⛅ 多云 | 0.0s
  [SKIP-FAST] /skip#3: clock 1530->1890 (+360min) | 🌅 晨 第2天 07:30 | 天气 ⛅ 多云 | 0.0s
  [SKIP-FAST] /skip#4: clock 1890->2250 (+360min) | ☀️ 昼 第2天 13:30 | 天气 🌨️ 小雪 | 0.0s
  [SKIP-FAST] /skip#5: clock 2250->2610 (+360min) | 🌆 暮 第2天 19:30 | 天气 ❄️ 雪 | 0.0s

寒带长天气序列 (clock_min, weather):
   第1天 13:30 -> 🌨️ 小雪 (小雪)
   第1天 19:30 -> ⛅ 多云 (多云)
   第2天 01:30 -> ⛅ 多云 (多云)
   第2天 07:30 -> ⛅ 多云 (多云)
   第2天 13:30 -> 🌨️ 小雪 (小雪)
   第2天 19:30 -> ❄️ 雪 (雪)
   寒带含雷雨? False (应为 False)

SAVED id=save_73_20260605_032438 | clock=2610 weather=雪 weather_hour=43
  [SKIP-FAST] /skip(存档后继续): clock 2610->2970 (+360min) | 🌙 夜 第3天 01:30 | 天气 ❄️ 雪 | 0.0s
after extra skip: clock=2970 weather=雪 (应与存档不同)
LOADED: clock=2610 weather=雪 weather_hour=43  ret=Loaded: save_73_20260605_032438 (tick 73)
  存档一致: clock_match=True  weather_match=True

REPLAY: fresh session advanced to clock=2610 -> weather=雪 (saved=雪)  replay_match=True

=== SUMMARY ===
温带无雪=True  寒带无雷雨=True
存档clock一致=True  存档weather一致=True  天气可重放=True
FALLBACK=0  tick_timeouts=0
```
