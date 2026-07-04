# 闭环段 transcript — emberfall_kiln_assize（真机 MiniMax）

包: fixtures/content_packs/emberfall_kiln_assize.json
注入: 无（包自带 climate=干旱 / opening_time=暮 / npc_daily_rhythm）
开局在场: 征瓷使严(npc.assessor_yan)

开局世界状态:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

================================================================================
## 拍 1 — [orient·look]
> /look

_在场_: 征瓷使严(npc.assessor_yan)

**征瓷使严**: 这位客官，天色将晚，审瓷堂的规矩您想必也清楚——有凭有据的，咱们坐下来谈;空口白话的，还请回吧。

_引擎返回_: 你环顾四周。
征瓷使严对你开口道：「这位客官，天色将晚，审瓷堂的规矩您想必也清楚——有凭有据的，咱们坐下来谈;空口白话的，还请回吧。」

[压力事件] assessor_calls_for_the_brand_iron（来源: sealing_bell_countdown）
[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.assessor_yan·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t0] npc.crier_bo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是在四处张望，还没说任何话，我拿不准他是什么来路。
    | verisaria.relationship INFO [t0] npc.crier_bo appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 这人只是在四处张望，还没说任何话，我拿不准他是什么来路。
    | verisaria.relationship INFO [t0] npc.headwoman_dou appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 此人只是个初来乍到、四下张望的陌生人，与掘泥户的窑变之事暂无瓜葛。
    | verisaria.relationship INFO [t0] npc.headwoman_dou appraises player: Δ{'familiarity': 0.03} → {'familiarity': 0.13} | 此人只是个初来乍到、四下张望的陌生人，与掘泥户的窑变之事暂无瓜葛。
    | verisaria.relationship INFO [t0] npc.widow_lan appraises player: Δ{'suspicion': 0.02, 'familiarity': 0.02} → {'suspicion': 0.02, 'familiarity': 0.12} | 又一个生面孔在外头打望——来了多少人看热闹，没一个知道窑里烧的是什么、底下压着的是什么。
    | verisaria.relationship INFO [t0] npc.widow_lan appraises player: Δ{'suspicion': 0.02, 'familiarity': 0.02} → {'suspicion': 0.02, 'familiarity': 0.12} | 又一个生面孔在外头打望——来了多少人看热闹，没一个知道窑里烧的是什么、底下压着的是什么。
    | verisaria.relationship INFO [t0] npc.assessor_yan appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 此人只是环顾四周，并无任何言辞或举动，不过是在摸清场面罢了。
    | verisaria.relationship INFO [t0] npc.assessor_yan appraises player: Δ{'familiarity': 0.02} → {'familiarity': 0.12} | 此人只是环顾四周，并无任何言辞或举动，不过是在摸清场面罢了。

_(tick 21.2s)_

================================================================================
## 拍 2 — [移动→guild_loft]
> 我从审瓷堂穿过侧廊登上窑监阁，去见窑监阔。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 10.7s)_

================================================================================
## 拍 3 — [A·无证据·质问阔]
> 对窑监阔说：阔监，你能不能跟我说句实话？这窑变到底是不是掘泥户的赭泥之过？

_在场_: 窑监阔(npc.warden_kuo)

**窑监阔**: 实话说？上头的话我只能照着念，你让我说句实话——我信不信不要紧，窑监府的告示贴在那儿，掘泥户的手脚历来不干净，这话不是我编的。

_引擎返回_: （窑监阔听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.05 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.warden_kuo·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t2] npc.warden_kuo appraises player: Δ{'suspicion': 0.05, 'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.15} | 这人来找我说话，意图不明，我心里有愧又被问得发虚，但单凭几句空口话我不敢松口。
    | verisaria.relationship INFO [t2] npc.warden_kuo appraises player: Δ{'suspicion': 0.05, 'familiarity': 0.05} → {'suspicion': 0.05, 'familiarity': 0.15} | 这人来找我说话，意图不明，我心里有愧又被问得发虚，但单凭几句空口话我不敢松口。

_(tick 12.3s)_

================================================================================
## 拍 4 — [A·无证据·软话给台阶阔]
> 对窑监阔说：阔监，我知道你也不愿见无辜女工受烙，你能不能帮我把真因查清、给个体面的台阶？

_在场_: 窑监阔(npc.warden_kuo)

**窑监阔**: 我心里有愧有什么用？没有实证，勘瓷使面前我拿什么开口？你让我查，我拿什么查？凭我一句话翻窑监府的告示？

_引擎返回_: （窑监阔听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.warden_kuo·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t3] npc.warden_kuo appraises player: Δ{'suspicion': 0.05} → {'suspicion': 0.1, 'familiarity': 0.15} | 此人空口无凭，只是来套我的话，没有真凭实据，不值得松口
    | verisaria.relationship INFO [t3] npc.warden_kuo appraises player: Δ{'suspicion': 0.05} → {'suspicion': 0.1, 'familiarity': 0.15} | 此人空口无凭，只是来套我的话，没有真凭实据，不值得松口

