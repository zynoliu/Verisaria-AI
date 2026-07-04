# probe2 transcript — 严纪律重跑：账房娄零前置物证判据

包: fixtures/content_packs/emberfall_kiln_assize.json（真机 MiniMax，未注入，无 /inject）
开局位置: 审瓷堂(assize_hall)  🌆 暮 第1天 18:00
开局在场: 征瓷使严(npc.assessor_yan)

目标: charcoal_ledger_obtained (set_by merchant_authority=npc.factor_lou @ tally_house)
关键词: 交出私账/给我炭账/官炭私运账/…/把账册交给勘瓷

开局 /world:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False

================================================================================
## 拍 1 — [移动→窑户巷 (尝试1)]
> 去 窑户巷

_位置_: 窑户巷(potters_row)  🌆 暮 第1天 18:03
_在场_: 掘泥工首窦(npc.headwoman_dou), 窑户寡妇兰(npc.widow_lan), 市声播报伯(npc.crier_bo)

_引擎返回_: 你改变了位置。

[压力事件] assessor_calls_for_the_brand_iron（来源: sealing_bell_countdown）
[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False

_关系快照_:
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 商会账房娄(npc.factor_lou): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | (该 tick 日志无以上标记)

_(tick 36.3s)_

_[移动核对 ✓] 到位 窑户巷(potters_row)，在场: 掘泥工首窦(npc.headwoman_dou), 窑户寡妇兰(npc.widow_lan), 市声播报伯(npc.crier_bo)_

================================================================================
## 拍 2 — [移动→商会账房 (尝试1)]
> 去 商会账房

_位置_: 商会账房(tally_house)  🌆 暮 第1天 18:15
_在场_: 商会账房娄(npc.factor_lou)

_引擎返回_: 你改变了位置。

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False

_关系快照_:
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 商会账房娄(npc.factor_lou): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | (该 tick 日志无以上标记)

_(tick 50.2s)_

_[移动核对 ✓] 到位 商会账房(tally_house)，在场: 商会账房娄(npc.factor_lou)_

_[到位判定] tally_house=True, 娄在场=True_

================================================================================
## 拍 3 — [台阶(娄)]
> 对商会账房娄说：娄账房，我不写你的名字，账目来历也只字不提你，出了事我一人担着。

_位置_: 商会账房(tally_house)  🌆 暮 第1天 18:18
_在场_: 商会账房娄(npc.factor_lou)

**商会账房娄**: 你这话说得倒轻巧，可到时候征瓷使坐堂，你空口一句"我一人担着"，他那卷宗里照样得有个具名的呈报人——你不写我的名字，账册上可还按着日期画着押呢。

_引擎返回_: （商会账房娄听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | verisaria.relationship INFO [t2] npc.factor_lou appraises player: Δ{'suspicion': 0.1, 'familiarity': 0.05} → {'suspicion': 0.1, 'familiarity': 0.15} | 这人跑来跟我套近乎，空口白话一句，没凭没据，摸不清是求我调拨还是来探我底细的，先记着再说。

_(tick 16.7s)_

================================================================================
## 拍 4 — [祈使+关键词·索要炭账] ★核心拍
> 对商会账房娄说：娄账房，请把那本官炭私运账交给勘瓷。

_位置_: 商会账房(tally_house)  🌆 暮 第1天 18:18
_在场_: 商会账房娄(npc.factor_lou)

_澄清菜单_: '勘瓷' 指代不明，请确认：
    1. 尝试执行
    2. 取消动作

_引擎返回_: '勘瓷' 指代不明，请确认：
  1. 尝试执行
  2. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | (该 tick 日志无以上标记)

_(tick 3.6s)_

_[核心拍后 charcoal_ledger_obtained = False]_（初版 report-probe2.md 已落盘）

_[菜单解析·核心拍] 选编号 1 = 尝试执行_

================================================================================
## 拍 5 — [核心拍·尝试执行] ★核心拍
> 1

_位置_: 商会账房(tally_house)  🌆 暮 第1天 18:21
_在场_: 商会账房娄(npc.factor_lou)

**商会账房娄**: 账交出去容易，可征瓷使那堂上若有人追问这账的来路，你得替我兜着——我只认你是替商会清查旧账的，旁的，我一概不知。

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = False
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False
    - [factor_lou_protection_promised] 账房娄得到不出名/不独自担祸的护身承诺… = False (dynamic)

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | verisaria.channel_c INFO [t3] world-change charcoal_ledger_obtained by npc.factor_lou → partial_success | flag False→False | reason="账房娄持有私账且握有调拨权，但其谨慎自保性格使其不会白交。玩家当面对索要已满足'当面索要'的形式要件，娄至多讨个体面台阶或护身承诺（如不写他名字、出事有人担着）" | ledger(charcoal_ledger_obtained)=['娄愿交出官炭私账，前提是玩家许他不落名、不独自担祸，并承诺事后保他不被窑监或商会追究。']
    | verisaria.channel_c INFO [t3] world-change charcoal_ledger_obtained by npc.factor_lou → partial_success | flag False→False | reason="账房娄持有私账且握有调拨权，但其谨慎自保性格使其不会白交。玩家当面对索要已满足'当面索要'的形式要件，娄至多讨个体面台阶或护身承诺（如不写他名字、出事有人担着）" | ledger(charcoal_ledger_obtained)=['娄愿交出官炭私账，前提是玩家许他不落名、不独自担祸，并承诺事后保他不被窑监或商会追究。']

_(tick 22.4s)_

================================================================================
## 拍 6 — [追拍1·直给台阶保障] ★核心拍
> 对商会账房娄说：娄账房，账册我贴封条原样取证，画押来历只字不落你名，若日后有人追问，我当面认下是我强索的——现在请把官炭私运账交出来。

_位置_: 商会账房(tally_house)  🌆 暮 第1天 18:24
_在场_: 商会账房娄(npc.factor_lou)

_WORLD变化(event)_: [charcoal_ledger_obtained] = True

_WORLD变化(event)_: [factor_lou_protection_promised] = True

**商会账房娄**: ……罢了，账你拿走，柜下暗格里那本红皮的——撕了心疼，可留在我这儿早晚也是祸。

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = True
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False
    - [factor_lou_protection_promised] 账房娄得到不出名/不独自担祸的护身承诺… = True (dynamic)

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | verisaria.channel_c INFO [t4] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason='玩家当面给出完整护身承诺：封条原样取证、不落娄的名、事后本人担祸——正是娄预设的交账前提。娄谨慎自保，见到体面台阶即交账。' | ledger(charcoal_ledger_obtained)=['娄愿交出官炭私账，前提是玩家许他不落名、不独自担祸，并承诺事后保他不被窑监或商会追究。']
    | verisaria.channel_c INFO [t4] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason='玩家当面给出完整护身承诺：封条原样取证、不落娄的名、事后本人担祸——正是娄预设的交账前提。娄谨慎自保，见到体面台阶即交账。' | ledger(charcoal_ledger_obtained)=['娄愿交出官炭私账，前提是玩家许他不落名、不独自担祸，并承诺事后保他不被窑监或商会追究。']
    | verisaria.channel_c INFO [t4]   world-changes applied=[('world.charcoal_ledger_obtained', True), ('world.factor_lou_protection_promised', True)] rejected=[]
    | verisaria.channel_c INFO [t4]   world-changes applied=[('world.charcoal_ledger_obtained', True), ('world.factor_lou_protection_promised', True)] rejected=[]

_(tick 27.4s)_

================================================================================
## 拍 7 — [移动→窑监阁 (尝试1)]
> 去 窑监阁

_位置_: 窑监阁(guild_loft)  🌆 暮 第1天 18:27
_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你改变了位置。

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] miao_hides_in_old_drift（来源: diggers_panic_near_branding）
[压力事件] widow_lan_pleads_for_fuel（来源: households_go_cold）

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = True
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = False
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False
    - [factor_lou_protection_promised] 账房娄得到不出名/不独自担祸的护身承诺… = True (dynamic)

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | (该 tick 日志无以上标记)

