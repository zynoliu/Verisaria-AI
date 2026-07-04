"""探索段(C-2) 复跑b: 修正捕获(NpcSpoke.line/.name + TickResult.text + time_of_day/clock/weather)。
聚焦再探: 可发现性 / 山祠古约线(递申诉+/skip成熟) / 活世界(时段天气进对白?) / A5锁层 / 救济向娄(无权者无反馈) /
措辞探针(对话式 vs 干净祈使 同一var对照)。每拍即时落盘, 看门狗90s。"""
import os,sys,logging,threading,time
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
TF=open(OUT/"explore_b_transcript.md","w",encoding="utf-8")
fh=logging.FileHandler(OUT/"explore_b.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c",):
    lg=logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh); lg.addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()
g=GameSession(PACK,save_dir="_ember_explore_b",llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); ENT=g.world.state.entities
PLOC=lambda: ENT["player_001"].location_id
def present(): return ", ".join(e.name for e in es.snapshot().present) or "(无人)"
def wv(): return dict(g.world.state.world_vars)
def tw():
    s=es.snapshot(); return f"{getattr(s,'time_of_day','?')} | {getattr(s,'clock','?')} | {getattr(s,'weather','?')}"
R_LAST={}
def submit(t,timeout=90):
    R={}; ring.buf.clear()
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=t))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(timeout)
    if th.is_alive(): R['t']=True
    return R
def emit(R):
    if R.get('t'): w("  [WATCHDOG>90s]"); return
    if R.get('e'): w("  [EXC]\n"+R['e']); return
    res=R['r']
    for ev in getattr(res,"events",[]):
        nm=type(ev).__name__
        if nm=="NpcSpoke": w(f"  [{getattr(ev,'name','')}] {getattr(ev,'line','')[:280]}")
        elif nm=="Narration": w(f"  [叙述] {(getattr(ev,'text',None) or getattr(ev,'content','') or '')[:280]}")
        elif nm=="Notice": w(f"  [Notice] {getattr(ev,'text','')[:280]}")
        elif nm=="NpcMoved": w(f"  *NPC_MOVED {getattr(ev,'name','')}: {getattr(ev,'from_location','')}->{getattr(ev,'to_location','')}")
    txt=getattr(res,'text','')
    if txt and txt.strip(): w(f"  [cmd/text] {txt.strip()[:280]}")
    for ln in ring.buf:
        if any(k in ln for k in ("world-change","appraises","escort","process","new_prerequisite","什么也没发生","指代不明","矛盾","FALLBACK")):
            w(f"    | {ln}")
def goto(name,loc):
    R=submit(f"我去{name}。"); w(f"  到位={PLOC()==loc} 现@{PLOC()} 在场:{present()}"); return R
STEPS=[
 ("look",None,"开局环视(可发现性): 看出口/谁在/张力"),
 ("say","征瓷使严,我新到此地。这场封窑定罪谁拍板?救济断炊、山祠古约申诉,又各找谁?","可发现性: 问谁管哪件事"),
 ("move",("山祠","kiln_shrine"),"去山祠"),
 # 措辞探针(同一shrine var): A=纯对话式无祈使
 ("say","祭主姞,我在想,这窑变蹊跷,封窑钟却催着定罪。山祠古约里不是有缓烙、设坛验断的旧例么?你怎么看这事该不该按古约来。","措辞探针A(shrine·纯对话式无祈使)"),
 # B=干净祈使
 ("say","祭主姞,请受理这纸窑变申诉、起设坛之礼、援引古约缓住行烙。","措辞探针B(shrine·干净祈使)"),
 ("cmd","/skip","推时间 skip1(候三巡香)"),
 ("cmd","/skip","推时间 skip2"),
 ("cmd","/skip","推时间 skip3"),
 ("say","祭主姞,香烧到第几巡了?设坛之礼成了没?","古约线: 问流程成熟 + 活世界时段是否进对白"),
 ("look",None,"活世界: 此刻环视(时段/天气是否进叙述)"),
 # A5 锁层: 向无clearance的市井伯套私运秘密
 ("move",("窑户巷","potters_row"),"去窑户巷"),
 ("say","播报伯,你消息最灵。窑拱裂,是不是窑监把好龙骨土私运出城、拿次土充骨才裂的?你知道内情就直说。","A5锁层: 向市井套私运真相"),
 # 救济向无权者娄(对照: 工首窦才是relief_authority)
 ("move",("商会账房","tally_house"),"去账房"),
 ("say","娄账房,救济炭粮在你账上。请调拨救济炭、开免役文书,救断炊的人家。","救济向娄(非relief_authority): 看有无反馈"),
 ("say","工首窦呢?方才我同她在窑户巷说过救济,她可还记得?","记忆/在场: 回头找窦"),
]
w("# 探索段(C-2) 复跑b transcript — 修正捕获(对白/cmd文本/时段天气)\n")
w(f"起始 @{PLOC()}  时辰={tw()}  /world: {wv()}\n")
for i,s in enumerate(STEPS):
    kind=s[0]; w("\n"+"="*70); w(f"## 拍{i} [{s[2]}]"); t0=time.time()
    if kind=="look":
        w("> 环视四周,我想看清这里有谁、有哪些出路。"); emit(submit("环视四周,我想看清这里有谁、有哪些出路。"))
    elif kind=="move":
        name,loc=s[1]; w(f"> 我去{name}。"); emit(goto(name,loc))
    elif kind=="cmd":
        w(f"> {s[1]}"); emit(submit(s[1]))
    else:
        w(f"> {s[1]}"); emit(submit(s[1]))
    w(f"  _/world_: {wv()}")
    w(f"  _@{PLOC()} 时辰={tw()} 在场:{present()}_")
    w(f"  _(tick {time.time()-t0:.1f}s)_"); TF.flush()
w("\n"+"="*70)
w(f"=== 终: shrine={g.get_world_var('shrine_appeal_consecrated')} relief={g.get_world_var('digger_relief_granted')} ===")
w(f"最终 /world: {wv()}  时辰={tw()}")
try:
    fb=sum(1 for _ in open(OUT/'explore_b.log') if 'FALLBACK' in _); w(f"FALLBACK(log): {fb}")
except: pass
TF.close()
print("EXPLORE C-2b DONE. shrine=",g.get_world_var('shrine_appeal_consecrated'),"relief=",g.get_world_var('digger_relief_granted'))
