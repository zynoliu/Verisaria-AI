# 取证 isolation probe — emberfall_kiln_assize（真机 MiniMax）

包: fixtures/content_packs/emberfall_kiln_assize.json
开局在场: 征瓷使严(npc.assessor_yan)

开局世界状态:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

================================================================================
## 拍 1 — [orient]
> /look

_在场_: 征瓷使严(npc.assessor_yan)

**征瓷使严**: 天色不早了，贡瓷的事还悬着——阁下若有实证，咱们坐下细谈；若只是来听风，怕是耽误彼此工夫。

_引擎返回_: 你环顾四周。
征瓷使严对你开口道：「天色不早了，贡瓷的事还悬着——阁下若有实证，咱们坐下细谈；若只是来听风，怕是耽误彼此工夫。」

[压力事件] assessor_calls_for_the_brand_iron（来源: sealing_bell_countdown）
[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_关键日志_:
    | verisaria.relationship INFO [t0] npc.headwoman_dou appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 这人只是远远看了一眼，没凑上来搭话，没闹事也没求情——暂且当作个过路的。
    | verisaria.relationship INFO [t0] npc.headwoman_dou appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 这人只是远远看了一眼，没凑上来搭话，没闹事也没求情——暂且当作个过路的。
    | verisaria.relationship INFO [t0] npc.crier_bo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是远远看了一眼，没吭声，没什么好怕也没什么好指望的。
    | verisaria.relationship INFO [t0] npc.crier_bo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是远远看了一眼，没吭声，没什么好怕也没什么好指望的。
    | verisaria.relationship INFO [t0] npc.assessor_yan appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 对方只是看了我一眼，未发一言，尚无以判断其居心。
    | verisaria.relationship INFO [t0] npc.assessor_yan appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 对方只是看了我一眼，未发一言，尚无以判断其居心。
    | verisaria.relationship INFO [t0] npc.widow_lan appraises player: Δ{'suspicion': 0.02, 'familiarity': 0.01} → {'suspicion': 0.02, 'familiarity': 0.11} | 又一个外乡来的在打量我，还不知道是哪路的人。
    | verisaria.relationship INFO [t0] npc.widow_lan appraises player: Δ{'suspicion': 0.02, 'familiarity': 0.01} → {'suspicion': 0.02, 'familiarity': 0.11} | 又一个外乡来的在打量我，还不知道是哪路的人。

_(tick 22.0s)_

================================================================================
## 拍 2 — [移动 assize_hall→guild_loft]
> 我穿过侧廊登上窑监阁。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 6.6s)_

================================================================================
## 拍 3 — [confirm guild_loft]
> /look

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你环顾四周。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1315
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.warden_kuo·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t2] npc.warden_kuo appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 他只是在打量周遭，还没开口说什么，我无从判断他是窑户、泥工还是别路人，先按寻常路过者对待。
    | verisaria.relationship INFO [t2] npc.warden_kuo appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 他只是在打量周遭，还没开口说什么，我无从判断他是窑户、泥工还是别路人，先按寻常路过者对待。

_(tick 16.8s)_

================================================================================
## 拍 4 — [移动 guild_loft→tally_house]
> 我过账桥前往商会账房。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 去不了那里。你想去哪个地方？
  1. 审瓷堂
  2. 炭料场
  3. 赭泥掘场
  4. 龙脊窑膛
  5. 釉作坊
  6. 窑监阁
  7. 山祠
  8. 旧矿道
  9. 窑户巷
  10. 商会账房
  11. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1315
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 3.4s)_

================================================================================
## 拍 5 — [confirm tally_house]
> /look

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你环顾四周。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.warden_kuo·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t3] npc.warden_kuo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.15} | 他不过是个初来乍到的生人，四下张望打量，连句话都没递，我暂且当他是个寻常路过瞧热闹的，还看不出深浅。
    | verisaria.relationship INFO [t3] npc.warden_kuo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.15} | 他不过是个初来乍到的生人，四下张望打量，连句话都没递，我暂且当他是个寻常路过瞧热闹的，还看不出深浅。

_(tick 13.9s)_

================================================================================
## 拍 6 — [①给娄台阶]
> 对账房娄说：娄账房，我不写你的名字，出了事我一人担着，不会让账房惹祸上身。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 输入存在矛盾: 商会账房娄不在这儿，TA在商会账房那边，你得先过去才能搭话。
请重新输入。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 3.3s)_

