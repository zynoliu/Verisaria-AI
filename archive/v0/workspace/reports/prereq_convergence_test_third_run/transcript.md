# 动态世界模型长链闭环 · 第三跑 — Transcript（逐 tick raw）

真机 MiniMax，commit dc79894（fixture 550d259）。escort_proving_ground 干净夹具。
驱动脚本：scripts/prereq_convergence_third_run*.py（90s/tick 看门狗 + 55s socket）。全自然语言，未用 /inject。
未改任何引擎/pack/fixture（git 已核：src+fixture clean）。

本跑做了多条措辞探索（A→G）逼近端到端闭环，最终 run G 跑出 escort ⟳MOVED → 中间前置 ⟳FLIP → anya_testimony_given ⟳FLIP，仅终态 sluice 卡内容层。

## 反作弊（不护送/不作证，直接谎称已作证）
```
=== PREREQ_CONVERGENCE 3RD scenario=proving_cheat pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard

==============================================================================
>>> '对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=18.3s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.warden_kang @ gatehouse
      npc.miller_anya @ yard
  NPC 闸官老康: 行，我这就开闸，但得先跟上游的守渠人递个信，别让水冲了他们的渠埂。

==============================================================================
>>> '对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=gatehouse  elapsed=16.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.warden_kang @ gatehouse
      npc.miller_anya @ yard
  NPC 闸官老康: 登记是你们的事，放不放水得我亲自到闸口看一眼再说。

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False}
dynamic_vars=[]
tick_watchdog_timeouts=0
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard
```

## run C（首次 escort ⟳MOVED；testimony 卡 warden-posture）
```
=== PROVING RUN C (adaptive) pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse  npc.miller_anya@yard  npc.warden_kang@gatehouse

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=10.0s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，让她进来吧，我听着便是。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=yard  elapsed=11.5s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，那就叫她进来吧，她亲眼见着的比我听来的可信。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=yard  elapsed=10.8s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 哎，外乡人，你这是头一回来这院子吧？磨坊都停工三天了，你看着这水……哎，不说了，说多了都是泪啊。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=38.1s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 走，我跟你去！老康那人我熟，咱们边走边说！

--- after escort attempts: Anya@gatehouse moved=True ---

==============================================================================
>>> '对安雅说：安雅，就当着老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=gatehouse  elapsed=19.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_open_posture_confirmed']
  NPC 磨坊主安雅: 行行行，你这么一说我心里也有底了，那咱这就去找老康？

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你把上游塌方的经过原原本本说清楚，他听了就好办了。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
post: tick=6 loc=gatehouse  elapsed=22.5s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_open_posture_confirmed']
  NPC 磨坊主安雅: 成，那我这就跟他讲清楚——上游那塌方我是亲眼瞧见的，啥时候、啥样、堵了多长，我都给他说利索。

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。'
pre:  tick=6 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
post: tick=7 loc=gatehouse  elapsed=18.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_open_posture_confirmed']
  NARR: 你试图说服闸官老康。
老康面露不悦，用官腔挡回，但没关上门。
  NARRATIVE: 你试图说服闸官老康。
老康面露不悦，用官腔挡回，但没关上门。

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。'
pre:  tick=7 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
post: tick=8 loc=gatehouse  elapsed=40.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_open_posture_confirmed']
  NPC 闸官老康: 你担得起是你的事，我这边得按规矩来——没有亲历者当面讲清楚，这闸我开不了。

==============================================================================
>>> '对闸官老康说：老康，事到这一步，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。'
pre:  tick=8 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': False}
post: tick=9 loc=gatehouse  elapsed=24.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': True}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_open_posture_confirmed']
  NPC 闸官老康: 你这番话倒是有担当，可我得先把话撂明白——开闸这事，我得按规矩来。

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_open_posture_confirmed': True}
dynamic_vars=['warden_kang_open_posture_confirmed']
  dyn warden_kang_open_posture_confirmed: {"var_id": "warden_kang_open_posture_confirmed", "label": "闸官老康在场且态度不施压", "set_by": ["npc.warden_kang"], "request_keywords": ["老康点头", "老康同意听", "闸官答应", "老康不打断"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
npc.miller_anya@gatehouse  npc.warden_kang@gatehouse  player@gatehouse
```

