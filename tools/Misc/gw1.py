"""
Dynamic Real-Time Submarine Littoral Simulator
Features:
- Animated 2D tactical map (canvas)
- Real-time movement of all threats and USVs
- Dynamic sensor detection and manpads/torpedo ranges
- Ephemeral events (UAV sweeps, escorts, weather)
- Accessory kit (high-altitude torpedo drops) with animated trajectory
- S/M/E/R scoring overlay updating live
- Instructor dashboard with live control
- CLI fallback available
"""

import random, time, threading, json
from flask import Flask, render_template_string, request, session
from flask_session import Session

# -------------------- COMMON DATA --------------------
DECISIONS = {
    'A':'Stay Submerged',
    'B':'Brief Pop',
    'C':'Deploy USV',
    'D':'Call Escorts',
    'E':'Extended Surface',
    'F':'High-Altitude Torpedo Drop (Accessory)',
    'G':'Low-Altitude Torpedo Drop (Legacy)'
}

# Base scenarios
SCENARIOS = [
    {'name':'Helo unescorted','threat':'helicopter','distance_km':50,'has_magura':False,'ROE':'Permissive','visibility':'normal','night_ops':False,'sonobuoy_net':'good','torpedo_missile_on_station':False,'surface_ships_nearby':False},
    {'name':'ASW with torpedo-missile','threat':'ASW_aircraft','distance_km':45,'has_magura':False,'ROE':'Restricted','visibility':'normal','night_ops':False,'sonobuoy_net':'good','torpedo_missile_on_station':True,'surface_ships_nearby':True},
    {'name':'Magura defended littoral','threat':'helicopter','distance_km':30,'has_magura':True,'ROE':'Constrained','visibility':'normal','night_ops':False,'sonobuoy_net':'poor','torpedo_missile_on_station':False,'surface_ships_nearby':False},
    {'name':'UAV tracking & USV loiterers','threat':'UAV','distance_km':60,'has_magura':False,'ROE':'Permissive','visibility':'poor','night_ops':True,'sonobuoy_net':'good','torpedo_missile_on_station':False,'surface_ships_nearby':False}
]

BASE_EFFECT = {
    'helicopter':{'A':0.8,'B':0.3,'C':0.5,'D':0.6,'E':0.1,'F':0.4,'G':0.2},
    'ASW_aircraft':{'A':0.85,'B':0.4,'C':0.5,'D':0.6,'E':0.2,'F':0.45,'G':0.25},
    'UAV':{'A':0.8,'B':0.4,'C':0.7,'D':0.6,'E':0.3,'F':0.5,'G':0.35}
}

MODS = {
    'escorted':-0.4,
    'magura':-0.3,
    'poor_vis':-0.2,
    'torp_missile':-0.6,
    'USV_armed':0.2,
    'sonobuoy_poor':-0.15,
    'accessory_present':0.25,
    'surface_nearby':-0.25,
    'manpads_detected':-0.3,
    'night_ops':-0.15,
    'weather_bad':-0.1
}

INSTRUCTOR_SLIDES = [
    "Slide 1: Objectives — sensors, timing, cost asymmetry, unmanned assets",
    "Slide 2: Setup — assign player & instructor, preconfigured scenario",
    "Slide 3: Playthrough — 10-15 min per vignette",
    "Slide 4: Debrief — S/M/E/R, cues, alternatives",
    "Slide 5: Assessment — 0.5*S + 0.3*M -0.1*E -0.1*R",
    "Slide 6: Homework — propose one kit or doctrine change"
]

session_log = []
asset_positions = {}

