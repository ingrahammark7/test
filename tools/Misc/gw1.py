"""
Unified Submarine Littoral Training Simulator
Run:
  Terminal CLI: python subgame_all.py --cli
  Web simulator: python subgame_all.py --web
Dependencies:
  - Python 3.8+
  - reportlab (pip install reportlab)
  - flask (pip install flask) [web mode]
  - curses (Windows: pip install windows-curses) [CLI mode]
"""

import random, datetime, io, sys

# --- COMMON DATA ---
DECISIONS = {'A':'Stay Submerged','B':'Brief Pop','C':'Deploy USV','D':'Call Escorts','E':'Extended Surface'}
SCENARIOS = [
    {'name':'Helo unescorted','threat':'helicopter','distance_km':50,'has_magura':False,'ROE':'Permissive','visibility':'normal','night_ops':False,'sonobuoy_net':'good','torpedo_missile_on_station':False},
    {'name':'ASW with torpedo-missile','threat':'ASW_aircraft','distance_km':45,'has_magura':False,'ROE':'Restricted','visibility':'normal','night_ops':False,'sonobuoy_net':'good','torpedo_missile_on_station':True},
    {'name':'Magura defended littoral','threat':'helicopter','distance_km':30,'has_magura':True,'ROE':'Constrained','visibility':'normal','night_ops':False,'sonobuoy_net':'poor','torpedo_missile_on_station':False},
    {'name':'UAV tracking & USV loiterers','threat':'UAV','distance_km':60,'has_magura':False,'ROE':'Permissive','visibility':'poor','night_ops':True,'sonobuoy_net':'good','torpedo_missile_on_station':False}
]
BASE_EFFECT = {'helicopter':{'A':0.8,'B':0.3,'C':0.5,'D':0.6,'E':0.1},
               'ASW_aircraft':{'A':0.85,'B':0.4,'C':0.5,'D':0.6,'E':0.2},
               'UAV':{'A':0.8,'B':0.4,'C':0.7,'D':0.6,'E':0.3}}
MODS = {'escorted':-0.4,'magura':-0.3,'poor_vis':-0.2,'torp_missile':-0.6,'USV_armed':0.2,'sonobuoy_poor':-0.15,'accessory_present':0.25}

INSTRUCTOR_SLIDES = [
    "Slide 1: Learning objectives — sensor/timing windows, cost asymmetry, unmanned assets, ROE",
    "Slide 2: Setup — assign player & umpire, preconfigured scenario, logging",
    "Slide 3: Playthrough — 10-15 min per vignette, decisions announced, run sim",
    "Slide 4: Debrief — S/M/E/R outcomes, cues used, alternatives",
    "Slide 5: Assessment — 0.5*S + 0.3*M - 0.1*E - 0.1*R, compare students",
    "Slide 6: Homework — propose one kit or doctrine change for Magura context"
]

session_log = []

# --- SIMULATOR ---
def compute_abort(scenario, decision, ephemeral):
    base = BASE_EFFECT.get(scenario['threat'], {}).get(decision, 0.5)
    base += min(0.2, max(0, (scenario['distance_km']-10)/200.0))
    mod = 0.0
    if scenario.get('has_magura') and decision in ['B','E']: mod += MODS['magura']
    if scenario.get('torpedo_missile_on_station'): mod += MODS['torp_missile']
    if scenario.get('visibility')=='poor': mod += MODS['poor_vis']
    if scenario.get('sonobuoy_net')=='poor': mod += MODS['sonobuoy_poor']
    if ephemeral.get('escorted'): mod += MODS['escorted']
    if ephemeral.get('USV_armed'): mod += MODS['USV_armed']
    if ephemeral.get('accessory_present'): mod += MODS['accessory_present']
    return max(0,min(1,base+mod))

def simulate_decision(scenario, decision, ephemeral):
    abort_prob = compute_abort(scenario, decision, ephemeral)
    r = random.random()
    if r <= abort_prob: S,M,E,R = 95,40,10,15; outcome='Abort'
    else: S=random.randint(20,70); M=random.randint(0,30); E=random.randint(30,60); R=random.randint(20,60); outcome='Engaged'
    return {'scenario':scenario,'decision':decision,'ephemeral':ephemeral,'abort_prob':abort_prob,'S':S,'M':M,'E':E,'R':R,'outcome':outcome}

