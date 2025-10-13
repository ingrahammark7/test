import random

# Base probability table
probabilities = {
    'A': {'abort': 0.6, 'persist': 0.4},      # Stay Submerged
    'B': {'abort': 0.75, 'persist': 0.25},    # Brief Pop
    'C': {'abort': 0.8, 'persist': 0.2},      # Deploy USV
    'D': {'abort': 0.85, 'persist': 0.15},    # Call Escorts
    'E': {'abort': 0.3, 'persist': 0.7},      # Extended Surface
}

# Modifiers for environmental and tactical factors
modifiers = {
    'escorted': -0.4,
    'loitering_missile': -0.5,
    'poor_visibility': -0.2,
    'ROE_constrained': -0.3,
    'USV_on_station': 0.1,
    'night_operations': -0.1,
    'magura_context': 0.2
}

def random_vignette():
    names = [
        'Unescorted Helo inbound',
        'Patrol aircraft with escort',
        'Surface group with loitering ASW',
        'Low visibility recon drone',
        'Submarine tracked by UAVs',
        'Magura engagement context',
        'Helicopter swarm detected',
        'Air to surface missile threat',
        'High altitude ASW aircraft',
        'Naval gunfire support present'
    ]
    descs = [
        'Sub at 60-80m, battery 30-60%, USV available',
        'Sub at 50-90m, battery 20-55%, escorts nearby',
        'Sub at 40-70m, battery 25-50%, loitering torpedo reported',
        'Sub at 50-80m, poor visibility, EO limited',
        'Sub at 60m, tracked by UAV, MANPADS available',
        'Sub at 50m, battery 45%, Magura drones deployed',
        'Sub at 55m, helicopters inbound in swarm',
        'Sub at 60m, incoming air-to-surface missiles',
        'Sub at 80m, ASW aircraft high altitude, torpedo drop imminent',
        'Sub at 45m, surface ships within 20km, naval gunfire possible'
    ]
    ROEs = ['Permissive', 'Restricted', 'Constrained']
    idx = random.randint(0, len(names)-1)
    return {'name': names[idx], 'desc': descs[idx], 'ROE': random.choice(ROEs)}

def apply_outcome(decision, modified_abort_prob):
    roll = random.random()
    if roll <= modified_abort_prob:
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

def ascii_decision_map():
    print("\n[Decision Map]")
    print("A: Stay Submerged  |  B: Brief Pop")
    print("C: Deploy USV       |  D: Call Escorts")
    print("E: Extended Surface |  Q: Quit")
    print("Legend: S=Survivability, M=Mission, E=Escalation, R=Resource cost")

print("\nSubmarine Littoral Decision Vignettes — Full Feature Endless Simulation\n")
cumulative_scores = {'S':0, 'M':0, 'E':0, 'R':0, 'total':0}

while True:
    vignette = random_vignette()
    print(f"\n--- New Random Vignette: {vignette['name']} ---")
    print(f"Description: {vignette['desc']}")
    print(f"ROE: {vignette['ROE']}\n")

    # Show ASCII decision map
    ascii_decision_map()

    # Player input
    decision = input("Enter your decision (A-E) or Q to quit: ").upper()
    if decision == 'Q':
        break
    if decision not in ['A','B','C','D','E']:
        print("Invalid decision. Defaulting to Stay Submerged.")
        decision = 'A'

    # Random modifiers including all features
    modifiers_applied = {
        'escorted': random.choice([True, False]),
        'loitering': random.choice([True, False]),
        'poor_visibility': random.choice([True, False]),
        'ROE_constrained': random.choice([True, False]),
        'USV_station': random.choice([True, False]),
        'night_operations': random.choice([True, False]),
        'magura_context': random.choice([True, False])
    }

    # Calculate modified probability
    base_abort = probabilities[decision]['abort']
    modifier_total = 0
    for key, active in modifiers_applied.items():
        if active:
            modifier_total += modifiers.get(key, 0)
    modified_abort = max(0, min(1, base_abort + modifier_total))

    # Apply outcome
    outcome, S, M, E, R, total_score = apply_outcome(decision, modified_abort)

    # Print round results with all features
    print(f"\nOutcome: {outcome}")
    print(f"Survivability (S): {S}")
    print(f"Mission (M): {M}")
    print(f"Escalation (E): {E}")
    print(f"Resource cost (R): {R}")
    print(f"Total Score: {total_score:.1f}")
    print(f"Modifiers applied: {', '.join([k for k,v in modifiers_applied.items() if v])}")
    print("Debrief: Adapt strategy for next round using situational awareness, Magura drones, and ROE rules.\n")

    # Update cumulative scores
    cumulative_scores['S'] += S
    cumulative_scores['M'] += M
    cumulative_scores['E'] += E
    cumulative_scores['R'] += R
    cumulative_scores['total'] += total_score

# Print cumulative results
print("--- Cumulative Scores ---")
print(f"Total Survivability (S): {cumulative_scores['S']}")
print(f"Total Mission (M): {cumulative_scores['M']}")
print(f"Total Escalation (E): {cumulative_scores['E']}")
print(f"Total Resource cost (R): {cumulative_scores['R']}")
print(f"Total Combined Score: {cumulative_scores['total']:.1f}")
print("\nSimulation complete. All features exhausted.")