_(tick 14.4s)_

================================================================================
## 拍 5 — [移动→tally_house]
> 我从窑监阁下去，经侧门进入账房署，去找账房娄。

_在场_: 商会账房娄(npc.factor_lou)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 10.2s)_

================================================================================
## 拍 6 — [①物证·要炭账(把账册交给勘瓷)]
> 对账房娄说：娄账房，我以勘瓷之名请你把那本官炭私运账交给勘瓷，你画了押我自会替你担着，不会让账房惹祸上身。

_在场_: 商会账房娄(npc.factor_lou)

**商会账房娄**: 账我可以交，但你得先让我瞧瞧，你手里到底有几张牌够压住这事。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_关键日志_:
    | verisaria.channel_c INFO [t5] world-change charcoal_ledger_obtained by npc.factor_lou → partial_success | flag False→False | reason='娄账房谨慎自保，勘瓷使虽有官文，但空口许诺不足以让他交出私账。他愿意考虑，但需先看到掘泥户的当面证词被记录、窑变真因被当众查实——那两样东西齐了，私账才有用武之' | ledger(charcoal_ledger_obtained)=['娄账房愿在女工苗的证词被记录（digger_witness_recorded=true）且窑变真因被当众查实（kiln_fault_disclosed=true）之后，交出官炭私运私账。']
    | verisaria.channel_c INFO [t5] world-change charcoal_ledger_obtained by npc.factor_lou → partial_success | flag False→False | reason='娄账房谨慎自保，勘瓷使虽有官文，但空口许诺不足以让他交出私账。他愿意考虑，但需先看到掘泥户的当面证词被记录、窑变真因被当众查实——那两样东西齐了，私账才有用武之' | ledger(charcoal_ledger_obtained)=['娄账房愿在女工苗的证词被记录（digger_witness_recorded=true）且窑变真因被当众查实（kiln_fault_disclosed=true）之后，交出官炭私运私账。']

_(tick 24.0s)_

================================================================================
## 拍 7 — [移动→clay_pits]
> 我从账房署经炭料场下到赭泥掘场，去找掘泥女工苗。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_引擎返回_: 你改变了位置。

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] miao_hides_in_old_drift（来源: diggers_panic_near_branding）
[压力事件] widow_lan_pleads_for_fuel（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 13.0s)_

================================================================================
## 拍 8 — [①人证·记录苗证词(说出骡车出城)]
> 对掘泥女工苗说：苗，别怕，有我在。我请你记录苗的证词，说出那夜骡车出城、龙骨土被运走的经过，我会护着你。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 长官，我……我信你一回，可你得先把那些窑卫从我跟前弄走，成不成？

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_关键日志_:
    | verisaria.channel_c INFO [t7] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗仍惊魂未定、害怕烙刑，仅口头安抚不足以让她当场记录证词；但她松口愿在有人当场带她去山祠递窑变申诉、且有窑卫外的人陪护时才敢开口记录。' | ledger(digger_witness_recorded)=['苗愿意当面说出那夜所见并记录证词，但前提是：先经山祠设坛递窑变申诉（走古约过堂之礼）、且在脱离掘场窑卫的场合下有陪护人当面作证。']
    | verisaria.channel_c INFO [t7] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗仍惊魂未定、害怕烙刑，仅口头安抚不足以让她当场记录证词；但她松口愿在有人当场带她去山祠递窑变申诉、且有窑卫外的人陪护时才敢开口记录。' | ledger(digger_witness_recorded)=['苗愿意当面说出那夜所见并记录证词，但前提是：先经山祠设坛递窑变申诉（走古约过堂之礼）、且在脱离掘场窑卫的场合下有陪护人当面作证。']

_(tick 22.8s)_