# --- PDF Export ---
def export_session_pdf(session_data, filename="submarine_session.pdf"):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        fname = filename.replace(".pdf",".txt")
        with open(fname,"w") as f:
            f.write("Session Log\n")
            for idx,r in enumerate(session_data):
                f.write(f"Round {idx+1}: {r['scenario']['name']}, Decision: {r['decision']}, Outcome: {r['outcome']}, Abort Prob: {r['abort_prob']:.2f}, S:{r['S']},M:{r['M']},E:{r['E']},R:{r['R']}\n")
        print("reportlab not installed. Text export:", fname)
        return fname
    buffer = filename
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - margin
    c.setFont("Helvetica-Bold",14)
    c.drawString(margin,y,"Submarine Littoral Training Session")
    y -= 20
    c.setFont("Helvetica",9)
    c.drawString(margin,y,"Generated: "+datetime.datetime.utcnow().isoformat()+"Z")
    y -= 16
    c.line(margin,y,width-margin,y)
    y -= 18
    for idx,r in enumerate(session_data):
        if y<80: c.showPage(); y=height-margin
        c.setFont("Helvetica-Bold",11)
        c.drawString(margin,y,f"Round {idx+1}: {r['scenario']['name']}")
        y-=14
        c.setFont("Helvetica",10)
        c.drawString(margin+10,y,f"Decision: {r['decision']} | Outcome: {r['outcome']}")
        y-=12
        c.drawString(margin+10,y,f"Abort Prob: {r['abort_prob']:.2f} S:{r['S']} M:{r['M']} E:{r['E']} R:{r['R']}")
        y-=16
    c.save()
    print("Exported PDF:", buffer)
    return buffer

# --- CLI MODE ---
def cli_mode():
    import curses
    def run_cli(stdscr):
        curses.curs_set(0)
        while True:
            scenario = random.choice(SCENARIOS)
            stdscr.clear()
            stdscr.addstr(0,0,f"Scenario: {scenario['name']}")
            stdscr.addstr(1,0,f"Threat: {scenario['threat']} Distance: {scenario['distance_km']} km Magura:{scenario['has_magura']}")
            stdscr.addstr(3,0,"Decisions:")
            for k,v in DECISIONS.items(): stdscr.addstr(f"{k} - {v}\n")
            stdscr.addstr("Choose decision (A-E) or Q to quit: ")
            stdscr.refresh()
            ch = stdscr.getkey().upper()
            if ch=='Q': break
            if ch not in DECISIONS: ch='A'
            ephemeral = {'escorted': random.choice([False, True, False]),
                         'accessory_present': random.choice([False, False, True]),
                         'USV_armed': ch=='C' and random.choice([True,False])}
            result = simulate_decision(scenario,ch,ephemeral)
            session_log.append(result)
            stdscr.addstr(f"Outcome: {result['outcome']}, Abort Prob:{result['abort_prob']:.2f}, S:{result['S']} M:{result['M']} E:{result['E']} R:{result['R']}\n")
            stdscr.addstr("Press any key to continue...")
            stdscr.getch()
    curses.wrapper(run_cli)
    export_session_pdf(session_log)

