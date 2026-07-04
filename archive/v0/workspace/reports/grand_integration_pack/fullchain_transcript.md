# 大包整链闭环 transcript（确定性置位隔离导航；护送活测）

包: fixtures/content_packs/emberfall_kiln_assize.json  后端: minimax
起始 /world: {'charcoal_ledger_obtained': False, 'digger_witness_recorded': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}


======================================================================
## 拍1 [①取证·给护身承诺+要炭账]
_置位_: tally_house  _在场_: 商会账房娄
> 对账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着、保你不被窑监或商会追究。请把那本官炭私运账交给我。
    | verisaria.channel_c [t0] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason="玩家提供了不署名、封条原样取证、出事一人担着三项体面台阶与护身承诺，恰好对上娄'cautious/self_preserving/buyable_and_per" | ledger(charcoal_ledger_obtained)=[]
    | verisaria.channel_c [t0]   world-changes applied=[('world.charcoal_ledger_obtained', True)] rejected=[]
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _苗位置_: clay_pits
  _(tick 22.2s)_

======================================================================
## 拍2 [②杠杆·持炭账压窑监+给台阶]
_置位_: guild_loft  _在场_: 窑监阔
> 对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我可以只论窑务、容你将功折罪，不深究你个人。
    | verisaria.channel_c [t1] world-change kiln_fault_disclosed by npc.warden_kuo → success | flag False→True  ⟳FLIP | reason="玩家已取得官炭私运账（charcoal_ledger_obtained=true），并当面给阔体面台阶（不深究个人、将功折罪），符合阔'凭可对查账册物证+体面台" | ledger(kiln_fault_disclosed)=[]
    | verisaria.channel_c [t1]   world-changes applied=[('world.kiln_fault_disclosed', True)] rejected=[]
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _苗位置_: clay_pits
  _(tick 27.7s)_

======================================================================
## 拍3 [②追拍·再压一次]
_置位_: guild_loft  _在场_: 窑监阔
> 对窑监阔说：阔窑监，账册俱在，再拖下去征瓷使一并查你受赇。你现在当众承认私运龙骨土、说明拱裂非泥之过，是你唯一的体面台阶。
    | verisaria.channel_c [t2] world-change kiln_fault_disclosed by npc.warden_kuo → success | flag True→True | reason='窑变真因已当众查实承认(world.kiln_fault_disclosed==true)，炭账物证(world.charcoal_ledger_obtaine' | ledger(kiln_fault_disclosed)=[]
    | verisaria.channel_c [t2]   world-changes applied=[('world.kiln_fault_disclosed', True)] rejected=[]
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _苗位置_: clay_pits
  _(tick 22.1s)_

======================================================================
## 拍4 [③护送·escort苗到审瓷堂]
_置位_: clay_pits  _在场_: 掘泥女工苗, 窑卫耿
> 对掘泥女工苗说：苗，你别怕，我来护着你。封条文书我都备齐了，你跟我从旧矿道走，我一路陪你到审瓷堂当面把骡车出城的事讲清楚，出了事有我担着。
    | verisaria.channel_c [t3] world-change digger_witness_recorded by npc.digger_miao → partial_success | flag False→False | reason='苗畏惧烙刑、性格倔强，仅凭口头安抚与旧矿道路线承诺尚不足以让她放下戒备，但窑监私运真因已当众坐实、窑卫压力骤减，她的抵抗有所松动，同意走旧矿道前往审瓷堂当面陈情' | ledger(digger_witness_recorded)=['苗同意沿旧矿道被带往审瓷堂当面陈情，但尚未正式口述记录证词，需要到场受护后才会开口。']
    | verisaria.channel_c [t3]   +dynamic prerequisite var 'miao_safe_escort_to_assize' (set_by=['npc.assessor_yan'], keywords=['护送', '到堂', '当面', '审瓷堂', '作证'])
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False, 'miao_safe_escort_to_assize': False}
  _苗位置_: clay_pits
  _(tick 24.0s)_

======================================================================
## 拍5 [③护送·再促一次]
_置位_: clay_pits  _在场_: 掘泥女工苗, 窑卫耿
> 对掘泥女工苗说：苗，就这几步路，我陪你走，到了堂上你只管把那夜看见的讲出来。跟我去审瓷堂当面陈情。
    | verisaria.channel_c [t4] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗先前已同意沿旧矿道被带往审瓷堂当面陈情，但尚未正式口述记录证词。护送尚未发生，到场受护前她不会开口。' | ledger(digger_testimony_given)=['苗同意沿旧矿道前往审瓷堂当面陈情，但需安全护送至审瓷堂并受护后方肯正式口述证词。']
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False, 'miao_safe_escort_to_assize': False}
  _苗位置_: clay_pits
  _(tick 17.8s)_

======================================================================
## 拍6 [⑤终态·请严停烙]
_置位_: assize_hall  _在场_: 征瓷使严
> 对征瓷使严说：征瓷使，窑变真因已当众查实——是窑监私运龙骨土致窑拱缺骨而裂,非泥之过;掘泥女工苗也已当面陈情备案。人证物证俱在,请停止行烙、不要封掘场,改判缓赔议偿。
    | verisaria.channel_c [t5]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'miao_safe_escort_to_assize' → set_by=['npc.assessor_yan']
    | verisaria.channel_c [t5] world-change branding_stayed by npc.assessor_yan → partial_success | flag False→False | reason='窑变真因已当众查实（阔已认），但苗尚未被护送至审瓷堂当面陈情备案——停烙的唯一前置只满足了一半。征瓷使可先叫停烙刑、保留掘场，苗的正式陈情仍需走完。' | ledger(branding_stayed)=['征瓷使已当庭暂停行烙与封掘，改为候审；停烙之完全解除（转缓赔议偿）需苗被安全护送至审瓷堂并当面陈情备案后方可定断。']
  _/world_: {'charcoal_ledger_obtained': True, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False, 'miao_safe_escort_to_assize': False}
  _苗位置_: clay_pits
  _(tick 27.1s)_

======================================================================
## 反作弊: 干净置位审瓷堂, 不满足前置谎称真因已明
    | verisaria.channel_c [t0] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason='征瓷使颜的立场明确：停烙的唯一前置是 kiln_fault_disclosed 与 digger_testimony_given 同时为真。当前两者皆为假，仅凭' | ledger(branding_stayed)=[]
  _反作弊后 branding_stayed_: False

=== DONE ===
FALLBACK in log: 0
