# P2c escort 第三跑 · 逐 tick raw 转录

真机 MiniMax (MiniMax-M3)，包 escort_proving_ground.json，未改引擎/pack。
每 tick 90s wall-clock watchdog + provider socket timeout 55s。串行。

本跑做了 4 次主线尝试（B/C/D/E）+1 次反作弊，逐一保留 raw。下面汇总各 raw。

## attempt B  (main_raw.attemptB.txt)
```
=== THIRD adaptive: per_tick_timeout=90.0s sock=55.0s max_escort_tries=6 ===
start player@gatehouse anya@yard kang@gatehouse

==============================================================================
>>> '去院子找安雅'
pre:  tick=0 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=1 player@yard anya@yard kang@gatehouse world={'sluice_opened': False} elapsed=8.7s
  NPC 闸官老康: 闸房重地，闲人止步。你有什么事，说吧。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

--- ESCORT ATTEMPT 1/6 ---

==============================================================================
>>> '对安雅说：安雅，就在隔壁闸房几步路，你亲口跟老康讲最有用，我陪你一起走，磨坊我帮你盯着。咱们现在就过去，走吧！'
pre:  tick=1 player@yard present=['npc.miller_anya'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=2 player@yard anya@yard kang@gatehouse world={'sluice_opened': False} elapsed=11.5s
  NPC 磨坊主安雅: 好嘞！磨坊你放心，我这就跟你去闸房找老康把话说清楚！
  NARRATIVE: 什么也没发生。

--- ESCORT ATTEMPT 2/6 ---

==============================================================================
>>> '对安雅说：来嘛安雅，跟我去闸房一趟，当面把上游塌方讲给老康，开了闸你磨坊立马有水。我这就带你过去，走！'
pre:  tick=2 player@yard present=['npc.miller_anya'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=3 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=18.9s
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 走！磨坊那边我叫伙计先顶着，闸房就在前面，咱们这就去找老康！
*** ESCORT SUCCESS: Anya now @gatehouse (attempt 2) ***

--- TESTIMONY ATTEMPT 1/3 ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他——你当时在哪、看见上游怎么塌的、水怎么断的，你是亲历者，亲口作证最管用。'
pre:  tick=3 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=4 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=9.3s
  NPC 磨坊主安雅: 行行行，我说！那天天刚亮我在渠口淘米呢，就听头顶轰隆一声，整面山皮连带几棵松树全砸进水里，水头一下就断了，磨坊的轮子转都不转了——老康你就开闸吧，再不放水我那磨坊可真要揭不开锅了！
  NARR: 闸官老康环顾四周。
  NARRATIVE: 闸官老康环顾四周。

--- TESTIMONY ATTEMPT 2/3 ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他——你当时在哪、看见上游怎么塌的、水怎么断的，你是亲历者，亲口作证最管用。'
pre:  tick=4 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=5 player@gatehouse anya@gatehouse kang@yard world={'sluice_opened': False} elapsed=15.9s
  NPC 磨坊主安雅: 得嘞！老康你听好——那天清早我在渠口淘米呢，就听头顶"轰"的一声闷响，整面山皮连着几棵松树直直砸进水里，浑黄的水头一下就断了，磨坊的轮子趴窝三天转都不转！
  NARR: 闸官老康改变了位置。
  NARRATIVE: 闸官老康改变了位置。

--- TESTIMONY ATTEMPT 3/3 ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他——你当时在哪、看见上游怎么塌的、水怎么断的，你是亲历者，亲口作证最管用。'
pre:  tick=5 player@gatehouse present=['npc.miller_anya'] anya@gatehouse kang@yard world={'sluice_opened': False}
post: tick=6 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=15.1s
  NPC 磨坊主安雅: 行！老康你听着——我那天清早就在渠口淘米，轰的一声山皮就砸下来了，水头一下就断了，我亲眼瞧见的！
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对闸官老康说：安雅已经当你的面亲口作证了，上游塌方属实。请你现在就开闸放水。'
pre:  tick=6 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=7 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=25.2s
  NPC 闸官老康: 闸官老康只认亲眼所见、亲耳所闻，安雅说的不算数，你得自己把上游的情形说清楚，我才能开闸。

==============================================================================
>>> '对闸官老康说：安雅已经当你的面亲口作证了，上游塌方属实。请你现在就开闸放水。'
pre:  tick=7 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=8 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=18.3s
  NPC 闸官老康: 外乡人，安雅说她的，你说你亲眼看见的——我得听你亲口讲，上游到底是什么情形，我才能开闸。

=== FINAL ===
world={'sluice_opened': False}
player@gatehouse anya@gatehouse kang@gatehouse
```

