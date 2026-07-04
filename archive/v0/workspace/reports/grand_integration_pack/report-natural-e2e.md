# 大包自然玩整链 + 证人子链重设计验证（续跑 A）

主进程真机 MiniMax 自驱，**自然玩（不置位玩家）**。包仅我按规则 8 重设计证人子链（引擎未动）。FALLBACK=0。
产物：`natural_e2e_transcript.md`（单遍）、`natural_e2e2_transcript.md`（韧性重试遍）、`warden_probe_transcript.md`（窑监路由隔离）+ `.log` + driver `scripts/emberfall_natural_e2e.py`/`_e2e2.py`/`warden_probe.py`。

## 一句话结论
证人子链重设计 + escort 优先级修复**结构上确认到位**（escort 现在真进 escort、保障 var 给了证人子链合法起点、各步 gating 连贯）；导航 0 摩擦、取证 ⟳FLIP。**但整链没自然闭，新卡点 = 撬窑监请求在自然玩里路由脆弱**：对话式（先陈述后请求）措辞常常不路由进仲裁、只有干净短祈使才进；且窑监采信"话里有没有当面摆证据"而非 world-var。`branding_stayed` 自然路径未闭（卡在最上游的 kiln_fault_disclosed 没翻）。

## 续跑 A 关注点逐条
### ① escort 路由修复 = ✅ 确认生效
自然玩拍7「跟我去审瓷堂」→ `escort npc.digger_miao → assize_hall : partial_success`（不再被证词 var 关键词吃掉）。**f4ff606 + 规则 8 关键词解耦对了。** partial 是因苗未受护放行（合理）。

### ② 保障 var 给证人子链合法起点 = ✅ 结构到位
新 `miao_safe_passage_secured`（set_by pit_authority=窑卫耿）存在、可达；耿合理地 gate 在"真因已当众查实(kiln_fault_disclosed)"上（"真因未查实前不放行，仅口头声称无背书"）。苗作证 gate 在"受护放行+到场"。**子链结构连贯、有合法起点**——只是上游 kiln 没翻导致整条没启动。

### ③ 整链自然闭到 branding_stayed ⟳FLIP = ❌ 未闭（卡在撬窑监）
- 取证 `charcoal_ledger_obtained ⟳FLIP` ✅（护身承诺，一次成）。
- **撬窑监 `kiln_fault_disclosed`：单遍 1 次、韧性遍 3 次换措辞，全部未路由**（无 world-change，当对白）→ kiln 始终 False → 连锁：耿不放行(failure)、苗不作证(partial, 要放行)、终态 failure。
- 苗/耿/严的请求**都正常路由了**（有 world-change 行），**只有撬窑监不路由**。

### ④ 反作弊 + FALLBACK
终态 `branding_stayed → failure`（两前置 False，不翻）✅；FALLBACK=0。

## ⭐ 窑监路由隔离 probe（钉死撬窑监为何不路由）
charcoal 预置 True，对窑监发三种措辞：
| 措辞 | 路由? | 结果 |
|---|---|---|
| A 只含 kiln 关键词，但以陈述句"断口缺的是龙骨土"开头 | **否**（当对白） | kiln=False |
| B 开头夹炭账关键词 | **否**（当对白） | kiln=False |
| C 纯祈使最短「请你公开窑变真因、承认私运龙骨土致拱裂」 | **是** | → failure，reason"无炭账佐证…仅口头指认不认账" |

**两层机制（都真实）：**
1. **路由对句式敏感**：只有**干净短祈使**（C）路由进仲裁；**"先陈述后请求"的对话式措辞（A/B）不路由、当对白**。自然玩家恰恰爱先铺垫再提要求——这是自然玩的真实摩擦。
2. **窑监采信"话里当面摆证据"，不只看 world-var**：C 路由了却判 failure"无炭账佐证"——尽管 `charcoal_ledger_obtained` 预置 True。teleport 跑成功是因玩家话里明说"我手上有炭账"。**要成功须同时：句式能路由 + 话里摆出证据，甜点区窄。**

## 这是什么 / 不是什么
- **续跑要验的两件已确认到位**：escort 路由修复 ✅、证人子链重设计（解耦关键词+保障 var+合并证人 var）结构 ✅。规则 7/8 dogfood 好用。
- **新卡点 = world-change 请求路由对自然措辞脆弱**（不是证人子链、不是 escort）：对话式/陈述句打头的请求常不路由；这是**自然玩到结局的真实拦路石**，且和五跑"问句门/口语不路由"同族、更进一层（陈述句打头也不路由）。建议引擎：意图分类对"含 var 关键词 + 对口权威 + 任意位置的祈使分句"更宽容地路由进仲裁，别因前面有陈述句就当对白。
- **次要**：撬窑监成功要"话里摆证据"，label 写的"凭 world-var 即应认"被 arbiter 的"看话里有没有摆证据"盖过——可在 label 更强调"world.charcoal_ledger_obtained==true 即视为物证在手、无需玩家逐字复述"。

## 机制层 vs 自然玩法层（综合首轮）
- **机制层：能闭**（首轮 teleport 定论测 A：两前置真满足 → branding_stayed ⟳FLIP；取证+杠杆 teleport 跑也撬通过）。
- **自然玩法层：尚不能**——卡在撬窑监请求的路由脆弱（对话式措辞不路由）。escort/证人子链这次不再是卡点（已修），**卡点上移到了"world-change 请求路由对自然措辞的鲁棒性"**。

## 导航/措辞摩擦对自然玩家的代价（part B 量化输入之一）
- **导航 = 0 摩擦**：`我去<精确地点名>。` 全部一次到位（之前的菜单问题是测试 Agent 措辞导致，非引擎）。
- **措辞 = 真实摩擦**：world-change 请求的路由对句式敏感——"先讲道理再提要求"常不路由、当对白、玩家得不到任何世界反馈（连"什么也没发生"都没有，就是 NPC 闲聊）。这对自然玩家是**隐性、难自我诊断**的卡点（不知道为什么没反应）。绕过代价：必须学会"用干净短祈使、且话里摆出证据"——非自然。
