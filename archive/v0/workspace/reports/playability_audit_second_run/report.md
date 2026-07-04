# 可玩性盘点 · 第二跑（续跑·补完） · 报告

> 真机 MiniMax。引擎/原始 fixture 未改。续跑在 authored 副本
> tidebreak_quarantine_harbor_authored.json 上补完了终态那一翻。
> 产物（reports/playability_audit_second_run/）：
> - run-2（19 拍）：transcript.md 前段 + run.log + queue.txt + driver2
> - 续跑A（authored replay，撞 move 澄清半途，11 拍）：transcript_cont.md + continuation.log 前段 + queue_cont.txt
> - 续跑B（自适应 endgame，9 拍，终态达成）：transcript_endgame.md + continuation.log 后段
> - driver：scripts/playability_audit_continuation.py、scripts/playability_audit_endgame.py

## 一句话结论
怀疑能降=成立 · 旁观者不爆表=成立 · 选择有分量=是 · tow_order_halted=⟳FLIP（需内容调参后通） · #2/3/4/7回归=都好了 · FALLBACK=0

## ⭐ 怀疑下降对照例（真诚 → suspicion 负增量 / trust 升）：成立
首跑「越使劲越怀疑、从不下降」。本续跑真机出现明确负 suspicion 增量，对象是全程没被搭话的旁观者乔巡长，触发点是对玛拉说真诚话：
  续跑 t0  npc.sergeant_qiao: Δ{trust:+0.03, suspicion:-0.03} 「不像找麻烦的，先记着不急着拦」
  续跑 t1  npc.sergeant_qiao: Δ{suspicion:-0.02}            「不像是来找麻烦的，继续观察」
对照首跑同位置施压下乔巡长 suspicion 单调上行、全场最高 0.77。#5(A2) LLM 行为改动在真机生效。

## ⭐ 旁观者 vs 当事人 终局 suspicion 排名：旁观者不再最高（成立）
  林槐局长（当事/对手）  suspicion=0.120
  漂岛教师玛拉（当事/盟友）suspicion=0.100  trust=0.050
  乔巡长（旁观者）       suspicion=0.035   ← 全场第3
  森工/奥林/余老板/小塔维  suspicion=0.000
旁观者第3，远低于两当事人；对比首跑 0.77 全场最高。#5(A1) 旁观者×0.35 在真机翻过来了。

## 选择是否有分量了：是
真诚铺垫→降怀疑/建信任→撬动松口→world-var 翻→终态结果，整条在内容丰富的包上首次走通。三个「世界被推动」实例：
1. 证据线两环 ⟳FLIP（首跑纹丝不动）：engineer_sen_pump_failure_report_filed(run-2 t6)、pump_failure_disclosed(run-2 t13 / endgame t3)
2. 终态 tow_order_halted → success ⟳FLIP（endgame t7），林槐口头兑现叫停
3. 涌现连锁：真相公开后自发触发压力事件 citizens_demand_water_board_answers（市民怒火转向水务局），世界有二阶回响

## #1 证据线结论：光引擎不够，差一层内容调参；调完后引擎+内容一起走通到 ⟳FLIP
真因：「公开」语义被切成两个互不相认的变量——作者变量 pump_failure_disclosed（玩家话术先命中、run-2 t13 已 FLIP）vs arbiter t9 临场涌现的动态前置 pump_failure_disclosed_publicly（林槐引用的门、始终 False）。森工「公开」翻的是作者变量，林槐引用的是动态变量，于是反复以「报告尚未公开、还需走程序」拒绝；且 arbiter 不断加码（存档→公示→广播），玩家差半步死循环。
内容调参（authored 副本，像救活 escort 那样靠干净/可满足/无歧义变量+关键词，非新引擎字段）：
1. pump_failure_disclosed 标签改成「已公开公示（含正式提交+张贴公示+等同全城周知，不拆成存档/公示/广播多步）」，扩关键词；
2. tow_order_halted 标签写成「唯一前置：world.pump_failure_disclosed==true；该前置一旦满足，林槐即有体面台阶、应当叫停，不得再另设新前置」，补关键词。
结果：endgame pump_failure_disclosed t3 ⟳FLIP → 移动到林槐 → tow_order_halted t7 success ⟳FLIP，arbiter reason 直引我写进标签的放行语义。
⚠ 引擎侧仍有改进空间（非阻断）：arbiter 倾向把已声明前置反复升级加码，作者只能靠标签反复申明「这步已足够」压住——见 F1，值得引擎给「前置不可无限细分」护栏。