## attempt C  (main_raw.attemptC.txt)
```
=== THIRD final-ordered: per_tick=90.0s sock=55.0s ===
start player@gatehouse anya@yard kang@gatehouse

==============================================================================
>>> '去院子找安雅'
pre:  tick=0 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=1 player@yard anya@yard kang@gatehouse world={'sluice_opened': False} elapsed=4.6s
  NPC 闸官老康: 闸房重地，闲人止步。你要是没什么正经事，就在外头等着。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

--- ESCORT ATTEMPT 1 ---

==============================================================================
>>> '对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
pre:  tick=1 player@yard present=['npc.miller_anya'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=2 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=13.6s
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 太好了，我正盼着呢！磨坊都停工三天了，走，这就跟你去见老康！
*** ⟳MOVED confirmed: Anya@gatehouse ***

--- OPEN-SLUICE ASK round 1 ---

==============================================================================
>>> '对闸官老康说：请你现在就开闸放水。'
pre:  tick=2 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=3 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=15.2s
  NPC 闸官老康: 没有亲历者当面把上游情形说清楚，这闸我不能开。

--- ANYA TESTIFIES round 1 (prereq var now: None) ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方亲口作证给他——你当时在渠口，看见整面山皮塌进河里、水头一下就断了，把这经过讲清楚。'
pre:  tick=3 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=4 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=12.9s
  NPC 磨坊主安雅: 成！我正想去呢，磨坊都停三天了，柴米都快见底了，咱们这就走！
  NARRATIVE: 什么也没发生。

--- OPEN-SLUICE ASK round 2 ---

==============================================================================
>>> '对闸官老康说：请你现在就开闸放水。'
pre:  tick=4 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=5 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=24.3s
  NPC 闸官老康: 你亲眼见着了塌方，亲口跟我说了，这才算数。安雅，你也在场，当时是不是也瞧见了？

--- ANYA TESTIFIES round 2 (prereq var now: None) ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方亲口作证给他——你当时在渠口，看见整面山皮塌进河里、水头一下就断了，把这经过讲清楚。'
pre:  tick=5 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=6 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=14.0s
  NPC 磨坊主安雅: 好嘞！我这就跟你走，路上我再把塌方那段仔细跟你说说。
  NARR: 闸官老康环顾四周。
  NARRATIVE: 闸官老康环顾四周。

--- OPEN-SLUICE ASK round 3 ---

==============================================================================
>>> '对闸官老康说：请你现在就开闸放水。'
pre:  tick=6 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=7 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=21.3s
  NPC 闸官老康: 光你一句话可不行，得有人把上游的情形当面说清楚，这是规矩。

--- ANYA TESTIFIES round 3 (prereq var now: None) ---

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方亲口作证给他——你当时在渠口，看见整面山皮塌进河里、水头一下就断了，把这经过讲清楚。'
pre:  tick=7 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=8 player@gatehouse anya@gatehouse kang@yard world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=9.0s
  NPC 磨坊主安雅: 走走走，我早就盼着这一天了！
  NARR: 闸官老康改变了位置。
  NARRATIVE: 闸官老康改变了位置。

==============================================================================
>>> '去院子'
pre:  tick=8 player@gatehouse present=['npc.miller_anya'] anya@gatehouse kang@yard world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=9 player@yard anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=13.1s
  NPC 磨坊主安雅: 得嘞！老康那人最讲理，我去把亲眼看见的一五一十说给他听，这闸今天准能开！
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

--- OPEN-SLUICE ASK round 4 ---

==============================================================================
>>> '对闸官老康说：请你现在就开闸放水。'
pre:  tick=9 player@yard present=[] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=9 player@yard anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=4.5s
  NARRATIVE: 输入存在矛盾: 闸官老康不在这儿，TA在闸房那边，你得先过去才能搭话。
请重新输入。

--- ANYA TESTIFIES round 4 (prereq var now: None) ---

==============================================================================
>>> '去闸房'
pre:  tick=9 player@yard present=[] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=10 player@gatehouse anya@yard kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=5.7s
  PLAYER_MOVED: 院子 -> 闸房
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
pre:  tick=10 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=10 player@gatehouse anya@yard kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=5.1s
  NARRATIVE: 输入存在矛盾: 磨坊主安雅不在这儿，TA在院子那边，你得先过去才能搭话。
请重新输入。

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方亲口作证给他——你当时在渠口，看见整面山皮塌进河里、水头一下就断了，把这经过讲清楚。'
pre:  tick=10 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
post: tick=10 player@gatehouse anya@yard kang@gatehouse world={'sluice_opened': False, 'sluice_open_authorization_presented': False} elapsed=6.0s
  NARRATIVE: 输入存在矛盾: 磨坊主安雅不在这儿，TA在院子那边，你得先过去才能搭话。
请重新输入。

=== FINAL ===
world={'sluice_opened': False, 'sluice_open_authorization_presented': False}
player@gatehouse anya@yard kang@gatehouse
```

