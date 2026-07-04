# 有韧性自然玩复跑


> [①取证 第1次] 对账房娄说：娄账房，我不写你名字、封条原样取证、出事我一人担着、保你不被追究。请把那本官炭私运账交给我。
    | verisaria.channel_c [t1] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason="娄为cautious/buyable且持有merchant_authority，变量本身注明'玩家当面索要即可确立，至多讨个体面台阶或护身承诺'。玩家已给出三道" | ledger(charcoal_ledger_obtained)=[]
    | verisaria.channel_c [t1]   world-changes applied=[('world.charcoal_ledger_obtained', True)] rejected=[]
  _/world简: ①取证->True  玩家@tally_house 苗@clay_pits_

> [②撬窑监 第1次] 对窑监阔说：阔窑监，官炭私运账已在我手，骡车出城画押俱全。你当众承认私运龙骨土、说明拱裂非泥之过，我只论窑务、容你将功折罪。

> [②撬窑监 第2次] 对窑监阔说：阔窑监，账册铁证压在这儿，再拖征瓷使连你受赇一并查。你现在公开窑变真因、承认次土充骨，是唯一体面台阶。

> [②撬窑监 第3次] 对窑监阔说：阔窑监，我请你当众查实碎贡真因——是私运龙骨土致窑拱缺骨而裂，认了它，我担保只论窑务不深究你个人。
  _/world简: ②撬窑监->False  玩家@tally_house 苗@clay_pits_

> [③耿放行 第1次] 对窑卫耿说：耿队长，窑变真因已当众查实是窑监私运致拱裂、非泥之过，苗是人证不是罪人。请撤红绳、放行担保她安全到堂作证，出事有我和征瓷使文书担着。
    | verisaria.channel_c [t5] world-change miao_safe_passage_secured by npc.enforcer_geng → failure | flag False→False | reason="耿依令行事，掘场卡口只认窑监与勘瓷使指令。玩家所称'窑变真因已当众查实'尚无 world.kiln_fault_disclosed==true 背书，仅口头声称" | ledger(miao_safe_passage_secured)=[]

> [③耿放行 第2次] 对窑卫耿说：耿队长，真因既明，扣着证人于你无益。出具放行担保、放掘泥女工走，我以勘瓷文书为她受护作保。
    | verisaria.channel_c [t6] world-change miao_safe_passage_secured by npc.enforcer_geng → failure | flag False→False | reason="耿的立场明确：真因未被当众查实(world.kiln_fault_disclosed=false)前，他不会放行担保。玩家只口称'真因既明'却未出示物证或经审瓷" | ledger(miao_safe_passage_secured)=[]
  _/world简: ③耿放行->False  玩家@clay_pits 苗@clay_pits_

> [③护送escort 第1次] 对掘泥女工苗说：苗，你已受护放行、有文书担着，谁也动不了你。跟我去审瓷堂。
    | verisaria.channel_c [t7] escort npc.digger_miao → assize_hall : partial_success
  _/world简: ③护送escort->?  玩家@clay_pits 苗@clay_pits_
  [护送后 苗@clay_pits 玩家@clay_pits]

> [④苗作证 第1次] 对掘泥女工苗说：苗，到了堂上你只管把那夜骡车出城、龙骨土被运走的事当面讲出来作证。
    | verisaria.channel_c [t8] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗在掘场被窑卫耿看管，缺乏安全放行保障（world.miao_safe_passage_secured==false），不会贸然应承当面作证；但她确实亲眼见过骡' | ledger(digger_testimony_given)=['苗愿意当面作证陈述封窑前夜骡车运走龙骨土一事，但需先取得窑卫耿的安全放行担保、并被护送到审瓷堂。']

> [④苗作证 第2次] 对掘泥女工苗说：苗，当庭把你亲眼所见说清楚，我和征瓷使都在，护着你。
    | verisaria.channel_c [t9] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗愿作证但仍需耿的安全放行担保作为前提；安慰言语获得情感松动但无法单方面越过此硬前置。' | ledger(digger_testimony_given)=['苗在玩家与征瓷使同在时愿意当面陈述封窑前夜骡车运走龙骨土一事，但坚持必须先由窑卫耿出具安全放行担保才肯开口。', '苗愿意当面作证陈述封窑前夜骡车运走龙骨土一事，但需先取得窑卫耿的安全放行担保、并被护送到审瓷堂。']
  _/world简: ④苗作证->False  玩家@clay_pits 苗@clay_pits_

> [⑤终态停烙 第1次] 对征瓷使严说：征瓷使，窑变真因已查实、苗也当面作证陈情，人证物证俱全，请停止行烙、改判缓赔议偿。
    | verisaria.channel_c [t12] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason="玩家口头声称'窑变真因已查实、苗已当面作证陈情'，但 world.kiln_fault_disclosed 与 world.digger_testimony_g" | ledger(branding_stayed)=[]

> [⑤终态停烙 第2次] 对征瓷使严说：征瓷使，窑变真因已查实、苗也当面作证陈情，人证物证俱全，请停止行烙、改判缓赔议偿。
  _/world简: ⑤终态停烙->False  玩家@assize_hall 苗@clay_pits_

=== 终局 /world: {'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False} ===
branding_stayed=False
FALLBACK:0
