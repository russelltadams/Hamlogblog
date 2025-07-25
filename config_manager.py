"""Configuration management for QSOWhat application"""
import json
import os
from typing import Dict, Any

CONFIG_FILE = 'config.json'

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Return default configuration if file doesn't exist
            return get_default_config()
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config: {e}")
        return get_default_config()

def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to config.json file"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False

def get_default_config() -> Dict[str, Any]:
    """Return default configuration"""
    return {
        "station": {
            "call_sign": "N0CALL",
            "operator_name": "Amateur Radio Operator",
            "qth": "Somewhere, USA",
            "grid_square": "AA00",
            "email": "operator@example.com"
        },
        "site": {
            "title": "QSOWhat",
            "subtitle": "Amateur Radio Log & Activities",
            "description": "Personal amateur radio logging and blog site",
            "admin_password": "changeme"
        },
        "qsl": {
            "default_message": "Thanks for the QSO! 73s",
            "equipment": "Various transceivers",
            "antenna": "Various antennas",
            "power": "Legal limit"
        },
        "display": {
            "timezone": "UTC",
            "date_format": "YYYY-MM-DD",
            "contacts_per_page": 50,
            "recent_contacts_limit": 10
        }
    }

def get_config_value(path: str, default=None):
    """Get a configuration value using dot notation (e.g., 'station.call_sign')"""
    config = load_config()
    keys = path.split('.')
    
    current = config
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return default

def update_config_value(path: str, value: Any) -> bool:
    """Update a configuration value using dot notation"""
    config = load_config()
    keys = path.split('.')
    
    current = config
    try:
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value
        current[keys[-1]] = value
        return save_config(config)
    except (KeyError, TypeError):
        return False