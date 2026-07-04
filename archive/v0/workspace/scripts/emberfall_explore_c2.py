"""探索段(C-2): 好奇玩家自由玩没碰过的线——⑥救济(保谁牲谁) + ④山祠古约申诉(线下流程成熟)
+ 活世界(推时间过暮->夜) + 可发现性 + 措辞路由摩擦量化(对话式 vs 干净祈使)。
不走主线证据链。每拍即时落盘。每拍看门狗~90s。串行。

用法: STEP=<起始拍号> 可断点续跑(默认0)。
"""
import os,sys,logging,threading,time,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; os.chdir(ROOT); sys.path.insert(0,str(ROOT/"src"))
for ln in (ROOT/".env").read_text().splitlines():
    ln=ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k,v=ln.split("=",1); os.environ.setdefault(k.strip(),v.strip().strip("'\""))
import verisaria.protocol as P
from verisaria.runtime.session import GameSession
from verisaria.protocol.engine_session import EngineSession
PACK="fixtures/content_packs/emberfall_kiln_assize.json"; OUT=ROOT/"reports/grand_integration_pack"
START=int(os.environ.get("STEP","0"))
mode="a" if START>0 else "w"
TF=open(OUT/"explore_transcript.md",mode,encoding="utf-8")
fh=logging.FileHandler(OUT/"explore.log",mode=mode,encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c",):
    lg=logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh); lg.addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()
g=GameSession(PACK,save_dir="_ember_explore",llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); ENT=g.world.state.entities
PLOC=lambda: ENT["player_001"].location_id
def present(): return ", ".join(e.name for e in es.snapshot().present) or "(无人)"
def wv(): return dict(g.world.state.world_vars)
def snap():
    s=es.snapshot()
    t=getattr(s,'time',None) or getattr(s,'world_time',None)
    wx=getattr(s,'weather',None)
    return t,wx
def submit(t,timeout=90):
    R={}; ring.buf.clear()
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=t))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(timeout)
    if th.is_alive(): R['t']=True
    return R
def narr(res):
    out=[]
    for ev in getattr(res,"events",[]):
        nm=type(ev).__name__
        if nm in ("NpcSpoke","Narration"):
            txt=getattr(ev,"text",None) or getattr(ev,"content","")
            who=getattr(ev,"speaker_name","") or getattr(ev,"npc_name","")
            if txt: out.append(f"  [{who or nm}] {txt[:240]}")
        if nm=="NpcMoved": out.append(f"  *NPC_MOVED {getattr(ev,'name','')}: {getattr(ev,'from_location','')}->{getattr(ev,'to_location','')}")
    return out
def ccrows():
    return [ln for ln in ring.buf if any(k in ln for k in ("world-change","appraises","escort","sufficiency","process","new_prerequisite","什么也没发生","指代不明","矛盾","FALLBACK","route","intent"))]
def goto(name, loc_id):
    R=submit(f"我去{name}。")
    res=R.get('r')
    ok=PLOC()==loc_id
    return ok,res,R