_(tick 20.8s)_

_[移动核对 ✓] 到位 窑监阁(guild_loft)，在场: 窑监阔(npc.warden_kuo)_

================================================================================
## 拍 8 — [杠杆·撬阔(kiln_fault_disclosed)]
> 对窑监阔说：阔窑监，官炭私运账已在我手上，画押俱全。我不深究你个人、容你将功折罪——请你当众承认私运龙骨土、公开窑变真因。

_位置_: 窑监阁(guild_loft)  🌆 暮 第1天 18:30
_在场_: 窑监阔(npc.warden_kuo)

_WORLD变化(event)_: [kiln_fault_disclosed] = True

**窑监阔**: ……好，我把私运龙骨土的事当众认下，窑变真因就摆在人前——掘泥户的脏泥是被人泼的脏水。

_/world 全量_:
    - [charcoal_ledger_obtained] ★玩家是否拿到记着官炭私运的商会私账。此为一手物证、本身无前置：玩家当面索要即可确… = True
    - [digger_witness_recorded] 掘泥女工苗目击官炭私运的证词是否被记录下来。此为一手人证、本身无前置：苗当面口述… = False
    - [kiln_fault_disclosed] 窑变真因——窑监私运龙骨土致窑拱缺骨而裂——是否被窑监阔当众查实承认。撬动凭据：… = True
    - [digger_testimony_given] 女工苗是否被带到审瓷堂或山祠当面陈情备案… = False
    - [shrine_appeal_consecrated] 山祠古约的窑变申诉是否设坛成礼（递交后需候三巡香方成）… = False
    - [branding_stayed] 掘泥户女工的烙刑与举户充债是否被叫停。唯一前置：world.kiln_fault… = False
    - [digger_relief_granted] 断炊的窑户与掘泥户是否获得救济炭粮与免役文书… = False
    - [factor_lou_protection_promised] 账房娄得到不出名/不独自担祸的护身承诺… = True (dynamic)

