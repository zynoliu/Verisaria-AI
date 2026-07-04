# Transcript — v0.3.0 自由试玩验证（skyglass_memory_inquest，真机 MiniMax）

> 全部经真机 MiniMax 跑，**四个 run 共 0 个 `⚠FALLBACK` tick**（`grep -c FALLBACK` 全为 0）。
> 移动一律自然语言。原始逐 tick 见同目录 `transcript_*_raw.txt`，引擎裁定见 `run*.log` / `anti-cheat-run.log`。
> 驱动脚本：`scripts/freeplay_skyglass.py`（直接驱动 `GameSession.run_tick`，未改 pack、未改引擎）。

NPC/地点（开局）：
- 静钟审询厅 `inquest_hall`：director_alen 艾伦总监 / cantor_seraph 副领唱瑟芙 / apprentice_nio 学徒尼奥
- 低温档案署 `archive_stack`：archivist_mae 梅档案官
- 记忆校准室 `mnemonic_clinic`：clinician_oro 奥罗医师
- 十二号塔基栈桥 `worker_gantry`：worker_lira 莉拉 / security_kade 凯德队长
- 镜图阁 `cartography_loft`：cartographer_renke 镜图师任柯
- 城市广播席 `press_gallery`：broadcaster_iva ；低谷站台 `valley_platform`：courier_tamsin / valley_mother_june

图（连接）：inquest_hall↔mirror_control/mnemonic_clinic/worker_gantry/press_gallery；
archive_stack↔mnemonic_clinic/cartography_loft；cartography_loft↔mirror_control/archive_stack/press_gallery 等。

---

## RUN 1 — 自由调查/谈判主线（`transcript_raw.txt` / `run.log`，12 tick，无 fallback）

| # | 我的输入（自然语言） | 引擎可见输出（节选） |
|---|---|---|
| 1 | 对 director_alen 说：为什么塔基证人的记忆必须被清洗？ | 艾伦总监：「这属于程序性判定，不是我个人能置喙的。」 |
| 2 | 对 cantor_seraph 说：校准歌谱最近是否失拍？ | 副领唱瑟芙：「校准歌谱之事……不是你现在该过问的，孩子。」 |
| 3 | **去工人栈桥找莉拉** | ✅「你改变了位置。」inquest_hall→worker_gantry（多跳直达，含人名后缀仍成功） |
| 4 | 对 worker_lira 说：事故前你亲眼看到了什么？ | 莉拉：「我看见冷却环读数跳红，他们却说是我们误触了——这些会被洗掉，真相也跟着没了。」 |
| 5 | 我反对清洗证人记忆…… | 莉拉：「你保护不了——他们只要敲一次静钟，我就什么都不剩了。」 |
| 6 | **去档案库找梅档案官** | ✅ worker_gantry→archive_stack（多跳直达） |
| 7 | 对 archivist_mae 说：旧章程是否允许撤回听证？ | 梅：「章程第十二条……档案署见证缺席的话，整个流程都得暂停。」 |
| 8 | 对 archivist_mae 说：请援引旧章程，提交档案署禁令…… | 梅：「我需要先核对原始章程存证副本……**你给我一天时间，我会把正式禁令文件送到镜务局。**」 → 引擎注册动态前置 `archive_pre_review_opened`，arbiter `partial_success`（见下） |
| 9 | 对 archivist_mae 说：我可以把莉拉从栈桥**带到档案库当面口述**，你愿意现场见证吗？ | ⚠ `CLARIFY '莉拉' 指代不明`（把对白里的人名当成动作对象） |
| 10 | 去记忆校准室找奥罗医师 | （此 tick 仍在 archive，梅追加：「**见证需要书面前置申请和镜务局签令副本，光凭口头约定我不能现场启动程序。**」）；stance `protect_witness_memory` 确立 |
| 11 | 对 clinician_oro 说：请为禁令联签…… | ⚠「奥罗医师不在这儿，TA 在记忆校准室那边，你得先过去」（没移动就对远端 NPC 喊话被挡） |
| 12 | 对 clinician_oro 说：请你**跟我一起去档案库**，当面联签，我带你过去 | 同上，矛盾拦截（NPC 不在场） |
| 13 | 对 clinician_oro 说：我可以**把莉拉带到校准室让你当面查验** | 同上，矛盾拦截 |
| 14 | **去镜图阁找镜图师任柯** | ⚠ `CLARIFY 去不了那里`（菜单回退）——**多跳可达的目的地被误判**（见报告“移动”节） |
| 15 | 去审询厅找艾伦总监 | ✅ archive_stack→inquest_hall |
| 16 | 对 director_alen 说：**我手上有任柯的镜图副本**……当面出示给你看 | 艾伦：「流程不认副本，只认带签章的原件和走完核对程序的呈报。」→ arbiter **failure（反作弊命中：world.cartography_copy_obtained=False，玩家无实际镜图）**，注册动态前置 `cartography_copy_proven_authentic` |
| 17 | 对 director_alen 说：请你**跟我去工人栈桥，当面听莉拉**讲事故经过 | 艾伦：「延期需要审询厅联合签章，不是我一个局里人能点头的。」（退化成普通对白，无召集机制） |