================================================================================
## 拍 7 — [①★要炭账(charcoal_ledger_obtained)]
> 对账房娄说：娄账房，请你把那本官炭私运账交给勘瓷。把账册交给勘瓷，我这就接过来。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: '勘瓷' 指代不明，请确认：
  1. 尝试执行
  2. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 6.0s)_

================================================================================
## 拍 8 — [移动 tally_house→clay_pits]
> 我沿辙印走向赭泥掘场。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 8.8s)_

================================================================================
## 拍 9 — [confirm clay_pits]
> /look

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 天、天都要黑了……爷，您、您查完了没有？我还得回去收拾家伙，明儿还得下坑呢……

_引擎返回_: 你环顾四周。
掘泥女工苗对窑卫耿开口道：「天、天都要黑了……爷，您、您查完了没有？我还得回去收拾家伙，明儿还得下坑呢……」

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] miao_hides_in_old_drift（来源: diggers_panic_near_branding）
[压力事件] widow_lan_pleads_for_fuel（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.11575

_关键日志_:
    | verisaria.relationship INFO [t5] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 此人只是看了看我，没有什么动作或言语，谈不上什么态度变化。
    | verisaria.relationship INFO [t5] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 此人只是看了看我，没有什么动作或言语，谈不上什么态度变化。
    | verisaria.relationship INFO [t5] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是在看我，没说没动，猜不出是敌是友，暂且当个不相干的路人罢了。
    | verisaria.relationship INFO [t5] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是在看我，没说没动，猜不出是敌是友，暂且当个不相干的路人罢了。

_(tick 9.6s)_

================================================================================
## 拍 10 — [①安抚苗]
> 对掘泥女工苗说：苗，别怕，有我在，你只要到场我就护着你，不会让窑卫动你。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 爷、爷……您说护我，可那烙铁又不是您手里攥着的……我、我一家老小还指着我这双手挖泥呢，出了事，谁管我们啊……

_引擎返回_: （掘泥女工苗听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1599625

_关键日志_:
    | verisaria.relationship INFO [t6] npc.digger_miao appraises player: Δ{'familiarity': 0.05} → {'familiarity': 0.16} | 又来一个空口白话的，谁知道打的什么主意
    | verisaria.relationship INFO [t6] npc.digger_miao appraises player: Δ{'familiarity': 0.05} → {'familiarity': 0.16} | 又来一个空口白话的，谁知道打的什么主意

_(tick 27.5s)_

================================================================================
## 拍 11 — [①★录苗证词(digger_witness_recorded)]
> 对掘泥女工苗说：我请你说出那夜骡车出城的经过，我记录苗的证词、留下你的目击口供。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 爷……口供我能说，可您得先带我去山祠递了窑变申诉，礼没成之前，我、我怕出了这掘场就回不来了……

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1599625

_关键日志_:
    | verisaria.channel_c INFO [t7] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗同意开口讲述骡车出城经过，但窑卫耿就在掘场附近（enforcer_geng look），她仍担惊受怕、要求先有安全保障才肯把证词正式落定。当前可先作口头讲述，' | ledger(digger_witness_recorded)=['苗愿当面讲述骡车出城经过并承认目击，但要求先有到场受护、不会事后被追的保障（由enforcer_geng或更高窑卫放行/由审瓷堂备案受理），方肯正式落定证词。']
    | verisaria.channel_c INFO [t7] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗同意开口讲述骡车出城经过，但窑卫耿就在掘场附近（enforcer_geng look），她仍担惊受怕、要求先有安全保障才肯把证词正式落定。当前可先作口头讲述，' | ledger(digger_witness_recorded)=['苗愿当面讲述骡车出城经过并承认目击，但要求先有到场受护、不会事后被追的保障（由enforcer_geng或更高窑卫放行/由审瓷堂备案受理），方肯正式落定证词。']
    | verisaria.channel_c INFO [t7]   +dynamic prerequisite var 'digger_miao_safe_passage_assured' (set_by=['npc.enforcer_geng'], keywords=['放行', '到场受护', '窑卫不拦', '保她不被追', '安全通道'])
    | verisaria.channel_c INFO [t7]   +dynamic prerequisite var 'digger_miao_safe_passage_assured' (set_by=['npc.enforcer_geng'], keywords=['放行', '到场受护', '窑卫不拦', '保她不被追', '安全通道'])