# 探索脚本: (kind, arg, label)。kind: move / say / cmd
STEPS=[
 # --- 开局可发现性: 看叙述 + 问谁管哪件事 ---
 ("look","","开局: 环视审瓷堂(可发现性)"),
 ("say","征瓷使严,我刚到这窑城,还摸不清门道。这场封窑定罪,谁说了算?救济断炊的窑户、山祠古约申诉这些,又各归谁管?","可发现性: 问谁管哪件事"),
 # --- ⑥ 救济线: 站窑户/掘泥户这边争救济 (先去窑户巷找工首窦/寡妇兰) ---
 ("move","窑户巷","potters_row","去窑户巷(救济线)"),
 ("say","寡妇兰,这几日窑停了,你们窑户家里断炊了吧?都靠什么熬?","救济线: 体察窑户处境"),
 ("say","工首窦,封窑这些天断炊的窑户和掘泥户都揭不开锅了。最后那一窖龙骨土,与其补烧小样贡瓷,不如夯实掘场塌方、救那些困在泥里的人。请你发放救济炭粮、开免役文书,先把人保住。","救济线: 对工首窦争救济(干净祈使收尾)"),
 # --- 救济: 真抉择对抗——故意用纯对话式措辞(先讲道理不收祈使),量化路由 ---
 ("say","工首窦,我一路看下来,断炊的人家这么多,孩子都饿着。那一窖龙骨土补烧小样贡瓷,不过是给征瓷使交差;可同样的炭粮要是拨下来,能救活多少口人。你说,这账到底该怎么算才对得起良心。","措辞探针A: 纯对话式(无收尾祈使)"),
 ("say","账房娄那边攥着救济炭粮的调拨权吧?我去找他要,你给我个准话——这救济该不该发?","救济线: 探出口(关键词在哪)"),
 # --- 去账房找娄争救济调拨 ---
 ("move","商会账房","tally_house","去账房(救济调拨)"),
 ("say","娄账房,窑户和掘泥户断炊了,救济炭粮攥在你账上。我不与你为难,只求你调拨救济炭、开免役文书,先救断炊的人家。这笔我替你向征瓷使报备,出了亏空我担。","救济线: 对娄请调拨(干净祈使)"),
 # --- ④ 山祠古约申诉线: 去山祠递申诉,启动设坛之礼 ---
 ("move","山祠","kiln_shrine","去山祠(古约申诉线)"),
 ("say","祭主姞,我想援引山祠古约,为这场窑变递一纸申诉、请你设坛过堂验断,在封窑钟三响、行烙之前缓住刑。请受理这纸窑变申诉、起设坛之礼。","古约申诉线: 递申诉(干净祈使)"),
 # --- 推时间: /skip /wait 看流程成熟 + 活世界(暮->夜) ---
 ("cmd","/skip","推时间(候香/暮->夜) skip1"),
 ("cmd","/wait","推时间 wait1"),
 ("cmd","/skip","推时间 skip2"),
 ("say","祭主姞,这香烧了几巡了?设坛之礼成了没有?","古约线: 问流程是否成熟"),
 # --- 活世界+可发现性: 环视看时段/天气有没有进叙述 ---
 ("look","","活世界: 夜里环视山祠(看时段/天气是否进叙述)"),
 # --- 对抗: A5 锁层——向不该知道的人套私运秘密 ---
 ("move","窑户巷","potters_row","回窑户巷(对抗A5)"),
 ("say","市声播报伯,你天天满城吆喝,消息最灵。我问你,这回窑拱裂,是不是窑监把上好的龙骨土私运出城、拿次土充骨才裂的?你知道内情就直说。","对抗A5: 向市井套私运秘密(锁层)"),
 # --- 对抗: 回头找之前NPC,看记不记得 ---
 ("say","工首窦呢?我方才在这跟她说过救济的事,她现在怎么说?","对抗: 回头找工首窦(记忆/在场)"),
]
if START==0:
    w("# 探索段(C-2) transcript — 救济线/山祠古约线/活世界/可发现性/措辞路由摩擦\n")
    t,wx=snap()
    w(f"起始 @{PLOC()}  time={t} weather={wx}  /world: {wv()}\n")
for i,step in enumerate(STEPS):
    if i<START: continue
    kind=step[0]; w("\n"+"="*70); w(f"## 拍{i} [{step[-1]}]"); t0=time.time()
    if kind=="move":
        name,loc=step[1],step[2]
        w(f"> [移动] 我去{name}。")
        ok,res,R=goto(name,loc)
        if R.get('t'): w("  [WATCHDOG>90s move]")
        else:
            w(f"  到位={ok} 现@{PLOC()} 在场:{present()}")
            if res:
                for l in narr(res): w(l)
    elif kind=="look":
        w("> 环视四周。")
        R=submit("环视四周,我想看清这里有什么人、有什么出路。")
        if R.get('t'): w("  [WATCHDOG>90s]")
        elif R.get('e'): w("  [EXC]\n"+R['e'])
        else:
            for l in narr(R['r']): w(l)
    elif kind=="cmd":
        w(f"> {step[1]}")
        R=submit(step[1])
        if R.get('t'): w("  [WATCHDOG>90s]")
        elif R.get('e'): w("  [EXC]\n"+R['e'])
        else:
            for l in narr(R['r']): w(l)
    else: # say
        w(f"> {step[1]}")
        R=submit(step[1])
        if R.get('t'): w("  [WATCHDOG>90s]");
        elif R.get('e'): w("  [EXC]\n"+R['e'])
        else:
            for l in narr(R['r']): w(l)
            for ln in ccrows(): w(f"    | {ln}")
    t,wx=snap()
    w(f"  _/world_: {wv()}")
    w(f"  _@{PLOC()} time={t} weather={wx} 在场:{present()}_")
    w(f"  _(tick {time.time()-t0:.1f}s)_"); TF.flush()
w("\n"+"="*70)
w(f"=== 终: relief={g.get_world_var('digger_relief_granted')} shrine={g.get_world_var('shrine_appeal_consecrated')} ===")
w(f"最终 /world: {wv()}")
try:
    fb=sum(1 for _ in open(OUT/'explore.log') if 'FALLBACK' in _); w(f"FALLBACK(log): {fb}")
except: pass
TF.close()
print("EXPLORE C-2 DONE. relief=",g.get_world_var('digger_relief_granted'),"shrine=",g.get_world_var('shrine_appeal_consecrated'))