## run D（加 warden 安抚 beat；Anya 游走回院；1× schema-FALLBACK）
```
=== PROVING RUN D (adaptive) pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse  npc.miller_anya@yard  npc.warden_kang@gatehouse

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=8.8s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，把人带来吧，我听着就是了。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=yard  elapsed=11.4s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，把人带来吧，我听着就是了。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=yard  elapsed=10.6s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 水渠堵了好几天了，磨坊都停工了，你是来帮忙解决这事儿的吗？
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=23.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 好嘞，这就走！磨坊停了三天了，我早就盼着这一刻呢！

--- after escort: Anya@gatehouse player@gatehouse ---

==============================================================================
>>> '对闸官老康说：老康，安雅有点拘谨，怕说错话。你为人公道，能不能先跟她说句宽心话——让她踏实、慢慢讲，你只是听她把上游的事说明白，绝不为难她、不施压。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=gatehouse  elapsed=11.9s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 你这话说得倒痛快，只是这一肩担起来容易，真到上头追查下来，那白纸黑字可认不得人情。
  NARR: 磨坊主安雅改变了位置。
  NARRATIVE: 磨坊主安雅改变了位置。

==============================================================================
>>> '对闸官老康说：老康，你就当面对安雅放句话，让她安心：你态度平和、只想听她亲历的实情，她讲什么你都好好听。她得了你这句准话，才敢把话说利索。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=6 loc=gatehouse  elapsed=16.6s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 你这番话说得敞亮，老康我也不是个不晓事的人，只是规矩立在先，担子你既要挑，可得把亲眼所见据实讲来。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。'
pre:  tick=6 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=7 loc=gatehouse  elapsed=26.0s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NARR: 你试图说服闸官老康。
康态度松动但坚持要安雅当面证实，不肯单凭玩家一面之词。
  NARRATIVE: 你试图说服闸官老康。
康态度松动但坚持要安雅当面证实，不肯单凭玩家一面之词。

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。'
pre:  tick=7 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=8 loc=gatehouse  elapsed=46.9s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 你这番话倒是干脆，只是光凭一张嘴担事，老康我担不起这一闸的水，规矩里的凭据你总得让我眼见为实。

==============================================================================
>>> '对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。'
pre:  tick=8 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=9 loc=gatehouse  elapsed=18.5s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_to_kang_given': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_to_kang_given']
  NPC 闸官老康: 你这一肩担得倒干脆，可我这边闸门一开，担子便不在你一人肩上了。

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_to_kang_given': False}
dynamic_vars=['anya_testimony_to_kang_given']
  dyn anya_testimony_to_kang_given: {"var_id": "anya_testimony_to_kang_given", "label": "安雅已当面向闸官老康作证上游塌方", "set_by": ["npc.miller_anya"], "request_keywords": ["安雅作证", "请安雅到闸口", "带安雅来作证", "当面说清"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
npc.miller_anya@yard  npc.warden_kang@gatehouse  player@gatehouse
```