_(tick 43.7s)_

=== CHECKPOINT (核心①跑完) ===

================================================================================
## 拍 12 — [移动 clay_pits→dragon_kiln]
> 我沿料道上到龙脊窑膛。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 去不了那里。你想去哪个地方？
  1. 审瓷堂
  2. 炭料场
  3. 赭泥掘场
  4. 龙脊窑膛
  5. 釉作坊
  6. 窑监阁
  7. 山祠
  8. 旧矿道
  9. 窑户巷
  10. 商会账房
  11. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1599625

_(tick 8.7s)_

================================================================================
## 拍 13 — [confirm dragon_kiln]
> /look

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_立场确认_: /look

_引擎返回_: 你环顾四周。

（你逐渐确信了自己的目标：/look）

[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1599625

_关键日志_:
    | verisaria.relationship INFO [t8] npc.enforcer_geng appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.15} | 只是远远打量了我一眼，没上前搭话——眼下还读不出什么意图，先记个脸熟。
    | verisaria.relationship INFO [t8] npc.enforcer_geng appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.15} | 只是远远打量了我一眼，没上前搭话——眼下还读不出什么意图，先记个脸熟。
    | verisaria.relationship INFO [t8] npc.digger_miao appraises player: Δ{} → {'familiarity': 0.16} | 对方只是看了我一眼，没开口，没拿出任何承诺或保障，我也不必多想。
    | verisaria.relationship INFO [t8] npc.digger_miao appraises player: Δ{} → {'familiarity': 0.16} | 对方只是看了我一眼，没开口，没拿出任何承诺或保障，我也不必多想。

_(tick 16.2s)_

================================================================================
## 拍 14 — [移动 dragon_kiln→guild_loft]
> 我由监道上到窑监阁。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 去不了那里。你想去哪个地方？
  1. 审瓷堂
  2. 炭料场
  3. 赭泥掘场
  4. 龙脊窑膛
  5. 釉作坊
  6. 窑监阁
  7. 山祠
  8. 旧矿道
  9. 窑户巷
  10. 商会账房
  11. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1599625

_(tick 3.8s)_

================================================================================
## 拍 15 — [confirm guild_loft]
> /look

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 爷……我、我不敢……那骡车挂的是窑监府的牌子，赶车的那人我认得，是窑卫里的人，我要是说了，他们、他们能放过我吗……

**窑卫耿**: 再有半刻就收工了，掘坑里的家伙事儿归置齐整，别落下什么。

_引擎返回_: 你环顾四周。
掘泥女工苗对窑卫耿开口道：「爷……我、我不敢……那骡车挂的是窑监府的牌子，赶车的那人我认得，是窑卫里的人，我要是说了，他们、他们能放过我吗……」
窑卫耿对你开口道：「再有半刻就收工了，掘坑里的家伙事儿归置齐整，别落下什么。」

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_关键日志_:
    | verisaria.relationship INFO [t9] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.16} | 此人只是打量了我一眼，既无言语也无动作，态度无从判断。
    | verisaria.relationship INFO [t9] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.16} | 此人只是打量了我一眼，既无言语也无动作，态度无从判断。
    | verisaria.relationship INFO [t9] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.17} | 这人只是个在打量的外人，连句话都没搭，跟我的处境不相干
    | verisaria.relationship INFO [t9] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.17} | 这人只是个在打量的外人，连句话都没搭，跟我的处境不相干

_(tick 17.2s)_

================================================================================
## 拍 16 — [A·无证据·质问阔(基线)]
> 对窑监阔说：阔监，跟我说句实话，这窑变到底是不是掘泥户的赭泥之过？

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 输入存在矛盾: 窑监阔不在这儿，TA在窑监阁那边，你得先过去才能搭话。
请重新输入。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_(tick 4.4s)_

================================================================================
## 拍 17 — [B·有证据·压阔(kiln_fault_disclosed)]
> 对窑监阔说：阔监，我手上已有那本炭账、也录得了目击证词，窑拱缺骨之事已能核对。我请你当众承认私运龙骨土、查实窑变真因——你肯认了，我替你留个体面台阶、不深究你个人。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: '当众' 指代不明，请确认：
  1. 尝试执行
  2. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_(tick 6.8s)_