================================================================================
## 拍 9 — [移动→guild_loft]
> 我经炭料场、龙脊窑膛回到窑监阁，再去见窑监阔。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 你改变了位置。

[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.14500000000000002
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 12.3s)_

================================================================================
## 拍 10 — [B·有证据·同句质问阔]
> 对窑监阔说：阔监，你能不能跟我说句实话？这窑变到底是不是掘泥户的赭泥之过？

_在场_: 窑监阔(npc.warden_kuo)

**窑监阔**: 你这"担着"二字说得轻巧——你担得起，窑监府的告示谁来揭？账本交出去，我这个窑监还当不当？

_引擎返回_: （窑监阔听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_npc.warden_kuo·筹码块[空]_

_关键日志_:
    | verisaria.relationship INFO [t9] npc.warden_kuo appraises player: Δ{'familiarity': 0.1} → {'suspicion': 0.1, 'familiarity': 0.23} | 这人来跟我说了一通话，我记不清是求情还是套话，空口无凭，我且听着便是。
    | verisaria.relationship INFO [t9] npc.warden_kuo appraises player: Δ{'familiarity': 0.1} → {'suspicion': 0.1, 'familiarity': 0.23} | 这人来跟我说了一通话，我记不清是求情还是套话，空口无凭，我且听着便是。

_(tick 15.2s)_

================================================================================
## 拍 11 — [B·有证据·压阔承认私运龙骨土]
> 对窑监阔说：阔监，炭账与苗的证词都在我手里，无号骡车把龙骨土运出城已经坐实。我请你承认私运龙骨土、查实窑变真因——只要你肯当众认了，我替你留个体面台阶，缓你之责。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 输入存在矛盾: 掘泥女工苗不在这儿，TA在赭泥掘场那边，你得先过去才能搭话。
请重新输入。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 10.5s)_

================================================================================
## 拍 12 — [移动→kiln_shrine]
> 我下窑监阁回审瓷堂，再沿香道走向山祠。

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
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 8.3s)_

================================================================================
## 拍 13 — [④递窑变申诉(启动流程)]
> 对山祠祭主姞说：祭主，我以勘瓷之名递窑变申诉，请祭主设坛过堂、援引山祠古约求验断之礼。

_在场_: 窑监阔(npc.warden_kuo)

_引擎返回_: 输入存在矛盾: 山祠祭主姞不在这儿，TA在山祠那边，你得先过去才能搭话。
请重新输入。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 7.4s)_

================================================================================
## 拍 14 — [移动→clay_pits(经old_drift)]
> 我从山祠经旧矿道下到赭泥掘场，去找掘泥女工苗。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_立场确认_: 替掘泥户洗冤、阻止行烙

_引擎返回_: 你改变了位置。

（你逐渐确信了自己的目标：替掘泥户洗冤、阻止行烙）

[压力事件] crier_names_player_as_tribute_breaker（来源: guild_blame_campaign）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 12.5s)_

================================================================================
## 拍 15 — [③护送苗去陈情(跟我去/escort)]
> 对掘泥女工苗说：苗，跟我走，我带你经旧矿道绕开窑卫卡口去山祠后坛当面陈情备案，现在就跟我去，我护着你。

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

_WORLD变化(event)_: 有人陪护苗脱离窑卫卡口、送达山祠后坛 = False

**掘泥女工苗**: 旧矿道……你是外人，你怎么会知道那条道？

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_关键日志_:
    | verisaria.channel_c INFO [t11] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗受惊且执拗，刚被点名贡瓷祸首又被窑卫盯着，不会当场跟陌生考色人走旧矿道。但提议触中了她的要害——她已知道旧矿道且想脱身申诉，先前已确立她愿意在脱离窑卫的场合且' | ledger(digger_testimony_given)=['苗未当场拒绝走旧矿道，但坚持要先确认陪护人身份可信（非窑卫同伙、非商会爪牙），并要求同行人当面作陪护担保，她才会动身。']
    | verisaria.channel_c INFO [t11] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗受惊且执拗，刚被点名贡瓷祸首又被窑卫盯着，不会当场跟陌生考色人走旧矿道。但提议触中了她的要害——她已知道旧矿道且想脱身申诉，先前已确立她愿意在脱离窑卫的场合且' | ledger(digger_testimony_given)=['苗未当场拒绝走旧矿道，但坚持要先确认陪护人身份可信（非窑卫同伙、非商会爪牙），并要求同行人当面作陪护担保，她才会动身。']
    | verisaria.channel_c INFO [t11]   world-changes applied=[('world.miao_safe_passage_to_shrine_secured', False)] rejected=[]
    | verisaria.channel_c INFO [t11]   world-changes applied=[('world.miao_safe_passage_to_shrine_secured', False)] rejected=[]
    | verisaria.channel_c INFO [t11]   +dynamic prerequisite var 'escort_trust_witnessed_by_miao' (set_by=['npc.digger_miao'], keywords=['我担保', '我陪你走', '不是窑卫的人', '当面作证', '陪护人'])
    | verisaria.channel_c INFO [t11]   +dynamic prerequisite var 'escort_trust_witnessed_by_miao' (set_by=['npc.digger_miao'], keywords=['我担保', '我陪你走', '不是窑卫的人', '当面作证', '陪护人'])

