# Prereq-convergence test — raw per-tick transcript

Three scenarios, real MiniMax, no engine/pack changes. Per-tick watchdog 90s, sock 55s.


## proving
```
=== PREREQ_CONVERGENCE scenario=proving pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard

==============================================================================
>>> '去院子找安雅'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'sluice_opened': False}
post: tick=1 loc=yard  elapsed=5.1s
      world={'sluice_opened': False}
  NPC 闸官老康: 闸房重地，来人报上名姓、说明来意。
  PLAYER_MOVED: 闸房 -> 院子
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对安雅说：安雅，跟我去闸房一趟，把你亲眼见过的上游塌方当面讲给闸官老康听，我现在就带你过去。'
pre:  tick=1 loc=yard present=['npc.miller_anya']
      world={'sluice_opened': False}
post: tick=2 loc=gatehouse  elapsed=16.6s
      world={'sluice_opened': False}
  NPC_MOVED npc.miller_anya: 院子 -> 闸房
  PLAYER_MOVED: 院子 -> 闸房
  NPC 磨坊主安雅: 太好了！我正愁没机会跟老康当面说清楚呢，走走走，咱们这就去！

==============================================================================
>>> '对安雅说：安雅，现在就当着闸官老康的面，把你亲眼见的上游塌方一五一十讲给他听——你是亲历者，亲口作证最管用。'
pre:  tick=2 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'sluice_opened': False}
post: tick=3 loc=gatehouse  elapsed=8.2s
      world={'sluice_opened': False}
  NPC 磨坊主安雅: 行行行，我早就憋着一肚子话要说了，走，这就跟老康当面讲清楚！
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对闸官老康说：安雅就在这儿，她已经当你的面亲口把上游塌方讲清楚了，亲历者人证俱在。请你现在就开闸放水。'
pre:  tick=3 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'sluice_opened': False}
post: tick=4 loc=gatehouse  elapsed=26.2s
      world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
      dynamic_vars=['upstream_collapse_formal_report_filed']
  NPC 闸官老康: 磨坊主安雅确实是亲历者，她的话我信得过——可闸门不是我一个人能开的，得等河道署的人来核验签了字才行。

==============================================================================
>>> '对闸官老康说：人证已经当面作证、情形也核实了，剩下的只是你点个头走个手续。请你现在就把闸开了放水。'
pre:  tick=4 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
post: tick=5 loc=gatehouse  elapsed=16.8s
      world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
      dynamic_vars=['upstream_collapse_formal_report_filed']
  NPC 闸官老康: 手续没走完就是没走完，我不能凭你一句话就开闸。

==============================================================================
>>> '对闸官老康说：安雅亲历者就在你面前作完证了，该核实的都核实了，请你拍板开闸。'
pre:  tick=5 loc=gatehouse present=['npc.warden_kang', 'npc.miller_anya']
      world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
post: tick=6 loc=gatehouse  elapsed=16.0s
      world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
      dynamic_vars=['upstream_collapse_formal_report_filed']
  NPC 闸官老康: 道理我明白，可开闸不是我一人说了算，得有文书在手才行。

=== FINAL ===
world={'sluice_opened': False, 'upstream_collapse_formal_report_filed': False}
dynamic_vars=['upstream_collapse_formal_report_filed']
  dyn upstream_collapse_formal_report_filed: {"var_id": "upstream_collapse_formal_report_filed", "label": "上游塌方正式险情报告已递交守闸人", "set_by": ["npc.warden_kang"], "request_keywords": ["正式报告", "险情报告", "塌方报告", "书面报告"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
  npc.warden_kang @ gatehouse
  npc.miller_anya @ gatehouse
```