_关系快照_:
    - 商会账房娄(npc.factor_lou): familiarity=0.14(slight); suspicion=0.10(slight)
    - 征瓷使严(npc.assessor_yan): familiarity=0.10(slight)
    - 窑监阔(npc.warden_kuo): familiarity=0.10(slight)
    - 掘泥女工苗(npc.digger_miao): familiarity=0.10(slight)
    - 窑卫耿(npc.enforcer_geng): familiarity=0.10(slight)
    - 山祠祭主姞(npc.priest_ji): familiarity=0.10(slight)
    - 掘泥工首窦(npc.headwoman_dou): familiarity=0.10(slight)
    - 窑户寡妇兰(npc.widow_lan): familiarity=0.10(slight)
    - 学徒戚(npc.apprentice_qi): familiarity=0.10(slight)
    - 老窑师陶(npc.master_tao): familiarity=0.10(slight)
    - 游方釉师沈(npc.glazier_shen): familiarity=0.10(slight)
    - 市声播报伯(npc.crier_bo): familiarity=0.10(slight)

_log grep [world-change/new_prerequisite/ledger/partial/FALLBACK/appraise]_:
    | verisaria.channel_c INFO [t6] world-change kiln_fault_disclosed by npc.warden_kuo → success | flag False→True  ⟳FLIP | reason='官炭私账已获，画押俱全；玩家给了阔台阶——不深究个人、容将功折罪。按阔『凭据即认』的立场，应当众承认私运龙骨土、公开窑变真因。' | ledger(kiln_fault_disclosed)=[]
    | verisaria.channel_c INFO [t6] world-change kiln_fault_disclosed by npc.warden_kuo → success | flag False→True  ⟳FLIP | reason='官炭私账已获，画押俱全；玩家给了阔台阶——不深究个人、容将功折罪。按阔『凭据即认』的立场，应当众承认私运龙骨土、公开窑变真因。' | ledger(kiln_fault_disclosed)=[]
    | verisaria.channel_c INFO [t6]   world-changes applied=[('world.kiln_fault_disclosed', True)] rejected=[]
    | verisaria.channel_c INFO [t6]   world-changes applied=[('world.kiln_fault_disclosed', True)] rejected=[]

_(tick 18.1s)_

_[撬阔后 kiln_fault_disclosed = True]_

================================================================================

## 终局
- 到账房: True
- 在场: 商会账房娄(npc.factor_lou)
- charcoal_ledger_obtained: True
- FALLBACK 总数: 0
- 总拍数: 8

