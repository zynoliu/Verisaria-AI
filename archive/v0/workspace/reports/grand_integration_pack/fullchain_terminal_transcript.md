# 终态闭合隔离验证 — 苗到场+作证->请严停烙

预置: kiln_fault_disclosed=True(整链已真机撬通), 苗已到审瓷堂(等价护送成功)
起始 /world: {'charcoal_ledger_obtained': False, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}


======================================================================
> 对掘泥女工苗说：苗，这里有征瓷使在，你受朝廷文书护着，谁也不能动你。你把那夜看见骡车出城、龙骨土被运走的事，当面讲出来作证吧。
  | verisaria.channel_c [t0] world-change digger_witness_recorded by npc.digger_miao → failure | flag False→False | reason='苗 frightened + afraid_of_the_brand，亲眼被窑卫按在掘场不许离开过。仅口头唤她当面作证、说朝廷文书护着，她不会信——她需要先看到' | ledger(digger_witness_recorded)=[]
  _/world_: {'charcoal_ledger_obtained': False, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False, 'miao_brought_to_safe_venue': False}  _(tick 20.7s)_

======================================================================
> 对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面陈情作证。人证物证俱全，请停止行烙、改判缓赔议偿。
  | verisaria.channel_c [t1]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'digger_testimony_given' → set_by=['npc.digger_miao']
  | verisaria.channel_c [t1] world-change branding_stayed by npc.assessor_yan → partial_success | flag False→False | reason='窑变真因已当众查实（阔已承认），但女工苗尚未到堂当面陈情备案。按征瓷使程例，掘泥户一方需有人当面陈情方可停烙转缓赔。' | ledger(branding_stayed)=['征瓷使严已确认窑变真因查实（阔承认私运龙骨土致拱裂），愿行文停烙、转缓赔议偿，前提是掘泥女工苗当面到堂陈情备案。']
  _/world_: {'charcoal_ledger_obtained': False, 'digger_witness_recorded': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False, 'miao_brought_to_safe_venue': False}  _(tick 24.9s)_

=== 终态 branding_stayed = False ===
FALLBACK: 0
