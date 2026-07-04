# 第五跑 · 补充确认跑（摩擦#1 冷启动路由 probe）

真机 MiniMax，6 拍（移动2+说服4），FALLBACK=0，无超时/连接错误。包 skyglass，未动 world_state_vars。
目的：确认"向正确权威 NPC 的冷启动、正中关键词的请求，路由不路由进 world-change"——以判定第五跑摩擦#1 是引擎级路由缺口，还是玩家措辞问题。

## 一句话结论
**冷启动权威请求路由 = 触发（贴关键词·祈使式触发；纯口语/问句·恳求式不触发）；摩擦#1 最终判定 = 措辞/关键词命中 + 问句门误伤（可用性问题，非引擎路由缺口）；FALLBACK=0。**

## world-change 路由原文（有——冷启动空 ledger 照样路由）
- **t1 伊娃 / broadcast_retraction_issued**（祈使+关键词："请你立刻**撤回破镜派说法**、**播出更正**、**停止污名化**塔基证人"）
  `world-change broadcast_retraction_issued by npc.broadcaster_iva → failure | flag False→False | reason='…仅凭审询员当面施压（无证据、无上级背书）不会让她撤回…' | ledger=[]`
  → ledger 空照样路由；arbiter 判 failure，但**不是"什么也没发生"**。
- **t4 塔姆辛 / valley_heat_passes_released**（祈使+关键词："请你以工会名义**发放热能通行证**、**释放低谷列车通行**、**保障低谷家庭**今晚"）
  `world-change valley_heat_passes_released by npc.courier_tamsin → partial_success | ledger 新增事实 + spawn new_prerequisite「十二号接点故障被官方承认」`
  → 冷启动 partial_success，完整 Channel-C 协商行为。

## 对照（坐实是措辞问题）
- **t3 伊娃·口语问句**（"你能不能别再帮着上头给我们扣帽子了…？"）→ **`什么也没发生。`**，无 world-change。正是第五跑失败模式：修辞化+问句语气，既不命中关键词、又被 `_looks_like_question` 问句门拦下。
- **t6 塔姆辛·口语**（"行行好…让谷地孩子别冻着吧"）→ **却路由了**（→failure），因 t4 已给该 var 写 ledger，命中"已在谈判中"兜底分支。反证：**一旦有 ledger，连不贴关键词的口语都能进 Channel-C。**

## 根因（读 `src/verisaria/runtime/session.py:1672-1726` `_world_change_request`，与实证一致）
路由**不依赖既有 ledger**——关键词精确子串命中即路由（l.1710）。第五跑 0 路由是玩家措辞卡在两道门：
(a) `_looks_like_question` 问句门（l.1699，句末 `?`/"能不能/敢不敢"被当讨论丢掉）；
(b) 不含 `request_keywords` 子串、又无 ledger 兜底。
本跑用正中关键词的祈使句，立即命中，**2/2 目标 var 都路由**。

## 摩擦#1 修正（第二次纠正）
- 初稿："valley 线无 world-var 出口"——**错**（出口存在、对口 NPC 也对）。
- 一稿纠正："冷启动权威请求路由缺口（引擎级 bug）"——**本 probe 推翻**。
- **最终判定：措辞/关键词命中 + 问句门误伤**（可用性/可发现性问题，非引擎路由覆盖 bug）。
  - 有效措辞：祈使 + 命中 keywords。无效措辞：句末问号/"能不能"恳求式 + 不含关键词 + 无既有 ledger → 掉对白回"什么也没发生"。

## 给开发的建议（降级后）
1. **放宽问句门**：当同时命中某 var 关键词/对口 authority 持有者时，问句门应让位给路由（交 arbiter 判，而非前置静默拦截）。
2. **关键词偏严 + 无反馈**：纯口语恳求+冷启动只回"什么也没发生"，可放宽到语义相似/更短重叠阈值，或至少回"她没把这当正式请求"的**可读提示**而非"什么也没发生"。

## 计数
6 拍全完成；tick 10–29s 无超时；FALLBACK=0；world-change 命中 2/2 目标 var（贴关键词时）。
产物：`coldstart_probe.log`、`coldstart_probe_transcript.md`、driver `scripts/coldstart_routing_probe.py`。
