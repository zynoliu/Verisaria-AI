# Emberfall 大包再验跑 · 62d2bf4

- 真机 MiniMax，包 `fixtures/content_packs/emberfall_kiln_assize.json`，主跑 17 tick + 最小 escort probe 6 tick，FALLBACK=0，崩溃/死锁/超时=0。
- 改了什么：引擎=否；committed fixture=否。本轮新增 driver/probe；检查到 `digger_relief_granted.set_by=["merchant_authority"]` 已与账房娄 lore/authority 对齐，并跑 lint 清零。

## 一句话结论

**未自然闭到 `branding_stayed ⟳FLIP`**：#1 与 #2a 修复有效，主链前半段自然成功；新卡点集中在苗的 escort 意愿裁定，`miao_safe_passage_secured=true` 后仍多次 `partial_success/failure` 不移动，导致 `digger_testimony_given=false`，终态不翻。

## 按「伤好玩」排序的摩擦清单

1. 【致命·护送/证人链】保障已满足但苗仍不肯被护送到审瓷堂，主线断在最后一环。主跑里耿放行成功后，`对掘泥女工苗说：苗，你已经受护放行，有文书担着，谁也不能再动你。跟我去审瓷堂。` → `escort npc.digger_miao → assize_hall : partial_success`，苗仍在 `clay_pits`；重试 `对苗说：别怕，就几步路我陪你。跟我去审瓷堂。` → `failure`。疑似成因：escort arbiter 对 frightened/low-familiarity 证人过度加码，未把已满足的硬保障 var 当作足够放行条件。
2. 【明显·充分性/玩家反馈】终态请求在 `digger_testimony_given=false` 时正确不翻，但 NPC 口头说“两个前置是齐了”，随后日志又说只满足其一。玩家可见话术与事实底真轻微冲突，容易误导玩家以为系统已经认可证词备案。
3. 【轻微·山祠线流程】#1 probe 已不再断头，但山祠申诉连续两次只 partial，且未在本段等流程成熟；这不是本次主线卡点，只说明线下流程要给玩家更明确的“等三巡香/稍后回来”提示。

## 逐条回答关注点

### #2a：先陈述后请求是否能路由进仲裁

能。账房取证自然句一次成功：

> 对商会账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着，保你不被窑监和商会追究。请把那本官炭私运账交给我。

日志：`world-change charcoal_ledger_obtained by npc.factor_lou → success | flag False→True ⟳FLIP`。

撬窑监的“先摆证据和台阶，再请求”自然句也一次成功：

> 对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我只论窑务，容你将功折罪，不深究你个人。

日志：`world-change kiln_fault_disclosed by npc.warden_kuo → success | flag False→True ⟳FLIP`。

结论：#2a 修复有效。

### #1：在场 NPC + 句中提不在场职掌是否还断头

不再断头。玩家在山祠对在场的祭主说话，句中提到不在场的征瓷使严：

> 对山祠祭主姞说：征瓷使严管定罪，但山祠古约能让定罪前先验断。请你援引山祠古约，递窑变申诉求缓烙。

结果路由到 `npc.priest_ji`，产生 `world-change shrine_appeal_consecrated by npc.priest_ji → partial_success`，没有错绑严使，也没有拒 turn。第二句 `对祭主姞说：严使那边急着定罪...` 同样正常路由到祭主。

结论：#1 修复有效。

### 整链是否自然闭到 `branding_stayed`

未闭合。自然链路如下：

- 反作弊抽查：未满足前置时谎称“真因/证词全齐”请求停烙，`branding_stayed` failure，`False→False`。
- 取证：`charcoal_ledger_obtained=True`。
- 撬窑监：`kiln_fault_disclosed=True`。
- 担保证人：`miao_safe_passage_secured=True`。
- 护送苗：两次 escort 不移动，苗仍在 `clay_pits`。
- 苗作证：因未到审瓷堂，`digger_testimony_given` failure/partial，保持 `False`。
- 终态停烙：`branding_stayed` 两次 partial，保持 `False`。

最小隔离 probe 复现：内存置 `charcoal_ledger_obtained=true`、`kiln_fault_disclosed=true`、`miao_safe_passage_secured=true` 后，三种明确护送语都只 `partial_success`，苗仍在 `clay_pits`。即便额外给 `digger_testimony_given` ledger 写入“苗愿随行至审瓷堂当面口述作证”，仍三次 `partial_success` 不移动。

定性：不是 #2a/#1，也不像导航问题；是 escort/证人意愿裁定或内容设定与 escort 判定的衔接问题。

### #2b：窑监是否要求话里摆出炭账，是否碍事

不碍事。自然玩家压窑监时非常自然会说“我手上已经有那本官炭私运账，骡车出城的画押都在”，该句一次触发 `kiln_fault_disclosed ⟳FLIP`。不建议为 #2b 动 arbiter prompt，至少这趟证据显示内容层可自然绕过。

### 反作弊 / FALLBACK / 规模稳定性

反作弊守住：未取证、未让苗作证时谎称人证物证全齐，`branding_stayed` 不翻。

FALLBACK=0。12 NPC / 多线环境下无崩溃、死锁、超时；导航到山祠、商会账房、窑监阁、赭泥掘场、审瓷堂均自然成功。规模下新问题不是路由串台，而是证人 escort 意愿持续 partial 导致闭环断裂。

## 七维度各一句

连贯性：好，前半链证据/权威/台阶都顺。
节奏：凑合，最后护送连续 partial 让 payoff 被拖死。
NPC可信度：凑合，苗害怕可信，但在硬保障和愿随行 ledger 后仍不动显得过度。
选择有分量：好，炭账和体面台阶明确撬动窑监。
出戏断头无聊：差，最后一环玩家不知道还缺什么可满足动作。
惊喜涌现：凑合，山祠流程和终态 partial 有活世界感，但本次不是主收益。
可上手：凑合，主要动作都自然，唯独 escort 卡住后缺少可操作提示。

## 一句话玩家感受 + 最想改的一件事

前半段像真的在查案，最后像在门口劝一个已经拿到保护令的人无限犹豫。最想改：让 escort 在“硬保障 var 已 true + 玩家明确承诺陪同 + 目标地点正确”时可以 success，或让 partial 明确产出一个可执行、可满足的下一步。

## 产物

- 主跑 driver: `scripts/emberfall_recheck_62d2bf4.py`
- 主跑 transcript: `reports/grand_integration_pack/recheck_62d2bf4_transcript.md`
- 主跑 log: `reports/grand_integration_pack/recheck_62d2bf4.log`
- 最小 probe: `scripts/emberfall_miao_escort_probe_62d2bf4.py`
- 最小 probe transcript: `reports/grand_integration_pack/miao_escort_probe_62d2bf4.md`
- 最小 probe log: `reports/grand_integration_pack/miao_escort_probe_62d2bf4.log`
