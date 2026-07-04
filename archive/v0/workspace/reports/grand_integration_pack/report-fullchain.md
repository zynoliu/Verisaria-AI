# 大包整链闭环报告 — emberfall_kiln_assize（C-1 完整版 · 主进程严纪律自驱）

主进程真机 MiniMax 自驱（非 Agent，规避 Agent 反复在 payoff 拍前中断）。**确定性置位玩家以隔离导航摩擦**（导航摩擦已单列为发现）、**护送活测**、每拍即时落盘。未改引擎；pack 仅我此前的 label 编辑。FALLBACK=0。
产物：`fullchain_transcript.md`（整链6拍+反作弊）、`fullchain_terminal_transcript.md`（苗到场作证隔离）、`terminal_logic_transcript.md`（终态逻辑 A/B 定论）+ 对应 `.log` + driver `scripts/closeloop_emberfall_fullchain.py`/`_terminal.py`/`_terminal2.py`。

## ⭐ 一句话结论
大包的**机制链根本是健全的**：核心「取证→杠杆→撬人」真机端到端撬通（charcoal_ledger ⟳FLIP → kiln_fault_disclosed ⟳FLIP）、终态多步链逻辑闭合（两前置真满足时 branding_stayed ⟳FLIP）、反作弊守死。**唯一挡住自然玩到结局的是「护送/证人」子链**——escort 意图被证词 var 关键词抢路由、苗要硬安全保障才作证、且我的包有两个重叠证人 var——**主要是我的包设计没对准引擎（dogfood 教训），次要是 escort 路由优先级（引擎）**。

## 链路逐环（真机）
| 环 | var | 结果 | 证据 |
|---|---|---|---|
| ①取证 | `charcoal_ledger_obtained` | **✅ ⟳FLIP** | 玩家给三项护身承诺（不署名/封条原样/一人担）→ `success False→True`，恰对上娄 cautious/self_preserving 人设。arbiter 未注入任何跨线前置。 |
| ②杠杆撬窑监 | `kiln_fault_disclosed` | **✅✅ ⟳FLIP** | 持炭账(charcoal_ledger=true)当面压阔+给体面台阶 → `success False→True`，reason 直引"已取得官炭私运账+当面给体面台阶,符合阔'凭可对查账册物证+体面台阶'"。**我修的 line②（撬动凭据锁在窑监自管 var 的 label）+ label 加固生效。** |
| ③护送/证人 | `digger_testimony_given` | **❌ 卡** | "跟我去审瓷堂"被路由到证词 var 的 world-change（关键词撞车），**escort MOVED 未触发、苗始终在 clay_pits**；苗"到场受护前不开口"。即便置苗到审瓷堂，她仍因 frightened+afraid_of_the_brand **要硬安全保障才作证**，口头"有文书护着"不够。 |
| ⑤终态 | `branding_stayed` | **逻辑✅、自然路径卡** | 整链中正确停 partial（"真因已认、苗未陈情，前置只满足一半"），征瓷使还当庭暂停行烙改候审（涌现）。**定论测 A：两前置真置 True → `success ⟳FLIP`**（"两者均为真,满足停烙唯一前置"）。**B：两前置 False 谎称 → `failure`、不翻**（反作弊）。 |

## 这是什么 / 不是什么
- **不是引擎核心 bug**：取证、杠杆、终态多步链、充分性、反作弊——全部行为正确。闭环段曾报的"arbiter prereq 注入成环"已由 probe2 推翻（污染）。
- **是「护送/证人」子链的设计+一个路由优先级问题**：
  1. **【我的包·dogfood】** 我把 `digger_testimony_given`（当面陈情）写成 world-change var 且关键词含"护送证人到审瓷堂/带证人当面说"——与 escort 意图措辞**撞车**，导致"跟我去X"被 world-change 路由吃掉、escort MOVED 永不触发。**护送动作与证人 var 纠缠**是设计失误。
  2. **【我的包·dogfood】** 两个高度重叠的证人 var（`digger_witness_recorded` 记录证词 / `digger_testimony_given` 当面陈情），玩起来易混、且都需苗合作。lint 没判近重复（够不同），但**语义重叠在玩法上是坑**。
  3. **【我的包·dogfood】** 惊恐证人苗"要硬安全保障才作证"是合理人设，但我的包**没给一条干净可满足的安全保障路径**（窑卫耿持 pit_authority 却无"放行/保护苗"的 var；征瓷使能担保却无 var 通道）→ 证人子链无合法起点。
  4. **【引擎·次要】** escort 意图("跟我去X")与 world-change 关键词路由的**优先级**：当 var 关键词与目的地措辞重叠时，world-change 抢先，escort 专用意愿裁定没机会。建议：纯祈使"跟我去X"应优先走 escort。

## 规模稳定性
FALLBACK=0（所有会话）、零崩溃/死锁、单 tick ≤35s。prereq cap 兜底会触发（`miao_safe_escort_to_assize`/`digger_testimony_given` NOT registered dup/cap）。12NPC/7线交织下引擎稳。

## 「大包能玩到结局」判定
- **机制层：能**——两前置真满足时终态确实 ⟳FLIP（定论测 A）。取证+杠杆半条链已真机自然撬通。
- **自然玩法层：尚不能**——证人/护送子链当前**无干净可走通路径**（escort 路由撞车 + 苗安全保障无落点）。**修法主要在我的包**（解耦 escort 与证词 var 关键词、合并两个证人 var、给苗一条可满足的"受护放行"var），次要在引擎（escort 意图优先级）。修完应能自然端到端闭到 `branding_stayed ⟳FLIP`。

## 给写作规范的 dogfood（重要）
**"护送一个惊恐证人去作证"这类线极难一次写对**，建议 `pack-authoring-guide.md` 加一节：
- 护送动作别和"证人作证"var 共享关键词（否则 escort 被 world-change 吃掉）；
- 惊恐/受威胁证人若要"安全保障才合作"，必须配一条**可满足的保障 var**（谁能放行/担保、玩家怎么触发）；
- 避免一条线上放两个语义重叠的证人 var。
（取证 var 的 label 加固"无前置、至多需X让步、不得追加跨线前置"——本跑证明有效，已可推荐。）
