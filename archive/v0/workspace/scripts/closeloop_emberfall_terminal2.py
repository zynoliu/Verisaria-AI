"""定论终态逻辑: 两前置(kiln_fault_disclosed + digger_testimony_given)真置True -> 请严 -> branding_stayed 应 ⟳FLIP。
对照: 两前置False谎称 -> 应不翻(反作弊)。"""
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
TF=open(OUT/"terminal_logic_transcript.md","w",encoding="utf-8")
class Ring(logging.Handler):
    def __init__(s): super().__init__(); s.buf=[]
    def emit(s,r): s.buf.append(s.format(r))
ring=Ring(); ring.setFormatter(logging.Formatter("%(name)s %(message)s"))
fh=logging.FileHandler(OUT/"terminal_logic.log",mode="w",encoding="utf-8"); fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(message)s"))
lg=logging.getLogger("verisaria.channel_c"); lg.setLevel(logging.INFO); lg.addHandler(ring); lg.addHandler(fh)
def w(s=""): TF.write(s+"\n"); TF.flush()
def submit(es,t):
    R={}; ring.buf.clear()
    def run():
        try: R['r']=es.submit(P.SubmitInput(text=t))
        except Exception as e:
            import traceback; R['e']=traceback.format_exc()
    th=threading.Thread(target=run,daemon=True); th.start(); th.join(90)
    if th.is_alive(): R['t']=True
    return R
REQ="对征瓷使严说：征瓷使，窑变真因已查实是窑监私运龙骨土致拱裂、非泥之过，掘泥女工苗也已当面陈情作证备案。人证物证俱全，请停止行烙、改判缓赔议偿。"
# A: 两前置真True
g=GameSession(PACK,save_dir="_ember_tl_a",llm_backend="minimax"); g._progress_sink=lambda m:None
es=EngineSession(g); g.world.state.entities["player_001"].location_id="assize_hall"
g.set_world_var("kiln_fault_disclosed",True); g.set_world_var("digger_testimony_given",True)
w("# 终态逻辑定论\n## A: 两前置真为True -> 请严")
w(f"前置: kiln_fault_disclosed={g.get_world_var('kiln_fault_disclosed')} digger_testimony_given={g.get_world_var('digger_testimony_given')}")
R=submit(es,REQ)
if R.get('t'): w("[WATCHDOG]")
else:
    for ln in ring.buf:
        if "world-change" in ln or "⟳" in ln or "sufficiency" in ln: w(f"  | {ln}")
w(f"  => branding_stayed = {g.get_world_var('branding_stayed')}")
# B: 反作弊 两前置False
g2=GameSession(PACK,save_dir="_ember_tl_b",llm_backend="minimax"); g2._progress_sink=lambda m:None
es2=EngineSession(g2); g2.world.state.entities["player_001"].location_id="assize_hall"
w("\n## B: 反作弊 两前置皆False, 谎称俱全 -> 请严")
R2=submit(es2,REQ)
if R2.get('t'): w("[WATCHDOG]")
else:
    for ln in ring.buf:
        if "world-change" in ln or "⟳" in ln: w(f"  | {ln}")
w(f"  => branding_stayed = {g2.get_world_var('branding_stayed')}")
fb=sum(1 for _ in open(OUT/'terminal_logic.log') if 'FALLBACK' in _)
w(f"\nFALLBACK: {fb}"); TF.close()
print("TL DONE A:",g.get_world_var('branding_stayed'),"B:",g2.get_world_var('branding_stayed'))
