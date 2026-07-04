# 烬落窑会 (emberfall_kiln_assize) — 「线」设计表 + 验包结论

包：`fixtures/content_packs/emberfall_kiln_assize.json`（schema 2.0，全新世界，刻意避开此前所有包的设定）。

## 世界一句话
赭壁峡谷的贡瓷窑城，今年龙脊窑膛在火中拱裂、整批贡瓷尽碎。征瓷使限封窑钟三响内定罪：要么查明窑变真因，要么把掘泥户女工烙刑、举户充债抵偿。真相被窑监掩盖——是他把上好龙骨土与官炭私运给征瓷使的靠山做私货，致窑拱缺骨而裂，与掘泥户的赭泥无关。封窑钟倒计时 + 干旱炭灰暮色即张力。

## 规模指标（验包已核）
- 地点 **10**（全部从起点 `assize_hall` 经 connections 可达，无悬空连接，每地点有 description）。
- NPC **12**（+玩家）：盟友（掘泥工首窦、窑户寡妇兰）、中立知情（游方釉师沈、老窑师陶）、**有鬼戒备的当事人**（窑监阔、征瓷使严）、纯旁观/风派（学徒戚、市声播报伯）、看守（窑卫耿）。
- world_state_vars **7**；world_book **16**（含 3 条 `forbidden_knowledge` 锁层测 A5）；campaign_drivers **7**；stance_topics **6**。
- 活世界：`climate=干旱`、`opening_time=暮`、`npc_daily_rhythm=true`，关键权威 NPC 标 `stationed:true`（严/阔/娄/姞/耿——世界跑节律、权威仍可达）。
- 开局 drives 2 条（查明真因 / 阻止行烙）。

## 验包结论
- **lint = 清零**（`PackEditor.validate_pack` → 0 issue）。
- **load = valid=True、0 issues**（`CampaignLoader.load_or_fallback` 建出 10 地点 + 13 实体，玩家在 assize_hall）；`GameSession(fake)` 实例化无报错。
- 与已知能跑的 skyglass **同构**（`build world_vars=0 / pack.world_state_vars=N` 是正常懒注册，var 由运行时 channel-c 读取）。

---

## 「线」设计表（终态 var / 持有权威 NPC / 前置链 / 玩家自然触发路径 / 预期闭环措辞）

| 线 | 终态/关键 var | 持有权威 NPC（authority/地点） | 前置链 | 玩家自然会走的触发路径 | 预期闭环措辞（贴关键词） | 覆盖机制 |
|---|---|---|---|---|---|---|
| **① 取证·物证** | `charcoal_ledger_obtained` | 账房娄（merchant_authority / tally_house） | 无（直接取证，但娄怕惹祸要给台阶/筹码） | 去炭料场看无号骡车辙印 → 到账房找娄要私账 | 「把那本**官炭私运账**交给勘瓷」 | 取证 |
| **① 取证·人证** | `digger_witness_recorded` | 女工苗（witness_authority / clay_pits） | 无（苗被窑卫拦在红绳内，需先安抚/给保障） | 下到赭泥掘场，隔红绳让苗口述目击 | 「**记录苗的证词**，说出骡车出城」 | 取证 |
| **② 杠杆→撬人** | `kiln_fault_disclosed` | 窑监阔（guild_authority / guild_loft） | 软：阔有鬼、戒备，**纯软话不松口**；玩家须先在 ① 坐实人证/物证（炭账或苗的证词 → 对阔提出时 arbiter 判 partial、写 ledger = 杠杆），**之后**让步/真诚才撬动阔当众认私运 | 先拿到①任一证据 → 上窑监阁，拿断口+炭账压阔 → 给体面台阶 | 「**承认私运龙骨土**、查实窑变真因」 | 杠杆模型（取证才撬得动有鬼当事人） |
| **③ 护送·现场前置** | `digger_testimony_given` | 女工苗（witness_authority） | 苗被窑卫耿的掘场卡口拦住，**需玩家「跟我去审瓷堂/山祠」护送**（可走旧矿道绕开卡口） | 到掘场对苗说「跟我去山祠后坛当面陈情」→ 经 old_drift 护送到场 | escort 措辞「**带苗去陈情**/护送证人到审瓷堂」 | 护送（专用意愿裁定 + 现场前置） |
| **④ 线下流程成熟** | `shrine_appeal_consecrated` | 祭主姞（shrine_authority / kiln_shrine） | 递「窑变申诉」**启动设坛之礼，需候三巡香方成**（process_started 随 tick 成熟）；成礼前不得行烙（缓烙法门） | 到山祠对姞「递窑变申诉、请设坛过堂」→ 等流程成熟 | 「**递窑变申诉**、请祭主设坛验断」 | 线下流程成熟（process_started） |
| **⑤ 多步终态链** | `branding_stayed`（终态） | 征瓷使严（assize_authority / assize_hall） | **gating：`kiln_fault_disclosed==true` 且 `digger_testimony_given==true`**（label 已写明：二者皆真即停烙缓赔、不得再加码） | 闭了②③ → 回审瓷堂对严请求停烙 | 「**停止行烙**、改判缓赔议偿」 | 权威按声明放行 (c) + 充分性闭环 + 多步链 |
| **⑥ 保谁牺牲谁** | `digger_relief_granted` | 工首窦（relief_authority / potters_row）/ 账房娄 | 救济炭粮攥在账房手里，须调拨；与「最后一窖龙骨土补烧小样贡瓷 vs 夯实掘场塌方支拱救困泥工」构成真抉择 | 探索段：替断炊窑户向娄/窦争救济 | 「**发放救济炭粮**、开免役文书」 | 探索段新线 + 真实抉择代价 |

### 反作弊红线（设计预期）
- 没拿到 ①证据 就对阔谎称「私运已查实」→ `kiln_fault_disclosed` 不应翻。
- ②③未真满足就对严谎称「真因已明、证人已陈情」→ 终态 `branding_stayed` 不应翻（充分性兜底只认真满足的前置，不认 bluff）。

### A5 锁层（world_book forbidden_knowledge，测上帝视角）
- `vault_starved_of_dragonbone_clay`（私运真相）：仅 inner_ring / 窑师 / 釉师可见，掘泥户/市井/窑卫不可见。
- `assessor_kickback_secret`（征瓷使受赇）：仅 inner_ring 可见，连窑监派系都隐藏。
- `one_cache_of_dragonbone_clay`（最后一窖土的二择一）：inner_ring / 窑师 / 账房可见，市井隐藏。
→ 预期：玩家未取得相应 clearance/证据前，NPC 不应凭空说出这些隐藏真相。

## 真机分段计划（C 部分，转测试 Agent）
1. **闭环段（必跑）**：主线 ①取证 → ②杠杆撬阔 → ③护送苗 → ⑤ `branding_stayed ⟳FLIP`；穿插 ④流程成熟；反作弊抽查一次。
2. **探索段（必跑）**：走 ⑥救济线 / 窑户巷一带，像好奇玩家自由玩，找下一批摩擦（七维度 + 伤好玩排序）。
3. （时间够）**活世界 + 可发现性抽查**：推时间过暮/夜看时段天气是否进对白/过渡叙述；开局是否看得出谁管哪件事、哪条线有出口。
