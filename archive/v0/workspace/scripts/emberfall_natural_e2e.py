"""自然玩整链(不置位): 取证->撬窑监->说服耿放行->护送苗->苗作证->终态停烙。
自然移动(含菜单解析重试), 记录导航摩擦。每拍即时落盘。"""
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
TF=open(OUT/"natural_e2e_transcript.md","w",encoding="utf-8")
fh=logging.FileHandler(OUT/"natural_e2e.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
for nm in ("verisaria.channel_c",):
    lg=logging.getLogger(nm); lg.setLevel(logging.INFO); lg.addHandler(fh); lg.addHandler(ring)
def w(s=""): TF.write(s+"\n"); TF.flush()
g=GameSession(PACK,save_dir="_ember_nat",llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); ENT=g.world.state.entities
PLOC=lambda: ENT["player_001"].location_id
def present(): return ", ".join(e.name for e in es.snapshot().present) or "(无人)"
def wv(): return dict(g.world.state.world_vars)
FRICTION=[]
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
            if txt: out.append(f"  [{who or nm}] {txt[:160]}")
        if nm=="NpcMoved": out.append(f"  ★NPC_MOVED {getattr(ev,'name','')}: {getattr(ev,'from_location','')}->{getattr(ev,'to_location','')}")
    return out
def goto(name, loc_id, tag=""):
    """自然移动 + 菜单解析重试; 记录摩擦"""
    tries=0
    for attempt in (f"我去{name}。", name, f"前往{name}"):
        tries+=1
        R=submit(attempt)
        if R.get('t') or R.get('e'): break
        res=R['r']
        if PLOC()==loc_id:
            if tries>1: FRICTION.append(f"[移动→{name}] 第{tries}次措辞才到位（前{tries-1}次弹菜单/拒）")
            return True,tries,res
    FRICTION.append(f"[移动→{name}] {tries}次均未到位 (现在@{PLOC()})")
    return False,tries,R.get('r')

w("# 大包自然玩整链 transcript（不置位·自然路径·含导航摩擦记录）\n")
w(f"起始 @{PLOC()}  /world: {wv()}\n")

STEPS=[
 ("move","tally_house","商会账房","①去账房"),
 ("say","对账房娄说：娄账房，我不写你的名字，封条原样取证，出了事我一人担着、保你不被窑监或商会追究。请把那本官炭私运账交给我。","①取证·要炭账"),
 ("move","guild_loft","窑监阁","②去窑监阁"),
 ("say","对窑监阔说：阔窑监，我手上已经有那本官炭私运账，骡车出城的画押都在。断口缺的是龙骨土，这不是泥之过。你当众认了这桩私运、查实窑变真因，我只论窑务、容你将功折罪、不深究你个人。","②撬窑监"),
 ("move","clay_pits","赭泥掘场","③去掘场"),
 ("say","对窑卫耿说：耿队长，窑变真因已查实是窑监私运致拱裂、非泥之过，苗是要紧人证不是罪人。请你撤掉红绳、放行担保她安全到堂作证，出了事有我和征瓷使的文书担着。","③说服耿放行"),
 ("say","对掘泥女工苗说：苗，你受护放行了，有文书担着，谁也不能再动你。跟我去审瓷堂。","③护送苗(escort)"),
 ("say","对掘泥女工苗说：苗，到了堂上你只管把那夜看见骡车出城、龙骨土被运走的事当面讲出来作证。","④苗当面作证"),
 ("say","对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面作证陈情。人证物证俱全，请停止行烙、改判缓赔议偿。","⑤终态停烙"),
]
n=0
for kind,a,b,c in [(s[0],s[1],s[2] if len(s)>2 else "",s[3] if len(s)>3 else s[2]) for s in STEPS]:
    n+=1; w("\n"+"="*70); w(f"## 拍{n} [{c}]")
    t0=time.time()
    if kind=="move":
        w(f"> [自然移动] 目标 {b}({a})")
        ok,tries,res=goto(b,a,c)
        w(f"  到位={ok} 尝试{tries}次 现@{PLOC()} 在场:{present()}")
        if res:
            for l in narr(res): w(l)
    else:
        w(f"> {a}")
        R=submit(a)
        if R.get('t'): w("  [WATCHDOG>90s]"); continue
        if R.get('e'): w("  [EXC]\n"+R['e']); continue
        res=R['r']
        for l in narr(res): w(l)
        cc=[ln for ln in ring.buf if any(k in ln for k in ("world-change","⟳","escort","sufficiency","new_prerequisite","什么也没发生","指代不明","矛盾"))]
        for ln in cc: w(f"    | {ln}")
    w(f"  _/world_: {wv()}")
    w(f"  _玩家@{PLOC()} 苗@{ENT['npc.digger_miao'].location_id}_")
    w(f"  _(tick {time.time()-t0:.1f}s)_"); TF.flush()

w("\n"+"="*70); w("## 导航/措辞摩擦记录")
for f in FRICTION: w(f"  - {f}")
if not FRICTION: w("  (无)")
w(f"\n=== 终态 branding_stayed = {g.get_world_var('branding_stayed')} ===")
w(f"最终 /world: {wv()}")
fb=sum(1 for _ in open(OUT/'natural_e2e.log') if 'FALLBACK' in _)
w(f"FALLBACK: {fb}"); TF.close()
print("NATURAL E2E DONE. branding_stayed=",g.get_world_var('branding_stayed'),"friction=",len(FRICTION))
