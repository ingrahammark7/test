# radar.py

import math
import random

class Radar:
    def __init__(self, max_range_km=50, base_detection_prob=0.9):
        """
        max_range_km: maximum radar detection range in kilometers.
        base_detection_prob: base probability to detect a target at close range.
        """
        self.max_range_km = max_range_km
        self.base_detection_prob = base_detection_prob
        self.jamming_level = 0.0  # 0.0 = no jamming, 1.0 = full jam

    def set_jamming_level(self, level):
        """
        Set ECM jamming level (0.0 to 1.0).
        """
        self.jamming_level = max(0.0, min(1.0, level))

    def detect(self, own_position, target_position, target_rcs):
        """
        Returns True if the radar detects the target, False otherwise.

        Detection probability is affected by:
        - Distance: detection probability falls off linearly from base_detection_prob at zero range to 0 at max_range.
        - Target RCS: larger RCS increases detection.
        - Jamming level: reduces detection chance.

        own_position, target_position: tuples (x, y) in km.
        target_rcs: Radar Cross Section of the target (m²).
        """
        dx = target_position[0] - own_position[0]
        dy = target_position[1] - own_position[1]
        distance = math.hypot(dx, dy)

        if distance > self.max_range_km:
            return False  # Out of radar range

        # Base detection chance drops linearly with distance
        detection_chance = self.base_detection_prob * (1 - distance / self.max_range_km)

        # Adjust detection by RCS (assume typical fighter RCS ~5 m²)
        rcs_factor = target_rcs / 5.0
        detection_chance *= min(2.0, rcs_factor)  # Cap max increase

        # Reduce detection by jamming
        detection_chance *= (1 - self.jamming_level)

        # Clamp detection chance between 0 and 1
        detection_chance = max(0.0, min(1.0, detection_chance))

        return random.random() < detection_chance