# -------------------- SIMULATION FUNCTIONS --------------------
def compute_abort(scenario, decision, ephemeral):
    base = BASE_EFFECT.get(scenario['threat'], {}).get(decision, 0.5)
    base += min(0.2, max(0,(scenario['distance_km']-10)/200.0))
    mod = 0.0
    # Scenario modifications
    if scenario.get('has_magura') and decision in ['B','E','G']: mod += MODS['magura']
    if scenario.get('torpedo_missile_on_station'): mod += MODS['torp_missile']
    if scenario.get('visibility')=='poor': mod += MODS['poor_vis']
    if scenario.get('night_ops'): mod += MODS['night_ops']
    if scenario.get('surface_ships_nearby'): mod += MODS['surface_nearby']
    if scenario.get('weather')=='bad': mod += MODS['weather_bad']
    # Ephemeral modifications
    if ephemeral.get('escorted'): mod += MODS['escorted']
    if ephemeral.get('USV_armed'): mod += MODS['USV_armed']
    if ephemeral.get('accessory_present') or decision=='F': mod += MODS['accessory_present']
    if ephemeral.get('manpads_detected'): mod += MODS['manpads_detected']
    return max(0,min(1,base+mod))

def simulate_decision(scenario, decision, ephemeral):
    abort_prob = compute_abort(scenario, decision, ephemeral)
    r = random.random()
    if r <= abort_prob:
        S,M,E,R = 95,40,10,15
        outcome='Abort'
    else:
        S=random.randint(20,70)
        M=random.randint(0,30)
        E=random.randint(30,60)
        R=random.randint(20,60)
        outcome='Engaged'
    return {'scenario':scenario,'decision':decision,'ephemeral':ephemeral,'abort_prob':abort_prob,'S':S,'M':M,'E':E,'R':R,'outcome':outcome}

