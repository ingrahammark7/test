import time
import json
import numpy as np
from collections import Counter


# =========================================================
# ACTION SPACE (PURE LABELS ONLY)
# =========================================================

ACTIONS = ["left", "right", "up", "down", "click"]


# =========================================================
# SCREEN (EXTERNAL - ASSUMED PROVIDED)
# =========================================================

class ScreenProvider:
    def get(self):
        # external system provides observation
        return np.zeros((84, 84))


# =========================================================
# HUMAN INPUT (OPTIONAL EXTERNAL SIGNAL)
# =========================================================

class HumanInput:
    def poll(self):
        return None


# =========================================================
# YOUR AI (EXTERNAL MODEL)
# =========================================================

class YourAI:
    def act(self, observation, human_event=None):
        # external policy returns action label
        return "click"


# =========================================================
# LOGGER (INTERNAL ONLY FUNCTIONALITY)
# =========================================================

class Logger:
    def __init__(self):
        self.logs = []

    def log(self, step, obs, action):
        self.logs.append({
            "step": step,
            "obs_mean": float(np.mean(obs)),
            "action": action,
            "t": time.time()
        })

    def save(self, path="run_log.json"):
        with open(path, "w") as f:
            json.dump(self.logs, f, indent=2)


# =========================================================
# EVALUATION (STATISTICAL ONLY)
# =========================================================

def entropy(actions):
    c = Counter(actions)
    total = len(actions)
    probs = [v / total for v in c.values()]
    return -sum(p * np.log(p + 1e-9) for p in probs)


def evaluate(logs):
    actions = [l["action"] for l in logs]
    obs_vals = [l["obs_mean"] for l in logs]

    return {
        "entropy": entropy(actions),
        "click_rate": actions.count("click") / len(actions),
        "stability": 1.0 - np.std(obs_vals)
    }


# =========================================================
# HARNESS (NO ASSUMPTIONS, NO SIDE EFFECTS)
# =========================================================

class EvaluationHarness:
    def __init__(self, policy, screen):
        self.policy = policy
        self.screen = screen
        self.human = HumanInput()
        self.logger = Logger()

    def run(self, steps=500):

        for i in range(steps):

            obs = self.screen.get()
            human_event = self.human.poll()

            action = self.policy.act(obs, human_event)

            self.logger.log(i, obs, action)

            if i % 50 == 0:
                print("step", i)

        self.logger.save()
        return self.logger.logs


# =========================================================
# RUNNER
# =========================================================

def run_system(policy, screen):
    harness = EvaluationHarness(policy, screen)

    logs = harness.run(steps=500)

    metrics = evaluate(logs)

    print("\n=== EVALUATION ===")
    print("Entropy:", metrics["entropy"])
    print("Click rate:", metrics["click_rate"])
    print("Stability:", metrics["stability"])

    return metrics


# =========================================================
# ENTRY POINT (NO REQUIREMENTS)
# =========================================================

if __name__ == "__main__":
    policy = YourAI()
    screen = ScreenProvider()

    run_system(policy, screen)