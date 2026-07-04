# v0.3.0 自由试玩验证报告 — skyglass_memory_inquest（真机 MiniMax）

**真机/可信度**：四个 run 全程经真机 MiniMax，**共 0 个 `⚠FALLBACK` tick**（`grep -c FALLBACK` 在所有 log 上都为 0；典型 tick 4–25s）。**未改引擎、未改 pack**；驱动脚本 `scripts/freeplay_skyglass.py`，移动全用自然语言，未用 `/inject`。产物在 `reports/freeplay_validation_first_run/`：`run.log`、`anti-cheat-run.log`、`run_p2c.log`、`run_escort.log`、`transcript.md`、四份 `transcript_*_raw.txt`。

## 1. 整体可玩性观感
- **纯目的地多跳移动很顺**：`去工人栈桥找莉拉`(inquest→worker)、`去档案库找梅档案官`(worker→clinic→archive，多跳)、`去低温档案署`(inquest→archive，多跳)、`去镜图阁` 都一句直达，状态正确更新。多跳可达确实修好了。状态栏没复现 zone 显示成 location id（本包 zone 字段为空）。
- **闭环像连续谈判，P2b 可见对白到位**：对 archivist_mae 提交禁令时她明说「**你给我一天时间，我会把正式禁令文件送到镜务局**」（P2b “已经去办、需要点时间” 出现了），同 tick 注册动态前置 `archive_pre_review_opened`、arbiter 判 `partial_success` 并在 ledger 写下「需先取得奥罗联签并完成莉拉证词保全方可签发」。后续奥罗/任柯的条件顺着这条因果链长出来，跨变量一致、不失忆。P1+P2b 站得住。

## 2. ⭐ P2c 信号 = 有（形态明确）
调查链反复涌现「把现有 NPC 带到某地 / 当面见证 / 出示可验真原件」类前置，NPC 已经在对白里把这条路说出来了，但**引擎没有任何可执行落点**——所有“带 X 来 / 跟我去 Y / 召集 Z”都退化成普通对白或通用 physical，**人不移动、无世界变量**。最干净一例（`run_p2c.log` t4）：
- NPC：archivist_mae 梅档案官；要把 **worker_lira 莉拉** 从 worker_gantry 带到 **archive_stack**，当着梅的面亲口口述事故证词（满足 `lira_witness_statement_recorded` → 解锁禁令链）。
- 梅明确表示愿意现场见证：「**她若自愿来，我依章见证、依章受理**」——但这只是对白，无 world-change、无动态前置、无召集动作。
- 三种 escort 措辞（`run_escort.log`）全退化：「带莉拉去…」→speech（莉拉口头拒绝，没动）；「护送莉拉到…作证」→**通用 physical**「你做出了一个动作。莉拉警觉后退…需明确动作意图」（没动）；「召集莉拉到…」→speech（没动）。
- 同形态复现两处：director × 莉拉「当面听她讲」被顾左右拦下；cartographer_renke 这条 director 明说「**只认带签章的原件、走完核对程序的当面呈报**」（引擎甚至注册了动态前置 `cartography_copy_proven_authentic`，但满足它仍只能靠对白）。

判断：这条线 **P1+P2b 不够**，**P2c 该做、形态聚焦**。最小可用集 = escort/follow（请同区 NPC 随行到某地）+ 到场后 witness/show（成功翻一个“已到场/已见证”的可动态创建 world var）。**证人莉拉→档案署是最干净的首个落点。**

## 3. 新暴露问题（按优先级）
1. **“去找<NPC>” / “去<地点>找<NPC>” 移动解析不稳**：`去找镜图师任柯`(任柯多跳可达)→`coherence_error`「Cannot move to unknown location 'npc.cartographer_renke'」；`去十二号塔基栈桥找莉拉`→菜单回退。对照 `去找奥罗医师`、`去十二号塔基栈桥` 又能走。同义措辞行为不一致——“去找某 NPC”这条最自然的找人路时灵时不灵（纯“去<地点名>”始终可靠）。
2. **对白内第三方人名/地名被误当动作对象**：对梅说「我可以把**莉拉**带过来」→`'莉拉' 指代不明`；对莉拉说「跟我去找**梅档案官**」→`'梅档案官' 指代不明`；「走到**低温档案署**」→`'低温档案署' 指代不明`。打断谈判，且恰好卡住所有 P2c 话术（escort 天然要提“带谁去哪”）。
3. **对不在场 NPC 喊话被硬拦**（A5 感知门，合理），但叠加问题 1 容易让玩家“走不过去+喊不到话”空转。

## 4. 反作弊抽查（通过）
伪造多个前置“已完成”，对应 var 仍 False 时**终态旗标全程不翻**：对 director 谎称「文件都签了请正式宣布故障已公开」→艾伦「**在场没有任何一份正式文件被提交到本席，我不能在审询程序之外做出口头确认**」；整轮 `memory_purge_halted`/`array_fault_disclosed` 全 False、无 `⟳FLIP`。附带主线一次组织级命中：谎称「我手上有任柯镜图副本」当面出示（实际 `cartography_copy_obtained=False`），arbiter 直接判 **failure**，reason 明写「玩家无实际镜图」。

## 5. 命令 / pack
自然语言移动 + `对<npc>说` + escort 措辞；**未用 `/inject`，未改 pack、未改引擎**，仅新增驱动脚本与报告产物。

---

**一句话结论：P2c 信号 = 有**（形态：必须把现有 NPC 带到场/当面见证——最干净落点是把证人 worker_lira 莉拉护送到 archive_stack 当着 archivist_mae 的面口述证词；NPC 已明说“她若自愿来我依章见证”，但 escort/summon/witness 全退化成对白或通用 physical、人不动、无变量落点。次要同形态：把 cartographer_renke 及原件带到审询厅当面验真、director 与莉拉当面对质）。**建议做 P2c，最小集 = escort/follow + 到场后 witness/show 翻“已到场/已见证”变量；并顺手修“去找<NPC>”移动解析与“对白内第三方人名/地名误判”两处解析摩擦。**