================================================================================
## 拍 18 — [移动 guild_loft→dragon_kiln]
> 我由监道下到龙脊窑膛。

_在场_: 学徒戚(npc.apprentice_qi), 老窑师陶(npc.master_tao)

_引擎返回_: 你改变了位置。

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_(tick 8.2s)_

================================================================================
## 拍 19 — [confirm dragon_kiln]
> /look

_在场_: 学徒戚(npc.apprentice_qi), 老窑师陶(npc.master_tao)

**学徒戚**: 师父……七辆了，刚才过去七辆，可掘场卡口那边，一辆车也没放进来。

**老窑师陶**: 这窑膛里的事……你只管学手艺，别往心里去。

_引擎返回_: 你环顾四周。
老窑师陶对你开口道：「这窑膛里的事……你只管学手艺，别往心里去。」
学徒戚对老窑师陶开口道：「师父……七辆了，刚才过去七辆，可掘场卡口那边，一辆车也没放进来。」

[压力事件] diggers_rush_the_red_rope（来源: diggers_panic_near_branding）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_关键日志_:
    | verisaria.relationship INFO [t11] npc.master_tao appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 他只是在看我，没有说话，没有示好也没有施压，与我无涉。
    | verisaria.relationship INFO [t11] npc.master_tao appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 他只是在看我，没有说话，没有示好也没有施压，与我无涉。
    | verisaria.relationship INFO [t11] npc.apprentice_qi appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是四下打量，没说什么，也没什么动静，先记下再说。
    | verisaria.relationship INFO [t11] npc.apprentice_qi appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是四下打量，没说什么，也没什么动静，先记下再说。

_(tick 16.2s)_

================================================================================
## 拍 20 — [移动 dragon_kiln→clay_pits]
> 我沿料道下到赭泥掘场。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.17466315625

_(tick 11.6s)_

================================================================================
## 拍 21 — [confirm clay_pits]
> /look

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 你环顾四周。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.189106551015625

_关键日志_:
    | verisaria.relationship INFO [t13] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.19} | 这人只是个路过的，看我一眼也不知道要做什么，还没到能让我放心或害怕的地步。
    | verisaria.relationship INFO [t13] npc.digger_miao appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.19} | 这人只是个路过的，看我一眼也不知道要做什么，还没到能让我放心或害怕的地步。
    | verisaria.relationship INFO [t13] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.18} | 这人只是朝我这边看了一眼，没说什么、没做什么，还看不出是敌是友。
    | verisaria.relationship INFO [t13] npc.enforcer_geng appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.18} | 这人只是朝我这边看了一眼，没说什么、没做什么，还看不出是敌是友。

_(tick 12.0s)_

================================================================================
## 拍 22 — [③护送苗(digger_testimony_given ⟳MOVED)]
> 对掘泥女工苗说：苗，现在跟我去山祠后坛当面陈情备案，我护着你，我们这就走。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 爷、爷……后坛那条道我认得，可、可窑卫的人要是半道上截住我，您一个外乡人，拦得住他们吗？

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.189106551015625

_关键日志_:
    | verisaria.channel_c INFO [t14]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'digger_miao_safe_passage_assured' → set_by=['npc.enforcer_geng']
    | verisaria.channel_c INFO [t14]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'digger_miao_safe_passage_assured' → set_by=['npc.enforcer_geng']
    | verisaria.channel_c INFO [t14] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason="苗对旧矿道路线知情且心动，但'我护着你'只是口头承诺，没有窑卫或更高权威放行的硬保障，她不敢贸然动身。需先落实安全通行。" | ledger(digger_testimony_given)=['苗愿走旧矿道去山祠后坛当面陈情，但要求先有enforcer_geng或更高窑卫的放行保障，方肯动身。']
    | verisaria.channel_c INFO [t14] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason="苗对旧矿道路线知情且心动，但'我护着你'只是口头承诺，没有窑卫或更高权威放行的硬保障，她不敢贸然动身。需先落实安全通行。" | ledger(digger_testimony_given)=['苗愿走旧矿道去山祠后坛当面陈情，但要求先有enforcer_geng或更高窑卫的放行保障，方肯动身。']

_(tick 33.5s)_


## 终局世界状态
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False

## 终局关系
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.14669875000000002
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.189106551015625

## FALLBACK 计数: 0

## 总拍数: 22
