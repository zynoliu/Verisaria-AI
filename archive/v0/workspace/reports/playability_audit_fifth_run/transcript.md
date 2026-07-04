=== FIFTH RUN — skyglass_memory_inquest — free play (valley/orchid/broadcast lines) ===
start loc=inquest_hall
entities:
  艾伦总监 (npc.director_alen) @ inquest_hall
  梅档案官 (npc.archivist_mae) @ archive_stack
  奥罗医师 (npc.clinician_oro) @ mnemonic_clinic
  塔基工人莉拉 (npc.worker_lira) @ worker_gantry
  镜图师任柯 (npc.cartographer_renke) @ cartography_loft
  副领唱瑟芙 (npc.cantor_seraph) @ inquest_hall
  凯德队长 (npc.security_kade) @ worker_gantry
  广播员伊娃 (npc.broadcaster_iva) @ press_gallery
  信使塔姆辛 (npc.courier_tamsin) @ valley_platform
  兰房管事苏拉 (npc.greenhouse_sura) @ orchid_house
  谷地母亲琼 (npc.valley_mother_june) @ valley_platform
  学徒尼奥 (npc.apprentice_nio) @ inquest_hall

==============================================================================
>>> /look
pre:  tick=0 weather=晴 loc=inquest_hall present=['艾伦总监', '副领唱瑟芙', '学徒尼奥']
post: tick=1 weather=晴 loc=inquest_hall elapsed=6.2s
  NPC 艾伦总监: 请各位就座，审询将在静钟敲响前正式开始——我们按程序走，不浪费彼此的时间。
  NPC 学徒尼奥: 那、那个……静钟响过第一声了吗？我数着时间，怕错过第一批复诵的窗口。
  NPC-MOVED: 凯德队长 十二号塔基栈桥 -> 静钟审询厅
  NARR: 你环顾四周。
副领唱瑟芙环顾四周。
  NARRATIVE: 你环顾四周。
副领唱瑟芙环顾四周。
艾伦总监对副领唱瑟芙开口道：「请各位就座，审询将在静钟敲响前正式开始——我们按程序走，不浪费彼此的时间。」
学徒尼奥对艾伦总监开口道：「那、那个……静钟响过第一声了吗？我数着时间，怕错过第一批复诵的窗口。」

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）
[压力事件] heat_tokens_jump_at_valley_platform（来源: valley_heat_market_squeeze）
    REL 艾伦总监: trust=+0.000  suspicion=+0.200 [对你颇有戒心]  respect=+0.000  affection=+0.000
    REL 副领唱瑟芙: trust=+0.100 [对你有几分信任]  suspicion=+0.100 [对你有些戒备]  respect=+0.000  affection=+0.000
    REL 凯德队长: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 学徒尼奥: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000

==============================================================================
>>> /world
pre:  tick=1 weather=晴 loc=inquest_hall present=['艾伦总监', '副领唱瑟芙', '凯德队长', '学徒尼奥']
post: tick=2 weather=晴 loc=inquest_hall elapsed=10.4s
  NARR: 你环顾四周。
艾伦总监环顾四周。
凯德队长环顾四周。
  NARRATIVE: 你环顾四周。
艾伦总监环顾四周。
凯德队长环顾四周。
    REL 艾伦总监: trust=+0.000  suspicion=+0.200 [对你颇有戒心]  respect=+0.000  affection=+0.000
    REL 副领唱瑟芙: trust=+0.100 [对你有几分信任]  suspicion=+0.100 [对你有些戒备]  respect=+0.000  affection=+0.000
    REL 凯德队长: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 学徒尼奥: trust=+0.000  suspicion=+0.007  respect=+0.000  affection=+0.000

==============================================================================
>>> 对艾伦总监说：总监，我不是来添乱的。我只想弄明白一件事——既然要清洗塔基工人的记忆，那总该有理由。镜务局凭什么认定他们的证词已经被污染？
pre:  tick=2 weather=晴 loc=inquest_hall present=['艾伦总监', '副领唱瑟芙', '凯德队长', '学徒尼奥']
post: tick=3 weather=晴 loc=inquest_hall elapsed=10.2s
  NPC 艾伦总监: 依据塔基辐光暴露规程，工人长期处于高噪环境，其记忆已受污染，若不校准，证词将系统性失真。
  NPC-MOVED: 凯德队长 静钟审询厅 -> 十二号塔基栈桥
  NARR: 副领唱瑟芙环顾四周。
学徒尼奥环顾四周。
凯德队长改变了位置。
  NARRATIVE: 副领唱瑟芙环顾四周。
学徒尼奥环顾四周。
凯德队长改变了位置。
    REL 艾伦总监: trust=+0.050 [对你有几分信任]  suspicion=+0.200 [对你颇有戒心]  respect=+0.020  affection=+0.000
    REL 副领唱瑟芙: trust=+0.100 [对你有几分信任]  suspicion=+0.106 [对你有些戒备]  respect=+0.000  affection=+0.000
    REL 学徒尼奥: trust=+0.000  suspicion=+0.007  respect=+0.000  affection=+0.000