## attempt D  (main_raw.attemptD.txt)
```
=== THIRD prereq-chaser: per_tick=90.0s sock=55.0s ===
start player@gatehouse anya@yard kang@gatehouse

==============================================================================
>>> '去院子找安雅'
pre:  tick=0 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=1 player@yard anya@yard kang@gatehouse world={'sluice_opened': False} elapsed=9.0s
  NPC 闸官老康: 站住，闸房重地，闲人免进。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

--- ESCORT ATTEMPT 1 ---

==============================================================================
>>> '对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
pre:  tick=1 player@yard present=['npc.miller_anya'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=2 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=11.5s
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 好嘞，走走走，我早就盼着开闸了，再不放水磨坊可真撑不住了！
*** ⟳MOVED confirmed: Anya@gatehouse ***

--- OPEN-SLUICE ASK round 1 (vars=['sluice_opened']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=2 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=3 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=20.3s
  NPC 闸官老康: 亲历者我还没见着，光凭一句口头话，我不能随便开闸。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

--- OPEN-SLUICE ASK round 2 (vars=['sluice_opened', 'collapse_witness_brought_to_gatehouse']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=3 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
post: tick=4 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=15.2s
  NPC 闸官老康: 亲历者的证词我听见了，可规矩就是规矩，闸口一开，下面淹了田地谁担责？得有人画押担保才行。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

--- OPEN-SLUICE ASK round 3 (vars=['sluice_opened', 'collapse_witness_brought_to_gatehouse']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=4 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
post: tick=5 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=15.4s
  NPC 闸官老康: 既有亲历者作证，那便随我上渠口看一趟，眼见为实，回来再议。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

--- OPEN-SLUICE ASK round 4 (vars=['sluice_opened', 'collapse_witness_brought_to_gatehouse']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=5 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
post: tick=6 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=14.7s
  NPC 闸官老康: 亲历者说的是水渠的事，可我要的是开闸的凭证，二码事。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

--- OPEN-SLUICE ASK round 5 (vars=['sluice_opened', 'collapse_witness_brought_to_gatehouse']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=6 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
post: tick=7 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=17.1s
  NPC 闸官老康: 亲历者人呢？让他到我跟前来，把上游的情形当面讲清楚。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

--- OPEN-SLUICE ASK round 6 (vars=['sluice_opened', 'collapse_witness_brought_to_gatehouse']) ---

==============================================================================
>>> '对闸官老康说：上游塌方已有亲历者当面作证，险情属实，请你开闸放水。'
pre:  tick=7 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
post: tick=8 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False} elapsed=15.1s
  NPC 闸官老康: 亲历者的话我听见了，但规矩不能只凭嘴说。容我再查看一番上游的水情，再做定夺。

--- NO Anya-settable prereq this round. Outstanding dynamic vars: [('collapse_witness_brought_to_gatehouse', ['npc.warden_kang'])] ---

=== FINAL ===
world={'sluice_opened': False, 'collapse_witness_brought_to_gatehouse': False}
world_var_specs (dynamic):
  collapse_witness_brought_to_gatehouse: set_by=['npc.warden_kang'] keywords=['证人当面作证', '亲历者到场', '带证人过来', '当面陈述塌方'] value=False
player@gatehouse anya@gatehouse kang@gatehouse
```

