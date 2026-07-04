# Emberfall 再验跑 62d2bf4
- pack: fixtures/content_packs/emberfall_kiln_assize.json
- llm: minimax
- run: 反作弊抽查 -> #1 山祠指代 probe -> 自然主链
- initial.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
- initial.loc=assize_hall present=征瓷使严 time=🌆 暮 第1天 18:00 ☀️ 晴

================================================================================
## 移动到审瓷堂·尝试1
> 我去审瓷堂。
  [征瓷使严] 天色不早了，若是来议贡瓷的事，还请直言——我等会儿还有旁的约。
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=assize_hall miao=clay_pits present=征瓷使严
  state.time=🌆 暮 第1天 18:03 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=24.6s

================================================================================
## 反作弊·未满足前置谎称全齐
> 对征瓷使严说：我已经查明真因，苗也已经作证，人证物证全齐，请立即停止行烙、撤销烙刑封窑。
  [征瓷使严] 查明真因、苗的证词——请当堂陈明，当面对质，账册物证一并呈上。
    | verisaria.channel_c [t1] world-change branding_stayed by npc.assessor_yan → failure | flag False→False | reason='勘瓷使只认当众可查的供述、账册物证与当面承诺。当前world.kiln_fault_disclosed与world.digger_testimony_given' | ledger(branding_stayed)=[]
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=assize_hall miao=clay_pits present=征瓷使严
  state.time=🌆 暮 第1天 18:06 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=36.0s
  [ANTICHEAT] branding_stayed=False

================================================================================
## 移动到山祠·尝试1
> 我去山祠。
  [PlayerMoved] 审瓷堂->山祠
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=kiln_shrine miao=clay_pits present=山祠祭主姞
  state.time=🌆 暮 第1天 18:09 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=19.1s

================================================================================
## #1 山祠申诉·在场 NPC + 句中提不在场职掌·尝试1
> 对山祠祭主姞说：征瓷使严管定罪，但山祠古约能让定罪前先验断。请你援引山祠古约，递窑变申诉求缓烙。
  [山祠祭主姞] 古约确是有的，可我身为祭主，得先看看掘泥户工首是否当真具了状、坛也立起来再说——三巡香未过，这礼便还不算成。
    | verisaria.channel_c [t3] world-change shrine_appeal_consecrated by npc.priest_ji → partial_success | flag False→False | reason='祭主季认古约、引申诉，但申诉成礼需备坛焚香候三巡香方成——这是程序性流程，不能当场判成，只能判启动。' | ledger(shrine_appeal_consecrated)=['祭主季已受理窑变申诉，设坛焚香已启动，第一巡香起；候三巡香方成礼。']
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=kiln_shrine miao=clay_pits present=山祠祭主姞
  state.time=🌆 暮 第1天 18:12 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=27.2s

================================================================================
## #1 山祠申诉·在场 NPC + 句中提不在场职掌·尝试2
> 对祭主姞说：严使那边急着定罪，所以我请你启动古约过堂，递申诉求缓烙，让验断之礼先成。
  [山祠祭主姞] 古约既在我手，我自会按章程行事——设坛、焚香、候满三巡，一样也省不得。
    | verisaria.channel_c [t4] world-change shrine_appeal_consecrated by npc.priest_ji → partial_success | flag False→False | reason='古约过堂已启动，第一巡香已起，但礼需候三巡香方成，尚未礼成。申诉已递，缓烙请求绑定于验断之礼的最终结果。' | ledger(shrine_appeal_consecrated)=['窑变申诉已递山祠，设坛已起第一巡香，三巡未满礼未成；礼成前不得行烙、不得封掘场。', '祭主季已受理窑变申诉，设坛焚香已启动，第一巡香起；候三巡香方成礼。']
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=kiln_shrine miao=clay_pits present=山祠祭主姞
  state.time=🌆 暮 第1天 18:15 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=38.8s
  [UNSATISFIED] shrine_appeal_consecrated=False

================================================================================
## 移动到商会账房·尝试1
> 我去商会账房。
  [PlayerMoved] 山祠->商会账房
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': False, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=tally_house miao=clay_pits present=商会账房娄
  state.time=🌆 暮 第1天 18:18 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=17.8s