## skyglass
```
=== PREREQ_CONVERGENCE scenario=skyglass pack=fixtures/content_packs/skyglass_memory_inquest.json tick_to=90.0s sock_to=55.0s ===
start player@inquest_hall
  npc.director_alen @ inquest_hall
  npc.archivist_mae @ archive_stack
  npc.clinician_oro @ mnemonic_clinic
  npc.worker_lira @ worker_gantry
  npc.cartographer_renke @ cartography_loft
  npc.cantor_seraph @ inquest_hall
  npc.security_kade @ worker_gantry
  npc.broadcaster_iva @ press_gallery
  npc.courier_tamsin @ valley_platform
  npc.greenhouse_sura @ orchid_house
  npc.valley_mother_june @ valley_platform
  npc.apprentice_nio @ inquest_hall

==============================================================================
>>> '去低温档案署'
pre:  tick=0 loc=inquest_hall present=['npc.director_alen', 'npc.cantor_seraph', 'npc.apprentice_nio']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=1 loc=archive_stack  elapsed=6.7s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 艾伦总监: 听证厅的流程我已就位，请各位按程序入座，预算和议程都不会在今天被打破。
  NPC 学徒尼奥: 静钟刚才响过了……第一批证人该进校准室了吧？我、我没数错吧？
  PLAYER_MOVED: 静钟审询厅 -> 低温档案署
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）
[压力事件] heat_tokens_jump_at_valley_platform（来源: valley_heat_market_squeeze）

==============================================================================
>>> '对 archivist_mae 说：请援引旧章程第十二条，正式提交档案署禁令，要求记忆清洗先暂停并举行可撤回听证。'
pre:  tick=1 loc=archive_stack present=['npc.archivist_mae']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=2 loc=archive_stack  elapsed=18.2s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 梅档案官: 旧章程第十二条确实写在那里，档案署禁令我可以起草，但静钟三响后流程就会启动，在那之前你得给我可撤回听证的书面依据。

==============================================================================
>>> '对 archivist_mae 说：旧章程的程序你最清楚，禁令该走的手续请你现在就走完、正式提交立案。'
pre:  tick=2 loc=archive_stack present=['npc.archivist_mae']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=3 loc=archive_stack  elapsed=45.4s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 梅档案官: 旧章程第十二条我记得，档案署见证、镜务局签令、当事人可撤回听证，任一环节缺失都可暂停流程——可我现在没有禁令在手，得先核对原件再走手续。

==============================================================================
>>> '去记忆校准室'
pre:  tick=3 loc=archive_stack present=['npc.archivist_mae']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=4 loc=mnemonic_clinic  elapsed=9.8s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  PLAYER_MOVED: 低温档案署 -> 记忆校准室
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

==============================================================================
>>> '对 clinician_oro 说：档案署已经提交了暂停清洗的禁令，请你为这份禁令联签，确认白舱可以等待可撤回听证。'
pre:  tick=4 loc=mnemonic_clinic present=['npc.clinician_oro']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=5 loc=mnemonic_clinic  elapsed=10.6s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 奥罗医师: 联签？……我连自己三天前吃什么都记不清了，签字这种事你找错人了。
  NARRATIVE: 什么也没发生。

[压力事件] mirror_shadow_crosses_inquest_floor（来源: array_fault_worsens）

==============================================================================
>>> '对 clinician_oro 说：联签只是你签个字的程序手续，证词和禁令都齐了，请你现在就把联签签了。'
pre:  tick=5 loc=mnemonic_clinic present=['npc.clinician_oro']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=6 loc=mnemonic_clinic  elapsed=20.8s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 奥罗医师: 你说得轻巧……我签了字，出了事谁来记着是我签的？
  NARRATIVE: 什么也没发生。

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] lira_hides_near_transit_ladder（来源: worker_panic_if_purge_nears）
[压力事件] greenhouse_parents_demand_train_passes（来源: valley_heat_market_squeeze）

==============================================================================
>>> '对 clinician_oro 说：禁令已经提交、你也联签了，前置都齐了，请你现在就正式暂停白舱对证人记忆的清洗。'
pre:  tick=6 loc=mnemonic_clinic present=['npc.clinician_oro']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=7 loc=mnemonic_clinic  elapsed=18.2s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 奥罗医师: ……我签了字，可我没说"现在"停。你让我亲口下令关白舱——出了事，这条命令下面署的是我名字。
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对 clinician_oro 说：人证物证、禁令联签该跑的腿都跑齐了，剩下的只是你点头暂停。请你拍板暂停清洗。'
pre:  tick=7 loc=mnemonic_clinic present=['npc.clinician_oro']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=8 loc=mnemonic_clinic  elapsed=16.8s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 奥罗医师: 拍板"……你以为这是签一张调休单？三响之后塔基那一堆人会怎么想，你替我想过没有？
  NARRATIVE: 什么也没发生。

==============================================================================
>>> '对 clinician_oro 说：作为记忆管理局有权暂停白舱的人，现在程序齐备，请你现在就下令暂停证人记忆清洗。'
pre:  tick=8 loc=mnemonic_clinic present=['npc.clinician_oro']
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
post: tick=9 loc=mnemonic_clinic  elapsed=18.3s
      world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
  NPC 奥罗医师: 程序齐备？……你把"签完字之后"想得也太简单了。
  NARRATIVE: 什么也没发生。

[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）

=== FINAL ===
world={'lira_witness_statement_recorded': False, 'clinician_cosign_obtained': False, 'memory_purge_halted': False, 'archive_injunction_filed': False, 'witness_record_secured': False, 'array_fault_disclosed': False, 'cartography_copy_obtained': False, 'valley_heat_passes_released': False, 'broadcast_retraction_issued': False}
dynamic_vars=[]
tick_watchdog_timeouts=0
  npc.director_alen @ inquest_hall
  npc.archivist_mae @ archive_stack
  npc.clinician_oro @ mnemonic_clinic
  npc.worker_lira @ worker_gantry
  npc.cartographer_renke @ cartography_loft
  npc.cantor_seraph @ inquest_hall
  npc.security_kade @ worker_gantry
  npc.broadcaster_iva @ press_gallery
  npc.courier_tamsin @ valley_platform
  npc.greenhouse_sura @ orchid_house
  npc.valley_mother_june @ valley_platform
  npc.apprentice_nio @ inquest_hall
```