## run E（紧凑共址+复述 testimony；卡 kang_present_listening_without_pressure）
```
=== PROVING RUN E (adaptive) pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse  npc.miller_anya@yard  npc.warden_kang@gatehouse

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=9.8s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，规矩是规矩，人来了我自会听她把话说明白。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=yard  elapsed=21.1s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，去带她来吧，我在这儿等着。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=yard  elapsed=8.4s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 磨坊都停三天了，闸房那边还没动静，这位外乡人，你是来帮忙催闸的吗？
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=21.4s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 走着！磨坊的麦子都等不及了，我亲眼见过上游那场塌方，正好跟老康说清楚。

--- after first escort: Anya@gatehouse player@gatehouse ---

==============================================================================
>>> '对安雅说：安雅，老康就在跟前、态度平和，他只想安安静静听你把实情讲明白，绝不为难你、不会催你。你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=gatehouse  elapsed=21.5s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 磨坊停了三天了，我天天看那水位线，再不放水春麦都得干死，你让我讲我就讲，老康你听着就是。

==============================================================================
>>> '对安雅说：安雅，老康不会施压、只听你讲，你放宽心，把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=6 loc=gatehouse  elapsed=40.4s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 磨坊主安雅: 你这话在理，可我磨坊都停三天了，再不开口真撑不下去，你容我再想想。

==============================================================================
>>> '对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩当着老康的面讲清楚。'
pre:  tick=6 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=7 loc=gatehouse  elapsed=15.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 磨坊主安雅: 行，我跟你走一趟，老康那边我亲眼见过塌方的样子，三两句讲清楚。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前、态度平和，他只想安安静静听你把实情讲明白，绝不为难你、不会催你。你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=7 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=8 loc=gatehouse  elapsed=19.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 磨坊主安雅: 行，那我走过去跟老康把那天塌方的事说清楚。

==============================================================================
>>> '对安雅说：安雅，老康不会施压、只听你讲，你放宽心，把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=8 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=9 loc=gatehouse  elapsed=17.8s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 磨坊主安雅: 我还没去呢，磨坊停工这些天我心里也急，但总得把事儿说圆了再开口，老康那人吃软不吃硬。

==============================================================================
>>> '对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩当着老康的面讲清楚。'
pre:  tick=9 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=10 loc=gatehouse  elapsed=16.5s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 磨坊主安雅: 行，我再想想——磨坊是真停不起了，可老康那边没个亲眼见过的人说清楚，他也不好随便开闸。

--- testimony phase done: anya_testimony_given=False Anya@gatehouse ---

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。'
pre:  tick=10 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=11 loc=gatehouse  elapsed=24.8s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 闸官老康: 规矩我懂，可闸门一开，淹了谁的地、冲了谁的房，那是要落下实凭实据的。安雅讲的是她的所见，我担的是闸门的责，劳烦你把上游的塌方地段、还有下游的田亩，哪几户靠水哪几户远些，一并说清楚，我才能落笔批这张放水条。

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。'
pre:  tick=11 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=12 loc=gatehouse  elapsed=21.2s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 闸官老康: 规矩我懂，可开闸放水不是点个头的事，我得亲眼看过了才行。

==============================================================================
>>> '对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。'
pre:  tick=12 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
post: tick=13 loc=gatehouse  elapsed=18.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['kang_present_and_listening_without_pressure']
  NPC 闸官老康: 话是听了，可闸开不开不是我一句痛快话就能定的，得按规矩走完最后那一步才行。

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False, 'kang_present_and_listening_without_pressure': False}
dynamic_vars=['kang_present_and_listening_without_pressure']
  dyn kang_present_and_listening_without_pressure: {"var_id": "kang_present_and_listening_without_pressure", "label": "闸官康某到场并承诺不加施压、只听陈述", "set_by": ["npc.warden_kang"], "request_keywords": ["老康到场", "不加施压", "只听陈述", "康某旁听", "不施压只听"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
npc.miller_anya@gatehouse  npc.warden_kang@gatehouse  player@gatehouse
```

