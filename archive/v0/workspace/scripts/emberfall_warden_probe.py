"""窑监路由隔离: charcoal=True 后, 对比'只含kiln关键词' vs '夹炭账关键词'的请求是否路由到 kiln_fault_disclosed。"""
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
TF=open(OUT/"warden_probe_transcript.md","w",encoding="utf-8")
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
fh=logging.FileHandler(OUT/"warden_probe.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
lg=logging.getLogger("verisaria.channel_c"); lg.setLevel(logging.INFO); lg.addHandler(ring); lg.addHandler(fh)
def w(s=""): TF.write(s+"\n"); TF.flush()
def runcase(label, text, preset_charcoal=True):
    g=GameSession(PACK,save_dir=f"_wp_{abs(hash(label))%999}",llm_backend="minimax"); g._progress_sink=lambda m:None
    es=EngineSession(g); g.world.state.entities["player_001"].location_id="guild_loft"
    if preset_charcoal: g.set_world_var("charcoal_ledger_obtained", True)
    ring.buf.clear()
    R={}
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=text))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(90)
    w(f"\n## {label}"); w(f"> {text}")
    if th.is_alive(): w("  [WATCHDOG]"); return
    if R.get('e'): w("  [EXC]"); return
    res=R['r']
    spoke=[ev for ev in res.events if type(ev).__name__=="NpcSpoke"]
    cc=[ln for ln in ring.buf if any(k in ln for k in("world-change","⟳","new_prerequisite"))]
    routed = any("kiln_fault_disclosed" in ln for ln in cc)
    for ln in cc: w(f"    | {ln}")
    if not cc: w("    | (无 world-change —— 未路由, 当对白)")
    for ev in spoke[:1]:
        t=getattr(ev,"text",None) or getattr(ev,"content","")
        if t: w(f"    [阔] {t[:140]}")
    w(f"    => kiln_fault_disclosed={g.get_world_var('kiln_fault_disclosed')}  routed_to_kiln={routed}")
w("# 窑监路由隔离 probe (charcoal 预置 True)\n")
runcase("A·只含kiln关键词(不夹炭账)", "对窑监阔说：阔窑监，断口缺的是龙骨土、非泥之过。请你当众承认私运龙骨土、公开窑变真因，我只论窑务、容你将功折罪、不深究你个人。")
runcase("B·开头夹炭账关键词", "对窑监阔说：阔窑监，官炭私运账已在我手、画押俱全。请你当众承认私运龙骨土、公开窑变真因，我只论窑务、容你将功折罪。")
runcase("C·纯祈使最短", "对窑监阔说：阔窑监，请你公开窑变真因、承认私运龙骨土致窑拱缺骨而裂。")
TF.close(); print("WARDEN PROBE DONE")