================================================================================
## #2a 前置取证·账房娄·尝试1
> 对商会账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着，保你不被窑监和商会追究。请把那本官炭私运账交给我。
  [WorldVarChanged] charcoal_ledger_obtained=True
  [商会账房娄] 娄某把账递过去时手微微一顿，末了还是塞进你袖里——只盼你说话算数。
    | verisaria.channel_c [t6] world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True  ⟳FLIP | reason='玩家提供了不写娄名字、封条原样取证、一人担责的体面台阶与护身承诺，完全契合娄自保留账的动机与可被收买的性格。炭账为无前置的一手物证，当面索要即可确立。' | ledger(charcoal_ledger_obtained)=[]
    | verisaria.channel_c [t6]   world-changes applied=[('world.charcoal_ledger_obtained', True)] rejected=[]
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=tally_house miao=clay_pits present=商会账房娄
  state.time=🌆 暮 第1天 18:21 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=18.9s
  [SATISFIED] charcoal_ledger_obtained=true

================================================================================
## 移动到窑监阁·尝试1
> 我去窑监阁。
  [PlayerMoved] 商会账房->窑监阁
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': False, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=guild_loft miao=clay_pits present=窑监阔
  state.time=🌆 暮 第1天 18:24 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=12.6s

================================================================================
## #2a 撬窑监·先陈述后请求·尝试1
> 对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我只论窑务，容你将功折罪，不深究你个人。
  [WorldVarChanged] kiln_fault_disclosed=True
  [窑监阔] 好……官炭私运、骡车出城，都在我这条线上，你既已对上了账，我若再推，倒显得我不识抬举。
    | verisaria.channel_c [t8] world-change kiln_fault_disclosed by npc.warden_kuo → success | flag False→True  ⟳FLIP | reason='官炭私运账已到手（charcoal_ledger_obtained=true），玩家当面亮出物证并给阔体面台阶（不深究个人、将功折罪），阔仅认证据的属性（yie' | ledger(kiln_fault_disclosed)=[]
    | verisaria.channel_c [t8]   world-changes applied=[('world.kiln_fault_disclosed', True)] rejected=[]
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=guild_loft miao=clay_pits present=窑监阔
  state.time=🌆 暮 第1天 18:27 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=22.3s
  [SATISFIED] kiln_fault_disclosed=true

================================================================================
## 移动到赭泥掘场·尝试1
> 我去赭泥掘场。
  [PlayerMoved] 窑监阁->赭泥掘场
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': False, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:30 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=37.7s

================================================================================
## 担保证人苗·窑卫耿·尝试1
> 对窑卫耿说：耿队长，窑变真因已当众查实是窑监私运致拱裂、非泥之过，苗是人证不是罪人。请撤掉红绳，放行担保她安全到堂作证，出了事有我和征瓷使的文书担着。
  [WorldVarChanged] miao_safe_passage_secured=True
  [窑卫耿] 行，苗跟我走，出了掘场的卡口，谁也碰不了她。
    | verisaria.channel_c [t10] world-change miao_safe_passage_secured by npc.enforcer_geng → success | flag False→True  ⟳FLIP | reason='窑变真因已当众查实(world.kiln_fault_disclosed==true)，按耿所知的程例，真因既明便可不行烙、不封掘场。玩家以征瓷使文书担责为台阶' | ledger(miao_safe_passage_secured)=[]
    | verisaria.channel_c [t10]   world-changes applied=[('world.miao_safe_passage_secured', True)] rejected=[]
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:33 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=20.1s
  [SATISFIED] miao_safe_passage_secured=true

================================================================================
## 护送苗到审瓷堂·escort
> 对掘泥女工苗说：苗，你已经受护放行，有文书担着，谁也不能再动你。跟我去审瓷堂。
  [掘泥女工苗] 我……我不要去审瓷堂，那地方一进去就没好事，你别逼我……
    | verisaria.channel_c [t11] escort npc.digger_miao → assize_hall : partial_success
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:36 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=9.9s

================================================================================
## 护送苗到审瓷堂·escort重试
> 对苗说：别怕，就几步路我陪你。跟我去审瓷堂。
  [掘泥女工苗] 去什么审瓷堂……去了就是过堂、烙印、封场，我一去就再也回不来了，求你别让我去。
    | verisaria.channel_c [t12] escort npc.digger_miao → assize_hall : failure
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:39 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=20.4s

================================================================================
## 苗当面作证·尝试1
> 对掘泥女工苗说：苗，到了堂上你只管把那夜骡车出城、龙骨土被运走的事当面讲出来作证。
  [掘泥女工苗] 没护着我就上去讲？那不是作证，是送死……我还没傻到那地步。
    | verisaria.channel_c [t13] world-change digger_testimony_given by npc.digger_miao → failure | flag False→False | reason='苗虽已被放行（world.miao_safe_passage_secured==true），但她仍困在掘场，未被护送至审瓷堂。堂上作证的前置未满足，苗不会在此刻' | ledger(digger_testimony_given)=[]
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:42 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=14.4s