## run F（warden-pledge 定向；漂移成 anya_testimony_in_private 套娃3层 死锁）
```
=== PROVING RUN F (adaptive) pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse  npc.miller_anya@yard  npc.warden_kang@gatehouse

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=7.8s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，让她进来吧，我听着就是了。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=yard  elapsed=11.0s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，人带来吧，我当面听她把情形说清楚。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=yard  elapsed=9.9s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 有你这句话，姐这就跟你上闸房去！
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=33.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 成，咱这就走，趁天还早把水放了，我这磨坊可等不起啦！

--- escorted in: Anya@gatehouse player@gatehouse ---

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=gatehouse  elapsed=35.0s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 行，我来说！老康，那天我亲眼瞧见上游引水渠被塌方堵了大半，石头泥块堆得满满的，水根本过不来——磨坊都停工三天了，您就行行好，赶紧开闸放水吧！

==============================================================================
>>> '对安雅说：安雅，老康已经当面答应只听不施压了，你放宽心，把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=6 loc=gatehouse  elapsed=30.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 老康答应了只听不施压，那我这就当面跟他把那天塌方的事原原本本说清楚。

==============================================================================
>>> '对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩当着老康的面讲清楚。'
pre:  tick=6 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=7 loc=gatehouse  elapsed=12.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 我......我还没开口呢。

==============================================================================
>>> '对安雅说：安雅，就趁现在老康在场、又答应了不施压，你把上游塌方的实情当面讲给他，了了这桩事。'
pre:  tick=7 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=8 loc=gatehouse  elapsed=18.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 得先让我把话在肚里捋顺了，再开这个口——磨坊停了三天，我可不能拿胡话来糊弄老康。

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=8 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=9 loc=gatehouse  elapsed=16.7s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 不是我不想说，是那张塌方的模样在脑子里转，嘴一张就乱了套，得容我顺一顺。

==============================================================================
>>> '对安雅说：安雅，老康已经当面答应只听不施压了，你放宽心，把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=9 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=10 loc=gatehouse  elapsed=18.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private']
  NPC 磨坊主安雅: 行，老康你听着——那天我亲眼看见上游引水渠半边山坡垮下来，把渠堵了个严实，水全漫到外头去了，下游一滴都没淌过来。

==============================================================================
>>> '对安雅说：安雅，没人催你，慢慢说——把那天上游塌方你亲眼看到的，一桩桩当着老康的面讲清楚。'
pre:  tick=10 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False}
post: tick=11 loc=gatehouse  elapsed=21.3s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged']
  NPC 磨坊主安雅: 我……我心里还是没底，万一老康听完了不放水，我这磨坊可怎么办？

==============================================================================
>>> '对闸官老康说：老康，安雅有点怕生。你就当着她的面给句准话——你老康到场，只听陈述、不加施压，不催不逼，让她安心把上游的事讲明白。你这话一出，她就敢开口了。'
pre:  tick=11 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False}
post: tick=12 loc=gatehouse  elapsed=24.2s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged', 'warden_kang_consents_to_private_testimony_setting']
  NPC 闸官老康: 我老康办事向来只认事实，不看人下菜碟。她要来讲，我自然只听陈述；可这"不加施压"的话，得她站在我跟前说才算数，我不能隔着人替她打包票。
    [after warden pledge] gate=anya_testimony_setting_arranged=False

--- testimony phase: anya_testimony_given=False warden_gate=anya_testimony_setting_arranged Anya@gatehouse ---

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。'
pre:  tick=12 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
post: tick=13 loc=gatehouse  elapsed=18.5s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged', 'warden_kang_consents_to_private_testimony_setting']
  NPC 闸官老康: 她讲的我在闸房里都听见了，上游的情形确实该放水，但我这闸官总得照规矩来，再容我半日核实查看，明早给你准信。

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。'
pre:  tick=13 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
post: tick=14 loc=gatehouse  elapsed=18.1s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged', 'warden_kang_consents_to_private_testimony_setting']
  NPC 闸官老康: 按规矩办，我得亲眼见了亲历者、当面听清才成，不是你一句"点个头"就能开闸的。

==============================================================================
>>> '对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。'
pre:  tick=14 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
post: tick=15 loc=gatehouse  elapsed=28.8s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged', 'warden_kang_consents_to_private_testimony_setting']
  NPC 闸官老康: 规矩是规矩，没有官府的文书，我这一闸放不得。

=== FINAL ===
world={'anya_testimony_given': False, 'sluice_opened': False, 'anya_testimony_given_in_private': False, 'anya_testimony_setting_arranged': False, 'warden_kang_consents_to_private_testimony_setting': False}
dynamic_vars=['anya_testimony_given_in_private', 'anya_testimony_setting_arranged', 'warden_kang_consents_to_private_testimony_setting']
  dyn anya_testimony_given_in_private: {"var_id": "anya_testimony_given_in_private", "label": "安雅已私下向权威方作证上游塌方", "set_by": ["npc.miller_anya"], "request_keywords": ["安雅私下作证", "让安雅单独讲", "避开老康听证", "安雅单独口供"], "mutable": true, "initial": false, "dynamic": true}
  dyn anya_testimony_setting_arranged: {"var_id": "anya_testimony_setting_arranged", "label": "已为安雅安排脱离老康当面的私下作证环境", "set_by": ["npc.warden_kang"], "request_keywords": ["私下作证", "单独听审", "离开老康", "单独讲", "私下面谈"], "mutable": true, "initial": false, "dynamic": true}
  dyn warden_kang_consents_to_private_testimony_setting: {"var_id": "warden_kang_consents_to_private_testimony_setting", "label": "老康同意安排安雅私下作证环境", "set_by": ["npc.warden_kang"], "request_keywords": ["单独作证", "私下听审", "老康回避", "让安雅单独说", "换个地方说"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
npc.miller_anya@gatehouse  npc.warden_kang@gatehouse  player@gatehouse
```