# --- WEB MODE ---
def web_mode():
    from flask import Flask, render_template_string, request, send_file
    app = Flask(__name__)

    @app.route("/")
    def index():
        scenario = random.choice(SCENARIOS)
        idx = SCENARIOS.index(scenario)
        return render_template_string("""
            <h2>Submarine Littoral Simulator</h2>
            <h3>Scenario: {{scenario.name}}</h3>
            <ul>
                <li>Threat: {{scenario.threat}}</li>
                <li>Distance: {{scenario.distance_km}} km</li>
                <li>Magura: {{scenario.has_magura}}</li>
                <li>Torpmissile: {{scenario.torpedo_missile_on_station}}</li>
            </ul>
            <form method="post" action="/decide">
                <input type="hidden" name="idx" value="{{idx}}">
                {% for k,v in decisions.items() %}
                    <input type="radio" name="decision" value="{{k}}" required> {{k}} - {{v}}<br>
                {% endfor %}
                <input type="submit" value="Submit Decision">
            </form>
            <br><a href="/log">Session Log</a> | <a href="/export">Export PDF</a> | <a href="/instructor">Instructor Dashboard</a>
        """, scenario=scenario, idx=idx, decisions=DECISIONS)

    @app.route("/decide", methods=['POST'])
    def decide():
        idx = int(request.form['idx'])
        scenario = SCENARIOS[idx]
        decision = request.form['decision']
        ephemeral = {'escorted': random.choice([False,True,False]),
                     'accessory_present': random.choice([False,False,True]),
                     'USV_armed': decision=='C' and random.choice([True,False])}
        result = simulate_decision(scenario,decision,ephemeral)
        session_log.append(result)
        return render_template_string("""
            <h2>Decision Result</h2>
            <p>Decision: {{result.decision}} | Outcome: {{result.outcome}}</p>
            <p>Abort Probability: {{result.abort_prob:.2f}}</p>
            <p>Scores: S={{result.S}}, M={{result.M}}, E={{result.E}}, R={{result.R}}</p>
            <p>Ephemeral Factors: {{result.ephemeral}}</p>
            <br><a href="/">Next Scenario</a> | <a href="/log">View Log</a> | <a href="/export">Export PDF</a> | <a href="/instructor">Instructor Dashboard</a>
        """, result=result)

    @app.route("/log")
    def log_view():
        html = "<h2>Session Log</h2><ul>"
        for r in session_log:
            html += f"<li>Scenario: {r['scenario']['name']} | Decision: {r['decision']} | Outcome: {r['outcome']} | Abort Prob: {r['abort_prob']:.2f}</li>"
        html += "</ul><br><a href='/'>Next Scenario</a> | <a href='/export'>Export PDF</a> | <a href='/instructor'>Instructor Dashboard</a>"
        return html

    @app.route("/export")
    def export_pdf():
        buffer = io.BytesIO()
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(buffer, pagesize=letter)
            width,height = letter
            margin=40
            y=height-margin
            c.setFont("Helvetica-Bold",14)
            c.drawString(margin,y,"Submarine Littoral Training Session")
            y-=20
            c.setFont("Helvetica",9)
            c.drawString(margin,y,"Generated: "+datetime.datetime.utcnow().isoformat()+"Z")
            y-=16
            c.line(margin,y,width-margin,y)
            y-=18
            for idx,r in enumerate(session_log):
                if y<80: c.showPage(); y=height-margin
                c.setFont("Helvetica-Bold",11)
                c.drawString(margin,y,f"Round {idx+1}: {r['scenario']['name']}")
                y-=14
                c.setFont("Helvetica",10)
                c.drawString(margin+10,y,f"Decision: {r['decision']} | Outcome: {r['outcome']}")
                y-=12
                c.drawString(margin+10,y,f"Abort Prob: {r['abort_prob']:.2f} S:{r['S']} M:{r['M']} E:{r['E']} R:{r['R']}")
                y-=16
            c.save()
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="submarine_session.pdf", mimetype='application/pdf')
        except ImportError:
            return "reportlab not installed; cannot export PDF"

    @app.route("/instructor")
    def instructor_dashboard():
        avg_abort = sum(r['abort_prob'] for r in session_log)/max(1,len(session_log))
        avg_S = sum(r['S'] for r in session_log)/max(1,len(session_log))
        html = "<h2>Instructor Dashboard</h2>"
        html += f"<p>Average Abort Probability: {avg_abort:.2f}</p>"
        html += f"<p>Average S Score: {avg_S:.1f}</p>"
        html += "<h3>Slides</h3><ol>"
        for slide in INSTRUCTOR_SLIDES:
            html += f"<li>{slide}</li>"
        html += "</ol><br><a href='/'>Return to Simulator</a>"
        return html

    app.run(debug=True)

# --- ENTRY POINT ---
if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python subgame_all.py --cli | --web")
        sys.exit(0)
    mode = sys.argv[1].lower()
    if mode=='--cli':
        cli_mode()
    elif mode=='--web':
        web_mode()
    else:
        print("Unknown mode:", mode)