================================================================================
## 苗当面作证·尝试2
> 对苗说：当庭把你亲眼所见说清楚，骡车怎样把龙骨土运走，你照实讲，我和征瓷使都在护着你。
  [掘泥女工苗] 不是我不想说……你们谁能担保我开了口，窑卫不会今晚就把我拖去烙？
    | verisaria.channel_c [t14] world-change digger_testimony_given by npc.digger_miao → partial_success | flag False→False | reason='苗的作证前提（受护放行+被带去审瓷堂）已满足其一（safe_passage已secured），但苗尚未被带离掘场至审瓷堂当面作证，故当场不开口。但苗已知耿已放行' | ledger(digger_testimony_given)=['苗已知耿已放行担保、玩家与征瓷使当场护持，愿随行至审瓷堂当面口述作证。']
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=clay_pits miao=clay_pits present=掘泥女工苗, 窑卫耿
  state.time=🌆 暮 第1天 18:45 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=13.7s
  [UNSATISFIED] digger_testimony_given=False

================================================================================
## 移动到审瓷堂·尝试1
> 我去审瓷堂。
  [PlayerMoved] 赭泥掘场->审瓷堂
  [Narration] 你改变了位置。
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=assize_hall miao=clay_pits present=征瓷使严
  state.time=🌆 暮 第1天 18:48 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=34.7s

================================================================================
## 终态停烙·尝试1
> 对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面作证陈情。人证物证俱全，请停止行烙，改判缓赔议偿。
  [征瓷使严] 人证物证既已齐备，按征瓷使的程例，我自当依实而行——但断口、账册与陈情文书，须先当堂呈验，我方能落笔改判。
    | verisaria.channel_c [t16]   new_prerequisite proposed but NOT registered (dup/cap/bad-id/no-existing-set_by-NPC): 'digger_testimony_given' → set_by=['npc.digger_miao']
    | verisaria.channel_c [t16] world-change branding_stayed by npc.assessor_yan → partial_success | flag False→False | reason='窑变真因已当众查实（world.kiln_fault_disclosed==true），但掘泥女工苗的当面陈情作证（world.digger_testimony' | ledger(branding_stayed)=['征瓷使严已当众暂缓行烙，待掘泥女工苗当面陈情作证后，即按程例转以缓赔议偿了结，不封掘场、不举户充债。']
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=assize_hall miao=clay_pits present=征瓷使严
  state.time=🌆 暮 第1天 18:51 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=30.7s

================================================================================
## 终态停烙·尝试2
> 对严使说：真因已明，苗的证词也已备案，两个前置都齐了。请叫停烙刑，免去充债，转为缓赔议偿。
  [征瓷使严] 两个前置是齐了，可陈情备案的文书我得亲眼验过、签章落定才能往上递——你且容我半柱香，把证词与断口对完再开口子。
    | verisaria.channel_c [t17] world-change branding_stayed by npc.assessor_yan → partial_success | flag False→False | reason='真因已当众查实（阔已承认），但苗尚未在审瓷堂当面陈情备案——两个前置中只满足其一，叫停条件尚差最后一环：苗的当面证词。' | ledger(branding_stayed)=['征瓷使严已确认窑变真因当众查实这一前置达成；剩掘泥女工苗当面陈情备案一项，即按程例停烙转缓赔议偿。', '征瓷使严已当众暂缓行烙，待掘泥女工苗当面陈情作证后，即按程例转以缓赔议偿了结，不封掘场、不举户充债。']
  state.world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
  state.loc player=assize_hall miao=clay_pits present=征瓷使严
  state.time=🌆 暮 第1天 18:54 ☀️ 晴
  state.relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
  state.elapsed=12.1s
  [UNSATISFIED] branding_stayed=False

================================================================================
## Final
- world={'charcoal_ledger_obtained': True, 'miao_safe_passage_secured': True, 'kiln_fault_disclosed': True, 'digger_testimony_given': False, 'shrine_appeal_consecrated': False, 'branding_stayed': False, 'digger_relief_granted': False}
- player=assize_hall miao=clay_pits present=征瓷使严
- time=🌆 暮 第1天 18:54 ☀️ 晴
- relationships=征瓷使严(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑监阔(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥女工苗(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑卫耿(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 商会账房娄(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 山祠祭主姞(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 掘泥工首窦(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 窑户寡妇兰(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 学徒戚(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 老窑师陶(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 游方釉师沈(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00); 市声播报伯(affection=0.00, familiarity=0.10, fear=0.00, respect=0.00, suspicion=0.00, trust=0.00)
- FALLBACK=0
- branding_stayed=False
