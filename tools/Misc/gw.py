import random

# Base decisions
decisions = {
    'A': 'Stay Submerged',
    'B': 'Brief Pop',
    'C': 'Deploy USV',
    'D': 'Call Escorts',
    'E': 'Extended Surface'
}

# Scenario templates with attributes
scenario_templates = [
    {'name': 'Unescorted Helo inbound', 'threat':'helicopter', 'distance_km':50, 'has_magura':False, 'ROE':'Permissive', 'visibility':'normal', 'night_ops':False},
    {'name': 'Patrol aircraft with escort', 'threat':'helicopter', 'distance_km':40, 'has_magura':False, 'ROE':'Restricted', 'visibility':'normal', 'night_ops':False},
    {'name': 'Surface group with loitering ASW', 'threat':'loitering_missile', 'distance_km':60, 'has_magura':False, 'ROE':'Constrained', 'visibility':'normal', 'night_ops':False},
    {'name': 'Low visibility recon drone', 'threat':'UAV', 'distance_km':45, 'has_magura':False, 'ROE':'Permissive', 'visibility':'poor', 'night_ops':False},
    {'name': 'Submarine tracked by UAVs', 'threat':'UAV', 'distance_km':50, 'has_magura':True, 'ROE':'Restricted', 'visibility':'normal', 'night_ops':True},
    {'name': 'Magura engagement context', 'threat':'helicopter', 'distance_km':30, 'has_magura':True, 'ROE':'Constrained', 'visibility':'normal', 'night_ops':False},
    {'name': 'Air to surface missile threat', 'threat':'missile', 'distance_km':40, 'has_magura':False, 'ROE':'Constrained', 'visibility':'normal', 'night_ops':False},
    {'name': 'High altitude ASW aircraft', 'threat':'ASW_aircraft', 'distance_km':70, 'has_magura':False, 'ROE':'Permissive', 'visibility':'normal', 'night_ops':False},
    {'name': 'Helicopter swarm detected', 'threat':'helicopter', 'distance_km':25, 'has_magura':True, 'ROE':'Restricted', 'visibility':'normal', 'night_ops':False},
    {'name': 'Naval gunfire support present', 'threat':'surface_ships', 'distance_km':15, 'has_magura':False, 'ROE':'Restricted', 'visibility':'normal', 'night_ops':False}
]

# Decision effectiveness matrix by threat type
decision_effectiveness = {
    'helicopter':    {'A':0.8, 'B':0.3, 'C':0.5, 'D':0.6, 'E':0.1},
    'ASW_aircraft':  {'A':0.9, 'B':0.4, 'C':0.5, 'D':0.6, 'E':0.2},
    'loitering_missile': {'A':0.7, 'B':0.2, 'C':0.6, 'D':0.5, 'E':0.1},
    'UAV':           {'A':0.85, 'B':0.4, 'C':0.7, 'D':0.6, 'E':0.3},
    'missile':       {'A':0.75, 'B':0.3, 'C':0.5, 'D':0.6, 'E':0.1},
    'surface_ships': {'A':0.6, 'B':0.4, 'C':0.5, 'D':0.7, 'E':0.3}
}

# Global modifiers
modifiers = {
    'escorted': -0.4,
    'loitering_missile': -0.5,
    'poor_visibility': -0.2,
    'ROE_constrained': -0.3,
    'USV_on_station': 0.1,
    'night_operations': -0.1,
    'magura_context': -0.3
}

def ascii_decision_map():
    print("\n[Decision Map]")
    print("A: Stay Submerged  |  B: Brief Pop")
    print("C: Deploy USV       |  D: Call Escorts")
    print("E: Extended Surface |  Q: Quit")
    print("Legend: S=Survivability, M=Mission, E=Escalation, R=Resource cost")