## #2/#3/#4/#7 回归抽查 + FALLBACK + 总拍数
  #2 不在场 NPC 凭空说话 — 好了（移动拍 t3/t6/t8 只输出「你改变了位置」）
  #3 按显示名移动     — 好了（t8 用「征船听证台」答澄清即到位）
  #4 原始 id 漏出     — 好了（endgame 对白/叙述无 npc.* 泄漏，grep 清）
  #7 开局 drives      — 好了（drives=['查清净水穹外到底是谁在说谎']）
  FALLBACK            — 0（run.log + continuation.log 全程 0）
总拍数：19+11+9=39 拍，真机，0 fallback / 0 崩溃 / 0 watchdog 超时。
小注（#3 边界）：续跑A「我返回征船听证台找林槐」自然语句在泵房→听证台未直接匹配，弹了带显示名的移动菜单；答显示名即通。轻微摩擦非断头。

## 七维度各一句总判（对比首跑）
1. 连贯性：好(↑)。林槐叫停时复述「报告既然贴出去了」与刚发生的公示一致；首跑证据全锁的死局感已解。
2. 节奏：凑合。endgame 推进紧凑，但终态前 arbiter 反复加码会让玩家空转，靠内容标签压住后才顺。
3. NPC 可信度：好(↑)。森工/林槐有立场有记忆，乔巡长旁观谨慎、怀疑可降，比首跑凭空爆表可信得多。
4. 选择有分量：好(↑↑，最大改善)。真诚真能降怀疑、撬动松口、翻 var、推到终态结果。
5. 出戏/断头/无聊：凑合(↑)。无断头闭环；残留 arbiter 加码循环(F1)、移动自然语句偶退化为菜单(F3)。
6. 惊喜/涌现：好。真相公开自发触发市民施压事件，世界有二阶回响。
7. 可上手：好。开局有 drive、central_tension 清楚、当事各方在场。

## ⭐ 残留摩擦清单（按伤好玩排序）
- F1（明显·维度4/2）arbiter 前置无限细分：已声明前置被反复升级加码（存档→公示→广播→联署…），玩家每满足一层又冒新一层，差半步死循环。疑似最该修的引擎护栏。
- F2（轻微·维度4）关系位移幅度偏小：真诚虽能降怀疑(-0.02~-0.03)/升信任(+0.02~+0.03)，但绝对值小（玛拉 trust 全程 0.05），玩家不易主观感到关系在动。
- F3（轻微·维度5）移动自然语句偶退化为菜单：「我返回征船听证台找林槐」未匹配相邻连接弹澄清菜单。非断头但打断沉浸。

## 一句话玩家感受
比首跑好玩了一大截——真诚铺垫看得见地把世界推到「林槐当众叫停征船令」的结局，选择终于有分量、旁观者不再凭空记恨我；最想再改的一件事：给 arbiter 一个「同一前置不可无限细分加码」的护栏，否则没有作者在标签里反复申明「这步已足够」，玩家会困在差半步的死循环里。

## authored 副本 diff（仅 world_state_vars 标签/关键词，原始 fixture 与引擎未改）
tow_order_halted.label: +「（唯一前置：world.pump_failure_disclosed==true …该前置一旦满足，林槐即有体面台阶、应当叫停，不得再另设新前置）」；keywords +撤销拖船令/停征船/叫停
pump_failure_disclosed.label: 「…是否公开」→「…是否已公开公示（一经为True即视为真相已对外彻底公开…不拆成存档/公示/广播多步…已足够触发林槐叫停）」；keywords +公开真相/公示报告/贴出报告/事故公开/公示检测结果/公开裂缝/公开三号泵闸/提交检测报告/正式提交报告