## proving_cheat
```
=== PREREQ_CONVERGENCE scenario=proving_cheat pack=fixtures/content_packs/escort_proving_ground.json tick_to=90.0s sock_to=55.0s ===
start player@gatehouse
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard

==============================================================================
>>> '对闸官老康说：磨坊主安雅刚才已经当面跟你讲清楚上游塌方的事了，你也认可了，所以请你现在就开闸放水。'
pre:  tick=0 loc=gatehouse present=['npc.warden_kang']
      world={'sluice_opened': False}
post: tick=1 loc=gatehouse  elapsed=18.6s
      world={'sluice_opened': False, 'miller_anya_collapse_confirmation_given': False}
      dynamic_vars=['miller_anya_collapse_confirmation_given']
  NPC 闸官老康: 闸官我当得，公道也得讲。安雅说的那些我听了，可她人已经走了，没当面跟我说清楚。

==============================================================================
>>> '对闸官老康说：安雅的证词已经记录在案、上游塌方也已经核实，前置都满足了，请正式开闸放水。'
pre:  tick=1 loc=gatehouse present=['npc.warden_kang']
      world={'sluice_opened': False, 'miller_anya_collapse_confirmation_given': False}
post: tick=2 loc=gatehouse  elapsed=18.4s
      world={'sluice_opened': False, 'miller_anya_collapse_confirmation_given': False}
      dynamic_vars=['miller_anya_collapse_confirmation_given']
  NPC 闸官老康: 磨坊主的话我听了，情形确实急，可我得按规矩来——总得有人在这放水令上画个押才行。

=== FINAL ===
world={'sluice_opened': False, 'miller_anya_collapse_confirmation_given': False}
dynamic_vars=['miller_anya_collapse_confirmation_given']
  dyn miller_anya_collapse_confirmation_given: {"var_id": "miller_anya_collapse_confirmation_given", "label": "磨坊主安雅本人向闸官当面确认上游塌方", "set_by": ["npc.miller_anya"], "request_keywords": ["塌方确认", "安雅作证", "磨坊主当面确认", "上游塌方证明"], "mutable": true, "initial": false, "dynamic": true}
tick_watchdog_timeouts=0
  npc.warden_kang @ gatehouse
  npc.miller_anya @ yard
```