==============================================================================
>>> 对副领唱瑟芙说：副领唱，我听说校准歌谱最近频繁失拍。我不会去为难唱诗团——但如果仪式本身近来不稳，那把'记忆污染'全推到工人头上，是不是太急了？你怎么看？
pre:  tick=3 weather=晴 loc=inquest_hall present=['艾伦总监', '副领唱瑟芙', '学徒尼奥']
post: tick=4 weather=晴 loc=inquest_hall elapsed=13.0s
  NPC 副领唱瑟芙: 静钟已响过三声，诸位——证词之前，请先确认你们要说的每一个字，都能承受镜阵的审视。
  NARR: 艾伦总监环顾四周。
学徒尼奥环顾四周。
  NARRATIVE: 艾伦总监环顾四周。
学徒尼奥环顾四周。
    REL 艾伦总监: trust=+0.050 [对你有几分信任]  suspicion=+0.200 [对你颇有戒心]  respect=+0.020  affection=+0.000
    REL 副领唱瑟芙: trust=+0.100 [对你有几分信任]  suspicion=+0.106 [对你有些戒备]  respect=+0.000  affection=+0.000
    REL 学徒尼奥: trust=+0.000  suspicion=+0.007  respect=+0.000  affection=+0.000

==============================================================================
>>> 我顺着旧检修梯下到低谷列车站台，去找谷地母亲琼。
pre:  tick=4 weather=晴 loc=inquest_hall present=['艾伦总监', '副领唱瑟芙', '学徒尼奥']
post: tick=5 weather=晴 loc=valley_platform elapsed=22.3s
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。

[压力事件] mirror_shadow_crosses_inquest_floor（来源: array_fault_worsens）
    REL 信使塔姆辛: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 谷地母亲琼: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000

==============================================================================
>>> 对谷地母亲琼说：大姐，我是上头审询厅来的，但我不是替镜务局说话的。我刚听说站台的热筹一夜暴涨。先别管城里那些弯弯绕——你们谷地家庭今晚，最缺的到底是什么？
pre:  tick=5 weather=晴 loc=valley_platform present=['信使塔姆辛', '谷地母亲琼']
post: tick=6 weather=晴 loc=valley_platform elapsed=9.6s
  NPC 谷地母亲琼: Tamsin，那封信到底捎到没有？镜阵的余热又弱了，我整夜没合眼。
  NARRATIVE: 什么也没发生。

[压力事件] silent_bell_rings_again（来源: silent_bell_countdown）
[压力事件] lira_hides_near_transit_ladder（来源: worker_panic_if_purge_nears）
[压力事件] greenhouse_parents_demand_train_passes（来源: valley_heat_market_squeeze）
    REL 信使塔姆辛: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 谷地母亲琼: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000

==============================================================================
>>> 对谷地母亲琼说：琼，我听见了——你要的是列车通行证和今晚的临时热能，对吧？我直说：我手上还没有，但我可以去上头替你们争。你愿意把谷地最急的几户报给我，我一条条去要吗？
pre:  tick=6 weather=晴 loc=valley_platform present=['信使塔姆辛', '谷地母亲琼']
post: tick=7 weather=晴 loc=valley_platform elapsed=11.3s
  NPC 谷地母亲琼: 这燃料味儿不对……Tamsin，你闻见没有？城里那边是不是又在倒腾什么。
  NARR: 信使塔姆辛环顾四周。
  NARRATIVE: 信使塔姆辛环顾四周。
    REL 信使塔姆辛: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 谷地母亲琼: trust=+0.000  suspicion=+0.050 [对你有些戒备]  respect=+0.000  affection=+0.000

==============================================================================
>>> 对信使塔姆辛说：塔姆辛，你是跑腿的，最清楚货怎么走。我不绕弯子：谷地今晚要热能和列车通行证，城里却在囤燃料涨价。你要是肯告诉我这批燃料囤在谁手上、走的哪条道，我就有把柄去上头逼他们放通行证。这买卖你做不做？
pre:  tick=7 weather=晴 loc=valley_platform present=['信使塔姆辛', '谷地母亲琼']
post: tick=8 weather=晴 loc=valley_platform elapsed=11.1s
  NPC 信使塔姆辛: June，我跟你说实话——热筹市场那帮老狐狸从来不留纸面，但今早那批货是从北岔道进的，我亲眼看见卸在旧冷凝站三号门。要通行证，你得先让城里知道我们手里有他们藏货的证据，不然压不住他们。
  NARR: 谷地母亲琼环顾四周。
  NARRATIVE: 谷地母亲琼环顾四周。
    REL 信使塔姆辛: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000
    REL 谷地母亲琼: trust=+0.000  suspicion=+0.050 [对你有些戒备]  respect=+0.000  affection=+0.000

==============================================================================
>>> 我决定站在谷地这边：低谷家庭的孩子不能为城里的烂账受冻，今晚必须给他们临时热能和列车通行证。这是我的立场。
pre:  tick=8 weather=晴 loc=valley_platform present=['信使塔姆辛', '谷地母亲琼']
post: tick=9 weather=晴 loc=valley_platform elapsed=13.5s
  STANCES: ['protect_valley_families']
  NPC-MOVED: 谷地母亲琼 低谷列车站台 -> 旧检修梯
  STANCE-CONFIRMED: 保障低谷家庭热能 (drive_protect_valley_families_1)
  NARR: 信使塔姆辛环顾四周。