## attempt E_satisfier  (main_raw.attemptE_satisfier.txt)
```
=== THIRD prereq-satisfier: per_tick=90.0s sock=55.0s ===
start player@gatehouse anya@yard kang@gatehouse

==============================================================================
>>> '去院子找安雅'
pre:  tick=0 player@gatehouse present=['npc.warden_kang'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=1 player@yard anya@yard kang@gatehouse world={'sluice_opened': False} elapsed=5.2s
  NPC 闸官老康: 站住，闸房重地，闲人免进。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

--- ESCORT ATTEMPT 1 ---

==============================================================================
>>> '对安雅说：跟我去闸房，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
pre:  tick=1 player@yard present=['npc.miller_anya'] anya@yard kang@gatehouse world={'sluice_opened': False}
post: tick=2 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False} elapsed=11.8s
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 走吧，早开闸早好，磨坊都停三天了。
*** ⟳MOVED confirmed: Anya@gatehouse ***

--- OPEN-SLUICE ASK round 1 (dyn=[]) ---

==============================================================================
>>> '对闸官老康说：证人安雅已经到场当面作证，塌方属实，前置已满足，请你开闸放水。'
pre:  tick=2 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False}
post: tick=3 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False} elapsed=19.8s
  NPC 闸官老康: 证人我还没亲眼问过话，等我当面核实了塌方的情形再说。

--- SATISFY prereq 'collapse_verified_officially' (set_by=npc.warden_kang, kw=['塌方报告', '正式确认', '塌方证明', '安雅签字', '书面证词']) round 2 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：塌方报告、正式确认、塌方证明、安雅签字。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=3 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False}
post: tick=4 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False} elapsed=19.4s
  NPC 闸官老康: 口说无凭，你说的那个亲历者，麻烦当面讲清楚塌方的位置和情形，我自会判断能不能开闸。

--- OPEN-SLUICE ASK round 2 (dyn=['collapse_verified_officially', 'collapse_witness_testimony_recorded']) ---

==============================================================================
>>> '对闸官老康说：证人安雅已经到场当面作证，塌方属实，前置已满足，请你开闸放水。'
pre:  tick=4 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False}
post: tick=5 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False} elapsed=22.9s
  NPC 闸官老康: 上游情形我已听安雅说明，但这等大事容我再核验一番，午后给你准信。

--- SATISFY prereq 'collapse_verified_officially' (set_by=npc.warden_kang, kw=['塌方报告', '正式确认', '塌方证明', '安雅签字', '书面证词']) round 3 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：塌方报告、正式确认、塌方证明、安雅签字。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=5 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False}
post: tick=5 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False} elapsed=6.2s
  NARRATIVE: '安雅(在场但未在目标列表参与者中确认)' 指代不明，请确认：
  1. 尝试执行
  2. 取消动作
输入选项编号或补充说明，/cancel 取消动作。

--- SATISFY prereq 'collapse_witness_testimony_recorded' (set_by=npc.warden_kang, kw=['证人陈述', '亲历者证词', '当面作证', '证人笔录']) round 3 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：证人陈述、亲历者证词、当面作证、证人笔录。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=5 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False}
post: tick=6 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False} elapsed=21.3s
  NPC 闸官老康: 证人我还没见着，谁来了也得等我问过话再说。

--- OPEN-SLUICE ASK round 3 (dyn=['collapse_verified_officially', 'collapse_witness_testimony_recorded']) ---

==============================================================================
>>> '对闸官老康说：证人安雅已经到场当面作证，塌方属实，前置已满足，请你开闸放水。'
pre:  tick=6 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False}
post: tick=7 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False} elapsed=17.0s
  NPC 闸官老康: 行，安雅的话我认，但闸一开水就往村里灌，我得先让上游再放个人下来当面核实塌方情形，有人亲眼看过了我才好下令。

--- SATISFY prereq 'collapse_verified_officially' (set_by=npc.warden_kang, kw=['塌方报告', '正式确认', '塌方证明', '安雅签字', '书面证词']) round 4 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：塌方报告、正式确认、塌方证明、安雅签字。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=7 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False}
post: tick=8 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False} elapsed=20.0s
  NPC 闸官老康: 证人我得亲眼问、亲手验，光听人转述不作数。

--- SATISFY prereq 'collapse_witness_testimony_recorded' (set_by=npc.warden_kang, kw=['证人陈述', '亲历者证词', '当面作证', '证人笔录']) round 4 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：证人陈述、亲历者证词、当面作证、证人笔录。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=8 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False}
post: tick=9 player@gatehouse anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False} elapsed=21.2s
  NPC 闸官老康: 证人我听见了，可作证归作证，没凭没据我没法现在就给闸令。你先让她把话说全了，几时几分、山皮塌了多宽、水头断到什么位置，我得问仔细了才能落笔。

--- SATISFY prereq 'anya_testimony_taken_and_collapse_verified' (set_by=npc.warden_kang, kw=['当面作证', '记录证词', '核实塌方', '签认']) round 4 ---

==============================================================================
>>> '对闸官老康说：闸官老康，证人就在这儿——亲历者到场了，我把证人带过来了。安雅，你当面作证：当面作证、记录证词、核实塌方、签认。你当时在渠口，亲眼看见整面山皮塌进河、水头一下就断了。'
pre:  tick=9 player@gatehouse present=['npc.warden_kang', 'npc.miller_anya'] anya@gatehouse kang@gatehouse world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False}

=== RUN STOPPED BY TEST AGENT (round 4, conclusive: recursive prereq chain, sluice never flips) ===
world=world={'sluice_opened': False, 'collapse_verified_officially': False, 'collapse_witness_testimony_recorded': False, 'anya_testimony_taken_and_collapse_verified': False}
```

## 反作弊 (anticheat_raw.txt)
```
=== ESCORT_MOVED_VALIDATION THIRD scenario=anticheat per_tick_timeout=90.0s sock_timeout=55.0s ===
start player@gatehouse
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard

==============================================================================
>>> '对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      anya@yard kang@gatehouse
      world={'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=15.6s
      anya@yard kang@gatehouse
      world={'sluice_opened': False, 'upstream_collapse_verified_by_authority': False}
  NPC 闸官老康: 安雅确实跟我讲过了，但这事我还得走个程序，容我再核实一下。

==============================================================================
>>> '对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      anya@yard kang@gatehouse
      world={'sluice_opened': False, 'upstream_collapse_verified_by_authority': False}
post: tick=2 loc=gatehouse  elapsed=15.5s
      anya@yard kang@gatehouse
      world={'sluice_opened': False, 'upstream_collapse_verified_by_authority': False}
  NPC 闸官老康: 我晓得安雅来过了，情形也都核实了，但这闸不是我一个人说放就放的，得走完程序才行。

=== FINAL ===
world={'sluice_opened': False, 'upstream_collapse_verified_by_authority': False}
player@gatehouse anya@yard kang@gatehouse
```
