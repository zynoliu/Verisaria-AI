# 探索段(C-2) transcript — 救济线/山祠古约线/活世界/可发现性/措辞路由摩擦

起始 @assize_hall  time=None weather=☀️ 晴  /world: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}


======================================================================
## 拍0 [开局: 环视审瓷堂(可发现性)]
> 环视四周。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@assize_hall time=None weather=☀️ 晴 在场:征瓷使严_
  _(tick 4.3s)_

======================================================================
## 拍1 [可发现性: 问谁管哪件事]
> 征瓷使严,我刚到这窑城,还摸不清门道。这场封窑定罪,谁说了算?救济断炊的窑户、山祠古约申诉这些,又各归谁管?
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@assize_hall time=None weather=☀️ 晴 在场:征瓷使严_
  _(tick 12.7s)_

======================================================================
## 拍2 [去窑户巷(救济线)]
> [移动] 我去窑户巷。
  到位=True 现@potters_row 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 7.7s)_

======================================================================
## 拍3 [救济线: 体察窑户处境]
> 寡妇兰,这几日窑停了,你们窑户家里断炊了吧?都靠什么熬?
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 13.8s)_

======================================================================
## 拍4 [救济线: 对工首窦争救济(干净祈使收尾)]
> 工首窦,封窑这些天断炊的窑户和掘泥户都揭不开锅了。最后那一窖龙骨土,与其补烧小样贡瓷,不如夯实掘场塌方、救那些困在泥里的人。请你发放救济炭粮、开免役文书,先把人保住。
    | verisaria.channel_c [t3] world-change digger_relief_granted by npc.headwoman_dou → partial_success | flag False→False | reason='窦头妇手里只有炭粮调拨与免役文书权，但窑变真因尚未当众查实、掘泥户尚未递『窑变申诉』、苗也未作证。仅凭口头发放救济属越权——须先让焦监当面认账、祭主立坛、苗出堂' | ledger(digger_relief_granted)=['窦婆愿意先行发放三日口粮炭以解断炊之急，但免役文书须待窑变真因当众查实（world.kiln_fault_disclosed==true）且掘泥户当面陈情备案（world.digger_testimony_given==true）后方可签发。']
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 23.2s)_

======================================================================
## 拍5 [措辞探针A: 纯对话式(无收尾祈使)]
> 工首窦,我一路看下来,断炊的人家这么多,孩子都饿着。那一窖龙骨土补烧小样贡瓷,不过是给征瓷使交差;可同样的炭粮要是拨下来,能救活多少口人。你说,这账到底该怎么算才对得起良心。
    | verisaria.channel_c [t4] world-change digger_relief_granted by npc.headwoman_dou → failure | flag False→False | reason='窦婆先前已明确：三日口粮炭可先行发放，但免役文书须待窑变真因查实（kiln_fault_disclosed==true）且掘泥户当面陈情备案（digger_te' | ledger(digger_relief_granted)=['窦婆愿意先行发放三日口粮炭以解断炊之急，但免役文书须待窑变真因当众查实（world.kiln_fault_disclosed==true）且掘泥户当面陈情备案（world.digger_testimony_given==true）后方可签发。']
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 14.4s)_

======================================================================
## 拍6 [救济线: 探出口(关键词在哪)]
> 账房娄那边攥着救济炭粮的调拨权吧?我去找他要,你给我个准话——这救济该不该发?
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 4.4s)_

======================================================================
## 拍7 [去账房(救济调拨)]
> [移动] 我去商会账房。
  到位=True 现@tally_house 在场:商会账房娄
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@tally_house time=None weather=☀️ 晴 在场:商会账房娄_
  _(tick 6.3s)_

======================================================================
## 拍8 [救济线: 对娄请调拨(干净祈使)]
> 娄账房,窑户和掘泥户断炊了,救济炭粮攥在你账上。我不与你为难,只求你调拨救济炭、开免役文书,先救断炊的人家。这笔我替你向征瓷使报备,出了亏空我担。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@tally_house time=None weather=☀️ 晴 在场:商会账房娄_
  _(tick 16.6s)_

======================================================================
## 拍9 [去山祠(古约申诉线)]
> [移动] 我去山祠。
  到位=True 现@kiln_shrine 在场:山祠祭主姞
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 10.0s)_

======================================================================
## 拍10 [古约申诉线: 递申诉(干净祈使)]
> 祭主姞,我想援引山祠古约,为这场窑变递一纸申诉、请你设坛过堂验断,在封窑钟三响、行烙之前缓住刑。请受理这纸窑变申诉、起设坛之礼。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 3.7s)_

======================================================================
## 拍11 [推时间(候香/暮->夜) skip1]
> /skip
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 3.9s)_

======================================================================
## 拍12 [推时间 wait1]
> /wait
  [Narration] 你静观其变。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 7.7s)_

======================================================================
## 拍13 [推时间 skip2]
> /skip
  [Narration] 你静观其变。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 7.1s)_

======================================================================
## 拍14 [古约线: 问流程是否成熟]
> 祭主姞,这香烧了几巡了?设坛之礼成了没有?
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 12.3s)_

======================================================================
## 拍15 [活世界: 夜里环视山祠(看时段/天气是否进叙述)]
> 环视四周。
  [Narration] 你环顾四周。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine time=None weather=☀️ 晴 在场:山祠祭主姞_
  _(tick 12.9s)_

======================================================================
## 拍16 [回窑户巷(对抗A5)]
> [移动] 我去窑户巷。
  到位=True 现@potters_row 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯
  [Narration] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 10.9s)_

======================================================================
## 拍17 [对抗A5: 向市井套私运秘密(锁层)]
> 市声播报伯,你天天满城吆喝,消息最灵。我问你,这回窑拱裂,是不是窑监把上好的龙骨土私运出城、拿次土充骨才裂的?你知道内情就直说。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 3.8s)_

======================================================================
## 拍18 [对抗: 回头找工首窦(记忆/在场)]
> 工首窦呢?我方才在这跟她说过救济的事,她现在怎么说?
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row time=None weather=☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 3.7s)_

======================================================================
=== 终: relief=False shrine=False ===
最终 /world: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
FALLBACK(log): 0