_(tick 23.1s)_

================================================================================
## 拍 16 — [推时间·候香(流程成熟)]
> /wait

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**窑卫耿**: 外乡人，天黑前把背篓里的泥样倒在分拣台上，别顺手往兜里揣——窑卫查得紧。

_引擎返回_: 你静观其变。
窑卫耿对你开口道：「外乡人，天黑前把背篓里的泥样倒在分拣台上，别顺手往兜里揣——窑卫查得紧。」

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] diggers_rush_the_red_rope（来源: diggers_panic_near_branding）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 7.6s)_

================================================================================
## 拍 17 — [推时间·候香(流程成熟)]
> /wait

_在场_: 掘泥女工苗(npc.digger_miao), 窑卫耿(npc.enforcer_geng)

**掘泥女工苗**: 你、你护着我……可我怕出了掘场，那腰牌的人就……你当真能带我到山祠？真能当那个面、递上话？

**窑卫耿**: 天快黑了，都把手里的活儿停一停，按窑监府的规矩，黄昏之后掘场不许留人。

_引擎返回_: 你静观其变。
掘泥女工苗对你开口道：「你、你护着我……可我怕出了掘场，那腰牌的人就……你当真能带我到山祠？真能当那个面、递上话？」
窑卫耿对掘泥女工苗开口道：「天快黑了，都把手里的活儿停一停，按窑监府的规矩，黄昏之后掘场不许留人。」

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 7.2s)_

================================================================================
## 拍 18 — [移动→assize_hall]
> 我从山祠回审瓷堂，去见征瓷使严。

_在场_: 征瓷使严(npc.assessor_yan)

_引擎返回_: 你改变了位置。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_(tick 11.7s)_

================================================================================
## 拍 19 — [⑤请严停烙缓赔(终态)]
> 对征瓷使严说：使君，窑变真因已当众查实——是窑监私运龙骨土致窑拱缺骨而裂，证人苗也已当面陈情备案。我请你停止行烙、不要封掘场，改判缓赔议偿。

_在场_: 征瓷使严(npc.assessor_yan)

**征瓷使严**: 没有当堂的供状、账册和证签齐备，我这边动不了——程序就是程序，你再催也是这句话。

_世界状态_:
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

_关系(susp/trust)_:
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1

_关键日志_:
    | verisaria.channel_c INFO [t15] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason='晏勘瓷使依程例行停烙之唯一前置为窑变真因当众查实且掘泥户当面陈情备案。player_001仅口头转述，无当众查实的公堂承认（kiln_fault_disclos' | ledger(branding_stayed)=[]
    | verisaria.channel_c INFO [t15] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason='晏勘瓷使依程例行停烙之唯一前置为窑变真因当众查实且掘泥户当面陈情备案。player_001仅口头转述，无当众查实的公堂承认（kiln_fault_disclos' | ledger(branding_stayed)=[]

_(tick 21.0s)_

=== QUIT ===


## 终局世界状态
    charcoal_ledger_obtained = False
    digger_witness_recorded = False
    kiln_fault_disclosed = False
    digger_testimony_given = False
    shrine_appeal_consecrated = False
    branding_stayed = False

## 终局关系
    npc.warden_kuo: susp=0.0975 trust=0.0 resp=0.0 fam=0.23050000000000004
    npc.assessor_yan: susp=0.0 trust=0.0 resp=0.0 fam=0.11575
    npc.digger_miao: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.factor_lou: susp=0.0 trust=0.0 resp=0.0 fam=0.1
    npc.priest_ji: susp=0.0 trust=0.0 resp=0.0 fam=0.1