def calculate_abort_prob(scenario, decision, applied_mods):
    base = decision_effectiveness[scenario['threat']][decision]
    modifier_total = 0
    if scenario['has_magura'] and decision in ['B','E']:
        modifier_total += modifiers['magura_context']
    if scenario['visibility']=='poor':
        modifier_total += modifiers['poor_visibility']
    if scenario['night_ops']:
        modifier_total += modifiers['night_operations']
    if scenario['ROE']=='Constrained':
        modifier_total += modifiers['ROE_constrained']
    for k,v in applied_mods.items():
        if v:
            modifier_total += modifiers.get(k,0)
    abort_prob = max(0, min(1, base + modifier_total))
    return abort_prob

def apply_outcome(abort_prob):
    roll = random.random()
    if roll <= abort_prob:
        S = random.randint(90,98)
        M = random.randint(30,50)
        E = random.randint(10,20)
        R = random.randint(10,25)
        outcome = 'Deterrence successful: attacker aborts.'
    else:
        S = random.randint(30,70)
        M = random.randint(0,20)
        E = random.randint(30,50)
        R = random.randint(20,50)
        outcome = 'Attacker persists: risk increased.'
    total_score = 0.5*S + 0.3*M - 0.1*E - 0.1*R
    return outcome, S, M, E, R, total_score

def suggest_tactical_hint(scenario):
    abort_probs = {}
    for d in decisions:
        # compute a temporary abort probability without random mods for hint
        abort_probs[d] = calculate_abort_prob(scenario, d, {'escorted':False,'loitering_missile':False,'USV_on_station':False})
    # Higher abort prob = safer
    best_decision = max(abort_probs, key=abort_probs.get)
    return best_decision, abort_probs[best_decision]

# Main loop
print("\nSubmarine Littoral Decision Vignettes — Tactical Hint Version\n")
cumulative_scores = {'S':0, 'M':0, 'E':0, 'R':0, 'total':0}

while True:
    scenario = random.choice(scenario_templates)
    print(f"\n--- Scenario: {scenario['name']} ---")
    print(f"Threat: {scenario['threat']}, Distance: {scenario['distance_km']}km")
    print(f"Magura Drones: {scenario['has_magura']}, ROE: {scenario['ROE']}")
    print(f"Visibility: {scenario['visibility']}, Night Ops: {scenario['night_ops']}\n")

    ascii_decision_map()
    
    hint_decision, hint_prob = suggest_tactical_hint(scenario)
    print(f"Tactical Hint: Consider '{decisions[hint_decision]}' (estimated abort probability: {hint_prob:.2f})\n")

    decision = input("Enter your decision (A-E) or Q to quit: ").upper()
    if decision == 'Q':
        break
    if decision not in decisions:
        print("Invalid input. Defaulting to Stay Submerged.")
        decision = 'A'

    applied_mods = {
        'escorted': random.choice([True,False]),
        'loitering_missile': random.choice([True,False]),
        'USV_on_station': random.choice([True,False])
    }

    abort_prob = calculate_abort_prob(scenario, decision, applied_mods)
    outcome, S, M, E, R, total_score = apply_outcome(abort_prob)

    print(f"\nOutcome: {outcome}")
    print(f"Survivability (S): {S}")
    print(f"Mission (M): {M}")
    print(f"Escalation (E): {E}")
    print(f"Resource cost (R): {R}")
    print(f"Total Score: {total_score:.1f}")
    print(f"Modifiers applied: {', '.join([k for k,v in applied_mods.items() if v])}")
    print("Debrief: Tactical hint applied based on scenario-threat interaction.\n")

    cumulative_scores['S'] += S
    cumulative_scores['M'] += M
    cumulative_scores['E'] += E
    cumulative_scores['R'] += R
    cumulative_scores['total'] += total_score

print("--- Cumulative Scores ---")
print(f"Total Survivability (S): {cumulative_scores['S']}")
print(f"Total Mission (M): {cumulative_scores['M']}")
print(f"Total Escalation (E): {cumulative_scores['E']}")
print(f"Total Resource cost (R): {cumulative_scores['R']}")
print(f"Total Combined Score: {cumulative_scores['total']:.1f}")
print("\nSimulation complete. Tactical hints were integrated.")