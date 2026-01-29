"""
PhysioCore Parameters - Biological Constants.
Defines baselines, decay rates (half-life), and thresholds.
"""

# Biological Constants
TICK_RATE_HZ = 30  # Simulation updates per second (virtual time)
SEC_PER_TICK = 1.0 / TICK_RATE_HZ

# 1. Hormone Baselines (Homeostatic Targets)
# Range: 0.0 to 1.0
BASELINES = {
    "dopamine": 0.5,      # Reward/Drive
    "serotonin": 0.5,     # Mood/Stability
    "oxytocin": 0.5,      # Social/Warmth
    "cortisol": 0.3,      # Stress/Alertness (lower baseline for health)
    "adrenaline": 0.2,    # Fight/Flight (low baseline)
    "endorphin": 0.2,     # Pain relief/Joy
    "acetylcholine": 0.5, # Focus/Learning
    "noradrenaline": 0.3, # Vigilance
    "melatonin": 0.1,     # Circadian (varies by time)
    "testosterone": 0.5,  # Dominance/Confidence
    "estrogen": 0.5,      # Empathy/Sensitivity
    "vasopressin": 0.5    # Memory/Bonding
}

# 2. Decay Rates (Half-life in Virtual Seconds)
# How fast hormones return to baseline
# Fast decay = volatile emotion (e.g. Adrenaline)
# Slow decay = mood (e.g. Serotonin)
HALF_LIVES = {
    "dopamine": 300,      # 5 mins
    "serotonin": 1800,    # 30 mins
    "oxytocin": 1200,     # 20 mins
    "cortisol": 900,      # 15 mins
    "adrenaline": 60,     # 1 min (very fast drop)
    "endorphin": 600,     # 10 mins
    "acetylcholine": 300, # 5 mins
    "noradrenaline": 120, # 2 mins
    "melatonin": 3600,    # 1 hour
    "testosterone": 3600, # 1 hour
    "estrogen": 3600,     # 1 hour
    "vasopressin": 1800   # 30 mins
}

# 3. Stimulus Impact Map
# Maps abstract stimuli to hormone secretions (Synthesis)
STIMULUS_MAP = {
    "praise": {"dopamine": 0.2, "oxytocin": 0.1},
    "threat": {"adrenaline": 0.4, "cortisol": 0.2},
    "task_completion": {"dopamine": 0.3, "endorphin": 0.1},
    "social_connection": {"oxytocin": 0.3, "serotonin": 0.1},
    "learning": {"acetylcholine": 0.3},
    "confusion": {"cortisol": 0.1, "noradrenaline": 0.1},
    "timeout": {"cortisol": 0.05}
}
