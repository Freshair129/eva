"""
PhysioCore Parameters - Biological Constants.
Loads authoritative specs from YAML configurations.
"""

import yaml
from pathlib import Path

# Paths
CONFIG_DIR = Path(__file__).parent / "configs"
HORMONE_SPEC_PATH = CONFIG_DIR / "hormone_spec_ml.yaml"
SYSTEM_CONFIG_PATH = CONFIG_DIR / "PhysioCore_configs.yaml"

def load_hormone_specs():
    """Parses hormone_spec_ml.yaml to extract baselines and half-lives."""
    if not HORMONE_SPEC_PATH.exists():
        return {}, {}, {}

    try:
        with open(HORMONE_SPEC_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"[PhysioCore] Error loading hormone specs: {e}")
        return {}, {}, {}
        
    specs = data.get("chemical_specs", {})
    
    baselines = {}
    half_lives = {}
    mappings = {}
    
    for key, info in specs.items():
        if not isinstance(info, dict): continue
        
        # normalized name: lowercase key (e.g. dopamine) or use name field
        name = info.get("name", key).lower()
        
        # Baseline
        baselines[name] = float(info.get("baseline", 0.0))
        
        # Half-life
        phy = info.get("physical", {})
        half_lives[name] = float(phy.get("half_life_sec", 300))
        
        # Stimulus Mappings
        stim_map = info.get("stimulus_mapping", {})
        if stim_map:
            for stim, impact in stim_map.items():
                if stim not in mappings:
                    mappings[stim] = {}
                mappings[stim][name] = float(impact)

    return baselines, half_lives, mappings

def load_system_config():
    """Parses PhysioCore_configs.yaml."""
    if not SYSTEM_CONFIG_PATH.exists():
        return {}
    try:
        with open(SYSTEM_CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except:
        return {}

# Load Data (Module Level)
BASELINES, HALF_LIVES, STIMULUS_MAP = load_hormone_specs()
SYSTEM_CONFIG = load_system_config()

# Global Defaults
TICK_RATE_HZ = SYSTEM_CONFIG.get("global", {}).get("update_rate_hz", 30)
if TICK_RATE_HZ <= 0: TICK_RATE_HZ = 30
SEC_PER_TICK = 1.0 / TICK_RATE_HZ