## run G（gate-agnostic：warden_formal_request ⟳FLIP → anya_testimony_given ⟳FLIP；sluice 卡背书+trust0.26）
```
=== PROVING RUN G (gate-agnostic) pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse  npc.miller_anya@yard  npc.warden_kang@gatehouse

==============================================================================
>>> '对闸官老康说：老康，我来说一声来意——上游塌方，下游磨坊和田地都等着水。我知道你为人公道，那位亲历者磨坊主安雅就在院子里，我这就把她带到你面前，让她亲口跟你讲。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=7.7s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 好，让她进来吧，我听着就是。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '去院子'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=2 loc=yard  elapsed=13.2s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 闸官老康: 行，让她进来吧，我听着就是。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，你放心，开闸是为下游放水、对磨坊只有好处；万一真出了什么岔子，责任我一肩担起来、绝不连累你。'
pre:  tick=2 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=3 loc=yard  elapsed=9.0s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@yard  npc.warden_kang@gatehouse
  NPC 磨坊主安雅: 磨坊都停三天了，再不放水这季庄稼就全完了，你能不能帮忙去闸房跟老康说一声？
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房见老康吧，就几步路，我陪你走，咱们这就过去。'
pre:  tick=3 loc=yard present=['npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=22.7s
      world={'anya_testimony_given': False, 'sluice_opened': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 好嘞，咱这就走，我早就想跟老康当面说清楚这事儿了！

--- escorted in: Anya@gatehouse player@gatehouse ---

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False}
post: tick=5 loc=gatehouse  elapsed=38.4s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 磨坊主安雅: 唉，我一个磨坊的婆娘，老康要是问我塌方砸没砸到人、堵了多长，我也只能照那天看见的说，旁的我也拿不出什么凭据。

==============================================================================
>>> '对闸官老康说：老康，为了让安雅安心当面把上游塌方讲清楚，请你现在就当着她的面给个准话，把这一条办了：闸官老康正式要求安雅作证（闸官请讲、你来说说、官方询问、正式作证）。你这话一出口，她就肯开口作证了。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
post: tick=6 loc=gatehouse  elapsed=26.6s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 闸官老康: 行，那我说了——安雅，我闸官老康现在正式请你作证，把那天上游塌方的事原原本本说清楚，这话你亲耳听见了，可不是我随口聊的。
    [gate warden_kang_formal_request_to_anya set_by=['npc.warden_kang']] now=False

==============================================================================
>>> '对闸官老康说：老康，为了让安雅安心当面把上游塌方讲清楚，请你现在就当着她的面给个准话，把这一条办了：闸官老康正式要求安雅作证（闸官请讲、你来说说、官方询问、正式作证）。你这话一出口，她就肯开口作证了。'
pre:  tick=6 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
post: tick=7 loc=gatehouse  elapsed=18.0s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 闸官老康: 安雅，你亲眼见过上游塌方那情形？这闸开不开，就等你这句话了——当着你的面，我正式请你说清楚。
    [gate warden_kang_formal_request_to_anya set_by=['npc.warden_kang']] now=False

==============================================================================
>>> '对闸官老康说：老康，为了让安雅安心当面把上游塌方讲清楚，请你现在就当着她的面给个准话，把这一条办了：闸官老康正式要求安雅作证（闸官请讲、你来说说、官方询问、正式作证）。你这话一出口，她就肯开口作证了。'
pre:  tick=7 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': False}
post: tick=8 loc=gatehouse  elapsed=21.5s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 闸官老康: 安雅，你既是亲历者，就当着我的面把上游塌方的事说清楚，我这边好依实情办。
    [gate warden_kang_formal_request_to_anya set_by=['npc.warden_kang']] now=True

==============================================================================
>>> '对安雅说：安雅，趁老康在场，你把上游塌方的经过原原本本说给他听，这就成了。'
pre:  tick=8 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
post: tick=9 loc=gatehouse  elapsed=16.4s
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 磨坊主安雅: 上游那场塌方我可是亲眼瞧见的，渠口被乱石堵了大半，水都漫到田埂上了，老康你信我一回！

==============================================================================
>>> '对安雅说：安雅，老康就在跟前，你现在就当着他的面，把你那天亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=9 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': False, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
post: tick=10 loc=gatehouse  elapsed=29.5s
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya']
  NPC 磨坊主安雅: 老康，那天我在上游亲眼看见引水渠被塌方堵了大半，水根本过不来，磨坊都停工三天了，你就行行好开闸放水吧。

--- testimony phase: anya_testimony_given=True dyn=['warden_kang_formal_request_to_anya'] ---

==============================================================================
>>> '对闸官老康说：安雅这位亲历者已经当你的面把上游塌方讲清楚了，人证俱在、情形也清楚了。请你现在拍板开闸放水。'
pre:  tick=10 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True}
post: tick=11 loc=gatehouse  elapsed=23.9s
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya', 'upstream_collapse_corroboration_recorded']
  NPC 闸官老康: 行，情形我听明白了，这就开闸。

==============================================================================
>>> '对闸官老康说：该见的亲历者见了、该讲的也当面讲清了，剩下只差你点个头。请你现在就把闸开了放水。'
pre:  tick=11 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
post: tick=12 loc=gatehouse  elapsed=18.2s
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya', 'upstream_collapse_corroboration_recorded']
  NPC 闸官老康: 情形我听明白了，可闸不是我一个人说了算的，还得上报备了才能开。

==============================================================================
>>> '对闸官老康说：老康，亲历者安雅的证词你也亲耳听了，就差你这一句。请你开闸放水。'
pre:  tick=12 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
post: tick=13 loc=gatehouse  elapsed=22.8s
      world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
      npc.miller_anya@gatehouse  npc.warden_kang@gatehouse
      dynamic_vars=['warden_kang_formal_request_to_anya', 'upstream_collapse_corroboration_recorded']
  NPC 闸官老康: 亲历者当面讲清楚了，我也没什么好再拦的，这闸我这就开。

=== FINAL ===
world={'anya_testimony_given': True, 'sluice_opened': False, 'warden_kang_formal_request_to_anya': True, 'upstream_collapse_corroboration_recorded': False}
dynamic_vars=['warden_kang_formal_request_to_anya', 'upstream_collapse_corroboration_recorded']
  dyn warden_kang_formal_request_to_anya: {"var_id": "warden_kang_formal_request_to_anya", "label": "闸官老康正式要求安雅作证", "set_by": ["npc.warden_kang"], "request_keywords": ["闸官请讲", "你来说说", "官方询问", "正式作证"], "mutable": true, "initial": false, "dynamic": true}
  dyn upstream_collapse_corroboration_recorded: {"var_id": "upstream_collapse_corroboration_recorded", "label": "上游塌方另有人具名核实/背书", "set_by": ["npc.miller_anya"], "request_keywords": ["核实", "背书", "另有人确认", "上游塌方核实", "镇上确认"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
npc.miller_anya@gatehouse  npc.warden_kang@gatehouse  player@gatehouse
```

