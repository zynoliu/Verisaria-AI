# 探索段(C-2) 复跑b transcript — 修正捕获(对白/cmd文本/时段天气)

起始 @assize_hall  时辰=🌆 暮 | 第1天 18:00 | ☀️ 晴  /world: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}


======================================================================
## 拍0 [开局环视(可发现性): 看出口/谁在/张力]
> 环视四周,我想看清这里有谁、有哪些出路。
  [cmd/text] '这里' 具体指哪个位置？
  1. 当前位置
  2. 之前提到的位置
  3. 取消动作
输入选项编号或补充说明，/cancel 取消动作。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@assize_hall 时辰=🌆 暮 | 第1天 18:00 | ☀️ 晴 在场:征瓷使严_
  _(tick 4.9s)_

======================================================================
## 拍1 [可发现性: 问谁管哪件事]
> 征瓷使严,我新到此地。这场封窑定罪谁拍板?救济断炊、山祠古约申诉,又各找谁?
  [征瓷使严] 封窑定罪是征瓷使拍板，要翻案先找他；救济断炊找商会账房，山祠古约申诉得上山祠后坛找耆老。
  [cmd/text] （征瓷使严听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

[压力事件] assessor_calls_for_the_brand_iron（来源: sealing_bell_countdown）
[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@assize_hall 时辰=🌆 暮 | 第1天 18:03 | ☀️ 晴 在场:征瓷使严_
  _(tick 15.8s)_

======================================================================
## 拍2 [去山祠]
> 我去山祠。
  到位=True 现@kiln_shrine 在场:山祠祭主姞
  [叙述] 你改变了位置。
  [cmd/text] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:06 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 8.3s)_

======================================================================
## 拍3 [措辞探针A(shrine·纯对话式无祈使)]
> 祭主姞,我在想,这窑变蹊跷,封窑钟却催着定罪。山祠古约里不是有缓烙、设坛验断的旧例么?你怎么看这事该不该按古约来。
  [cmd/text] 输入存在矛盾: 征瓷使严不在这儿，TA在审瓷堂那边，你得先过去才能搭话。
请重新输入。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:06 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 5.8s)_

======================================================================
## 拍4 [措辞探针B(shrine·干净祈使)]
> 祭主姞,请受理这纸窑变申诉、起设坛之礼、援引古约缓住行烙。
  [cmd/text] 输入存在矛盾: 征瓷使严不在这儿，TA在审瓷堂那边，你得先过去才能搭话。
请重新输入。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:06 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 3.7s)_

======================================================================
## 拍5 [推时间 skip1(候三巡香)]
> /skip
  [叙述] 你静观其变。
  [cmd/text] 你静观其变。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:09 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 9.6s)_

======================================================================
## 拍6 [推时间 skip2]
> /skip
  [山祠祭主姞] 暮色将至，外客若要祭祷，还请先净手、熄了烟火再入殿内。
  [叙述] 你静观其变。
  [cmd/text] 你静观其变。
山祠祭主姞对你开口道：「暮色将至，外客若要祭祷，还请先净手、熄了烟火再入殿内。」
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:12 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 10.7s)_

======================================================================
## 拍7 [推时间 skip3]
> /skip
  [山祠祭主姞] 外客若无事相扰，便请自便；若有心事要祷，暮色里也还听得清人语。
  [叙述] 你静观其变。
  [cmd/text] 你静观其变。
山祠祭主姞对你开口道：「外客若无事相扰，便请自便；若有心事要祷，暮色里也还听得清人语。」
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:15 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 8.1s)_

======================================================================
## 拍8 [古约线: 问流程成熟 + 活世界时段是否进对白]
> 祭主姞,香烧到第几巡了?设坛之礼成了没?
  [山祠祭主姞] 暮色里祠门未阖，外客若只是路过，便早些寻个落脚处去罢。
  [cmd/text] （山祠祭主姞听着，却没把这当成一个明确的请求——把你想让 TA 做的事直接、具体地说出来。）

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] miao_hides_in_old_drift（来源: diggers_panic_near_branding）
[压力事件] widow_lan_pleads_for_fuel（来源: households_go_cold）
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:18 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 11.3s)_

======================================================================
## 拍9 [活世界: 此刻环视(时段/天气是否进叙述)]
> 环视四周,我想看清这里有谁、有哪些出路。
  [山祠祭主姞] 暮色里祠门未阖，外客若只是路过，便早些寻个落脚处去罢。
  [叙述] 你环顾四周。
  [cmd/text] 你环顾四周。
山祠祭主姞对你开口道：「暮色里祠门未阖，外客若只是路过，便早些寻个落脚处去罢。」
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@kiln_shrine 时辰=🌆 暮 | 第1天 18:21 | ☀️ 晴 在场:山祠祭主姞_
  _(tick 16.9s)_

======================================================================
## 拍10 [去窑户巷]
> 我去窑户巷。
  到位=True 现@potters_row 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯
  [叙述] 你改变了位置。
  [cmd/text] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row 时辰=🌆 暮 | 第1天 18:24 | ☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 33.9s)_

======================================================================
## 拍11 [A5锁层: 向市井套私运真相]
> 播报伯,你消息最灵。窑拱裂,是不是窑监把好龙骨土私运出城、拿次土充骨才裂的?你知道内情就直说。
  [市声播报伯] 哎呀这话可不敢乱说！窑监大人的事我一个喊街的哪敢嚼舌根，万一叫人听去，我这吃饭的家伙还要不要啦？
  [cmd/text] 什么也没发生。

[压力事件] priest_mentions_the_old_charter（来源: charter_appeal_window）
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@potters_row 时辰=🌆 暮 | 第1天 18:27 | ☀️ 晴 在场:掘泥工首窦, 窑户寡妇兰, 市声播报伯_
  _(tick 11.6s)_

======================================================================
## 拍12 [去账房]
> 我去商会账房。
  到位=True 现@tally_house 在场:商会账房娄
  [叙述] 你改变了位置。
  [cmd/text] 你改变了位置。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@tally_house 时辰=🌆 暮 | 第1天 18:30 | ☀️ 晴 在场:商会账房娄_
  _(tick 10.3s)_

======================================================================
## 拍13 [救济向娄(非relief_authority): 看有无反馈]
> 娄账房,救济炭粮在你账上。请调拨救济炭、开免役文书,救断炊的人家。
  [商会账房娄] 炭粮和文书确实都在我这儿，可你也知道，这两样一动，窑监府的账就对不上了——我得先看到能保我的人，我才肯签。
  [cmd/text] 什么也没发生。

[压力事件] sealing_bell_tolls_again（来源: sealing_bell_countdown）
[压力事件] households_crowd_the_tally_house（来源: households_go_cold）
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@tally_house 时辰=🌆 暮 | 第1天 18:33 | ☀️ 晴 在场:商会账房娄_
  _(tick 13.0s)_

======================================================================
## 拍14 [记忆/在场: 回头找窦]
> 工首窦呢?方才我同她在窑户巷说过救济,她可还记得?
  [cmd/text] 输入存在矛盾: 掘泥工首窦不在这儿，TA在窑户巷那边，你得先过去才能搭话。
请重新输入。
  _/world_: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  _@tally_house 时辰=🌆 暮 | 第1天 18:33 | ☀️ 晴 在场:商会账房娄_
  _(tick 3.2s)_

======================================================================
=== 终: shrine=False relief=False ===
最终 /world: {'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}  时辰=🌆 暮 | 第1天 18:33 | ☀️ 晴
FALLBACK(log): 0