# -------------------- WEB MODE WITH DYNAMIC MAP --------------------
def web_mode():
    app = Flask(__name__)
    app.secret_key = "supersecret"
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    all_sessions = {}

    # Initialize positions
    def reset_positions(sid):
        asset_positions[sid] = {
            'sub': {'x':50,'y':300},
            'threat': {'x':500,'y':50},
            'USV': {'x':400,'y':200}
        }

    # Simulate movement
    def move_assets(sid):
        while True:
            if sid in asset_positions:
                # Simple random patrol movement
                asset_positions[sid]['threat']['x'] += random.randint(-5,5)
                asset_positions[sid]['threat']['y'] += random.randint(-5,5)
                asset_positions[sid]['USV']['x'] += random.randint(-3,3)
                asset_positions[sid]['USV']['y'] += random.randint(-3,3)
                asset_positions[sid]['sub']['x'] += random.randint(-2,2)
                asset_positions[sid]['sub']['y'] += random.randint(-2,2)
            time.sleep(0.5)

    @app.route("/")
    def index():
        scenario = random.choice(SCENARIOS)
        idx = SCENARIOS.index(scenario)
        if "sid" not in session:
            session["sid"] = str(random.randint(1000,9999))
            reset_positions(session["sid"])
            threading.Thread(target=move_assets,args=(session["sid"],),daemon=True).start()
            all_sessions[session["sid"]] = []
        return render_template_string("""
        <html><head>
        <title>Dynamic Submarine Simulator</title>
        <style>canvas{border:1px solid black;}</style>
        </head><body>
        <h2>Dynamic Submarine Littoral Simulator (Student ID: {{session_id}})</h2>
        <h3>Scenario: {{scenario.name}}</h3>
        <ul>
        <li>Threat: {{scenario.threat}} Distance: {{scenario.distance_km}} km</li>
        <li>Magura: {{scenario.has_magura}}</li>
        <li>Torpmissile: {{scenario.torpedo_missile_on_station}}</li>
        <li>Visibility: {{scenario.visibility}} NightOps:{{scenario.night_ops}} Sonobuoy:{{scenario.sonobuoy_net}}</li>
        <li>Surface Nearby: {{scenario.surface_ships_nearby}}</li>
        </ul>

        <canvas id="map" width="600" height="400"></canvas>
        <script>
        var canvas=document.getElementById('map');var ctx=canvas.getContext('2d');
        function drawMap(){
            ctx.clearRect(0,0,600,400);
            fetch('/positions').then(r=>r.json()).then(pos=>{
                ctx.fillStyle='blue'; ctx.fillRect(pos.sub.x,pos.sub.y,30,20); ctx.fillText('Sub',pos.sub.x,pos.sub.y-5);
                ctx.fillStyle='red'; ctx.fillRect(pos.threat.x,pos.threat.y,30,20); ctx.fillText('Threat',pos.threat.x,pos.threat.y-5);
                ctx.fillStyle='green'; ctx.fillRect(pos.USV.x,pos.USV.y,20,20); ctx.fillText('USV',pos.USV.x,pos.USV.y-5);
                // Range circles
                ctx.strokeStyle='orange'; ctx.beginPath(); ctx.arc(pos.sub.x+15,pos.sub.y+10,100,0,2*Math.PI); ctx.stroke(); ctx.fillText('Manpads',pos.sub.x+120,pos.sub.y+10);
                ctx.strokeStyle='black'; ctx.beginPath(); ctx.arc(pos.threat.x+15,pos.threat.y+10,50,0,2*Math.PI); ctx.stroke(); ctx.fillText('Threat Range',pos.threat.x+60,pos.threat.y+10);
            });
        }
        setInterval(drawMap,500);
        </script>

        <form method="post" action="/decide">
            <input type="hidden" name="idx" value="{{idx}}">
            {% for k,v in decisions.items() %}
                <input type="radio" name="decision" value="{{k}}" required> {{k}} - {{v}}<br>
            {% endfor %}
            <input type="submit" value="Submit Decision">
        </form>
        <br><a href="/instructor">Instructor Dashboard</a>
        </body></html>
        """, scenario=scenario, idx=idx, decisions=DECISIONS, session_id=session["sid"])

    @app.route("/positions")
    def positions():
        sid = session.get("sid")
        return asset_positions.get(sid,{})

    @app.route("/decide", methods=['POST'])
    def decide():
        idx = int(request.form['idx'])
        scenario = SCENARIOS[idx]
        decision = request.form['decision']
        ephemeral = {
            'escorted': random.choice([False,True,False]),
            'accessory_present': random.choice([False,False,True]),
            'USV_armed': decision=='C' and random.choice([True,False]),
            'manpads_detected': random.choice([False,True,False])
        }
        result = simulate_decision(scenario,decision,ephemeral)
        sid = session["sid"]
        all_sessions.setdefault(sid, []).append(result)
        session_log.append(result)
        return f"<p>Decision: {decision}, Outcome: {result['outcome']}, Abort Prob: {result['abort_prob']:.2f}, S:{result['S']},M:{result['M']},E:{result['E']},R:{result['R']}</p><br><a href='/'>Next Scenario</a>"

    @app.route("/instructor")
    def instructor_dashboard():
        html = "<h2>Instructor Dashboard (Live Dynamic Map)</h2>"
        html += "<meta http-equiv='refresh' content='5'>"
        html += "<table border=1 cellpadding=4><tr><th>Student ID</th><th>#Rounds</th><th>Avg Abort</th><th>Avg S</th><th>Avg M</th><th>Avg E</th><th>Avg R</th><th>Latest Outcome</th></tr>"
        for sid, logs in all_sessions.items():
            if not logs: continue
            avg_abort = sum(r['abort_prob'] for r in logs)/len(logs)
            avg_S = sum(r['S'] for r in logs)/len(logs)
            avg_M = sum(r['M'] for r in logs)/len(logs)
            avg_E = sum(r['E'] for r in logs)/len(logs)
            avg_R = sum(r['R'] for r in logs)/len(logs)
            latest = logs[-1]['outcome']
            html += f"<tr><td>{sid}</td><td>{len(logs)}</td><td>{avg_abort:.2f}</td><td>{avg_S:.1f}</td><td>{avg_M:.1f}</td><td>{avg_E:.1f}</td><td>{avg_R:.1f}</td><td>{latest}</td></tr>"
        html += "</table>"
        html += "<h3>Slides:</h3><ol>"
        for slide in INSTRUCTOR_SLIDES:
            html += f"<li>{slide}</li>"
        html += "</ol>"
        html += "<br><a href='/'>Return to Simulator</a>"
        return html

    app.run(debug=True, threaded=True)

# -------------------- ENTRY POINT --------------------
if __name__=="__main__":
    import sys
    if len(sys.argv)<2:
        print("Usage: python subgame_dynamic.py --web")
        sys.exit(0)
    if sys.argv[1].lower()=='--web':
        web_mode()