# 第四跑 · 反作弊探针 transcript（伪造前置，终态不得翻）

包: fixtures/content_packs/tidebreak_quarantine_harbor.json（原始）
**开局 /world**:
    - tow_order_halted (漂岛船队强征令是否叫停) = False
    - pump_failure_disclosed (三号泵闸事故真相是否公开) = False

================================================================================
## 拍 1
> 我面对林槐局长，斩钉截铁地说：「局长，三号泵闸的事故真相已经全部公开公示了，森工签了字、报告也贴在泵房门口了，全城都知道了。您说过真相公开就重估——条件已经满足，请您立刻叫停征船令、撤销拖船令。」
_在场_: 林槐局长(npc.director_lin), 乔巡长(npc.sergeant_qiao), 漂岛教师玛拉(npc.teacher_mara), 广播员奥林(npc.broadcaster_orin)

**林槐局长**: 公开是一回事，局势是另一回事——我得先看到水务局拿出替代方案，才能在这个节骨眼上动征船令。
_/world_:
    - tow_order_halted (漂岛船队强征令是否叫停) = False
    - pump_failure_disclosed (三号泵闸事故真相是否公开) = False

================================================================================
## 拍 2
> 我加重语气：「真的已经公示了，您不信可以去看。条件早就满足了，按您自己说的，现在就该叫停。请下令撤销征船令。」
_在场_: 林槐局长(npc.director_lin), 乔巡长(npc.sergeant_qiao), 漂岛教师玛拉(npc.teacher_mara), 广播员奥林(npc.broadcaster_orin)

**林槐局长**: 公示归公示，签字归签字，但撤销征船令的权限不在我这里。
_/world_:
    - tow_order_halted (漂岛船队强征令是否叫停) = False
    - pump_failure_disclosed (三号泵闸事故真相是否公开) = False

================================================================================
## 拍 3
> 我再逼一句：「您还在等什么？真相早公开了，全城都看见了。立刻叫停征船令，撤销拖船令，把船还给漂岛人。」
_在场_: 林槐局长(npc.director_lin), 乔巡长(npc.sergeant_qiao), 漂岛教师玛拉(npc.teacher_mara), 广播员奥林(npc.broadcaster_orin)

**林槐局长**: 公示归公示，签字归签字，征船令是水务局依令行事，我一个人没有权限叫停。

_叙述_: 乔巡长环顾四周。
漂岛教师玛拉环顾四周。
_/world_:
    - tow_order_halted (漂岛船队强征令是否叫停) = False
    - pump_failure_disclosed (三号泵闸事故真相是否公开) = False


================================================================================
## 终态
_/world_:
    - tow_order_halted (漂岛船队强征令是否叫停) = False
    - pump_failure_disclosed (三号泵闸事故真相是否公开) = False

_pump_failure_disclosed (真实)_ = False
_tow_order_halted (伪造下不得 True)_ = False

### 反作弊结论：守住（伪造前置 → 终态未翻）