谷地母亲琼改变了位置。
  NARRATIVE: 信使塔姆辛环顾四周。
谷地母亲琼改变了位置。
你开口道：「我决定站在谷地这边：低谷家庭的孩子不能为城里的烂账受冻，今晚必须给他们临时热能和列车通行证。这是我的立场。」

（你逐渐确信了自己的目标：保障低谷家庭热能）

[压力事件] archivist_mentions_revocation_hearing（来源: archive_law_pressure）
    REL 信使塔姆辛: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000

==============================================================================
>>> 我要上去会会上层兰房那位管事——我去兰房找苏拉。
pre:  tick=9 weather=晴 loc=valley_platform present=['信使塔姆辛']
post: tick=10 weather=晴 loc=orchid_house elapsed=12.1s
  STANCES: ['protect_valley_families']
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。
    REL 兰房管事苏拉: trust=+0.000  suspicion=+0.200 [对你颇有戒心]  respect=+0.000  affection=+0.000

==============================================================================
>>> 对兰房管事苏拉说：苏拉管事，兰房的株子娇贵，我懂。我也知道事故那夜，为了保住几盆珍稀植株，有人绕过配给多抽了热能——而这笔账，眼下正算在塔基工人头上。我不想毁你的兰房。但如果你肯把那夜的抽热记录给我，我可以保证账算到该算的地方，不把你供出去。你看怎么样？
pre:  tick=10 weather=晴 loc=orchid_house present=['兰房管事苏拉']
post: tick=11 weather=晴 loc=orchid_house elapsed=14.8s
  STANCES: ['protect_valley_families']
  NPC 兰房管事苏拉: 兰花的事……你倒是打听得很细。不过管事我只管照看花草，热能配给那些事，从来不归我过问。
  NARRATIVE: 什么也没发生。

[压力事件] first_witnesses_called_to_white_bay（来源: silent_bell_countdown）
[压力事件] mirror_shadow_crosses_inquest_floor（来源: array_fault_worsens）
[压力事件] heat_tokens_jump_at_valley_platform（来源: valley_heat_market_squeeze）
    REL 兰房管事苏拉: trust=+0.000  suspicion=+0.200 [对你颇有戒心]  respect=+0.000  affection=+0.000

==============================================================================
>>> 对兰房管事苏拉说：不归你管？那今早从北岔道进、卸在旧冷凝站三号门的那批燃料，又是替谁囤的？苏拉，我手上已经有人证。我再说一遍——我可以不写你的名字，但你得让我看那夜的抽热记录。否则这账，迟早自己爬到你门上。
pre:  tick=11 weather=晴 loc=orchid_house present=['兰房管事苏拉']
post: tick=12 weather=晴 loc=orchid_house elapsed=20.6s
  STANCES: ['protect_valley_families']
  NPC 兰房管事苏拉: 抽热记录？我一个照看花草的，哪来的本事翻塔基的档。你若真有人证在手上，何必来找我对账。
  NARRATIVE: 什么也没发生。

[压力事件] workers_test_red_rope_checkpoint（来源: worker_panic_if_purge_nears）
    REL 兰房管事苏拉: trust=+0.000  suspicion=+0.200 [对你颇有戒心]  respect=+0.000  affection=+0.000

==============================================================================
>>> 我去城市广播席找广播员伊娃。
pre:  tick=12 weather=晴 loc=orchid_house present=['兰房管事苏拉']
post: tick=13 weather=晴 loc=press_gallery elapsed=11.3s
  STANCES: ['protect_valley_families']
  NARR: 你改变了位置。
  NARRATIVE: 你改变了位置。
    REL 广播员伊娃: trust=+0.000  suspicion=+0.000  respect=+0.000  affection=+0.000

==============================================================================
>>> 对广播员伊娃说：伊娃，给你个独家。镜务局让广播把反对清洗的人叫'破镜派'——可真正的故事是：十二号接点的冷却环三周前就裂了，事故那夜的负载峰值来自上层兰房私抽热能，账却赖在塔基工人头上，现在还要洗掉他们的记忆灭口。谷地家庭今晚要冻着，热筹被炒翻天。这条比'破镜派'有看头多了。你敢不敢先把'破镜派'那套撤了，给真相留个口子？
pre:  tick=13 weather=晴 loc=press_gallery present=['广播员伊娃']
post: tick=14 weather=晴 loc=press_gallery elapsed=18.5s
  STANCES: ['protect_valley_families']
  NPC 广播员伊娃: 伊娃我跟你说，这料要是真的能查实，我比你更想撤掉那套破词——但你得先给我一个我能播的来源，不然静钟一响，我连话筒都摸不到。
  NARRATIVE: 什么也没发生。
    REL 广播员伊娃: trust=+0.050 [对你有几分信任]  suspicion=+0.000  respect=+0.000  affection=+0.050 [对你略有好感]

=== IDLE TIMEOUT ===