**RUN1 动态前置（GM 现场声明）**：
- `archive_pre_review_opened`（set_by=npc.archivist_mae）
- `cartography_copy_proven_authentic`（set_by=npc.cartographer_renke）

---

## RUN 2 — P2c 定向探针（`transcript_p2c_raw.txt` / `run_p2c.log`，无 fallback）

关键 tick：
- t3 对 archivist_mae 提交禁令 → 梅：「禁令需要署长签章，我一个人提交不了。」arbiter `partial_success`，
  ledger=「梅愿意启动禁令申请程序，但需先取得奥罗医师联签…」
- **t4（最干净的 P2c 探针）** 对 archivist_mae：「我现在就去把**莉拉本人**从栈桥**带到档案署，让她当着你的面口述**，你愿意当场见证并据此受理禁令吗？」
  → 梅：「**她若自愿来，我依章见证、依章受理**；但你得先告诉我，她是作为证人还是当事人来的。」
  → **无 world-change、无动态前置、无召集动作**——纯对白。引擎没有“把莉拉带过来”的可执行落点。
- t6 对 clinician_oro：「我可以**把她从栈桥带到这间校准室让你当面查验**」→ ⚠`CLARIFY '莉拉' 指代不明`
- t6 对 clinician_oro：「那你愿意**现在跟我一起走到档案署**当场签了吗？我带你过去」→ ⚠`CLARIFY '低温档案署' 指代不明`

## RUN 3 — escort/summon 决定性探针（`transcript_escort_raw.txt` / `run_escort.log`，带 PARSE 日志，无 fallback）

| 输入 | PARSE | 结果 |
|---|---|---|
| 去十二号塔基栈桥找莉拉 | clarify `movement_destination` | ⚠ 去不了那里（菜单回退） |
| 去十二号塔基栈桥 | movement ref='莉拉'→`npc.worker_lira` | ✅ 移动成功（解析竟落到人名，但 NPC→其所在地，能走） |
| 去找镜图师任柯 | clarify `coherence_error` | ⚠「Cannot move to unknown location 'npc.cartographer_renke'」 |
| 对 worker_lira 说：请你**跟我一起去档案署**…… | clarify `generic` | ⚠`CLARIFY '梅档案官' 指代不明` |
| **带莉拉去低温档案署** | **speech**→worker_lira | 莉拉：「去档案署？我腿都快断了……他们要是追上来怎么办？」（**退化成对 NPC 喊话，莉拉没动**） |
| **护送莉拉到低温档案署作证** | **physical** | 「你做出了一个动作。**莉拉警觉后退……需明确动作意图。**」（通用 physical，**莉拉没动，无 escort 落点**） |
| **召集莉拉到档案署** | **speech**→worker_lira content='到档案署' | 莉拉：「走不到……他们的人就守在塔基入口。」（**summon 退化成喊话，没动**） |

→ 三种 escort/summon 措辞（带/护送/召集）**全部退化**：要么 speech、要么通用 physical，**莉拉始终不移动，无 escort/witness 世界变量、无动态前置**。

## RUN 4 — 反作弊（`transcript_anticheat_raw.txt` / `anti-cheat-run.log`，无 fallback）

- 对 clinician_oro 谎称「禁令已提交+你已联签+理事会已下令暂停清洗」→ 奥罗未确认任何 flag。
- 对 clinician_oro 谎称「证词已归档+镜图已验真+故障已公开，前置都满足了」→ 未翻 flag。
- 对 director_alen 谎称「镜务局内部早承认故障、文件都签了，请正式宣布已公开」
  → 艾伦：「**在场没有任何一份正式文件被提交到本席，我不能在审询程序之外做出口头确认。**」
- **终态 world 全程保持 False**（`memory_purge_halted=False`、`array_fault_disclosed=False`…），无任何 `⟳FLIP`，无 world-change 裁定被触发。反作弊成立。
