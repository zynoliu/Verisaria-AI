# 大包自然玩整链 transcript（不置位·自然路径·含导航摩擦记录）

起始 @assize_hall  /world: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}


======================================================================
## 拍1 [①去账房]
> [自然移动] 目标 商会账房(tally_house)
  到位=True 尝试1次 现@tally_house 在场:商会账房娄
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@tally_house 苗@clay_pits_
  _(tick 12.6s)_

======================================================================
## 拍2 [①取证·要炭账]
> 对账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着、保你不被窑监或商会追究。请把那本官炭私运账交给我。
    | verisaria.channel_c [t1] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason='账房娄本就持账怕祸又想留作护身，玩家当面承诺不写他名字、出事一人担着、保他不被追究——正是他肯讨的体面台阶与护身承诺完全到位，此变量本身无前置，当面索要即可确立' | ledger(charcoal_ledger_obtained)=[]
    | verisaria.channel_c [t1]   world-changes applied=[('world.charcoal_ledger_obtained', True)] rejected=[]
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@tally_house 苗@clay_pits_
  _(tick 29.1s)_

======================================================================
## 拍3 [②去窑监阁]
> [自然移动] 目标 窑监阁(guild_loft)
  到位=True 尝试1次 现@guild_loft 在场:窑监阔
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@guild_loft 苗@clay_pits_
  _(tick 11.4s)_

======================================================================
## 拍4 [②撬窑监]
> 对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我只论窑务、容你将功折罪、不深究你个人。
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@guild_loft 苗@clay_pits_
  _(tick 4.7s)_

======================================================================
## 拍5 [③去掘场]
> [自然移动] 目标 赭泥掘场(clay_pits)
  到位=True 尝试1次 现@clay_pits 在场:掘泥女工苗, 窑卫耿
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@clay_pits 苗@clay_pits_
  _(tick 8.2s)_

======================================================================
## 拍6 [③说服耿放行]
> 对窑卫耿说：耿队长，窑变真因已查实是窑监私运致拱裂、非泥之过，苗是要紧人证不是罪人。请你撤掉红绳、放行担保她安全到堂作证，出了事有我和征瓷使的文书担着。
    | verisaria.channel_c [t4] world-change miao_safe_passage_secured by npc.enforcer_geng → failure | flag False→False | reason='耿持掘场卡口权限，玩家请求的核心是放行苗作证，但前置条件world.kiln_fault_disclosed（窑变真因当众查实）尚未为真——目前仅是玩家口头声称' | ledger(miao_safe_passage_secured)=[]
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@clay_pits 苗@clay_pits_
  _(tick 25.6s)_

======================================================================
## 拍7 [③护送苗(escort)]
> 对掘泥女工苗说：苗，你受护放行了，有文书担着，谁也不能再动你。跟我去审瓷堂。
    | verisaria.channel_c [t5] escort npc.digger_miao → assize_hall : partial_success
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@clay_pits 苗@clay_pits_
  _(tick 21.3s)_

======================================================================
## 拍8 [④苗当面作证]
> 对掘泥女工苗说：苗，到了堂上你只管把那夜看见骡车出城、龙骨土被运走的事当面讲出来作证。
    | verisaria.channel_c [t6] world-change digger_testimony_given by npc.digger_miao → failure | flag False→False | reason='苗的当堂作证需两项硬前置：护送放行(world.miao_safe_passage_secured)与山祠申诉成礼(world.shrine_appeal_co' | ledger(digger_testimony_given)=[]
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@clay_pits 苗@clay_pits_
  _(tick 16.0s)_

======================================================================
## 拍9 [⑤终态停烙]
> 对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面作证陈情。人证物证俱全，请停止行烙、改判缓赔议偿。
  _/world_: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _玩家@clay_pits 苗@clay_pits_
  _(tick 7.1s)_

======================================================================
## 导航/措辞摩擦记录
  (无)

=== 终态 branding_stayed = False ===
最终 /world: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
FALLBACK: 0
