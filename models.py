import json
import os
import datetime
import logging

STATION_LOG_FILE = 'station_log.json'
BLOG_POSTS_FILE = 'blog_posts.json'

def load_station_log():
    """Load station log from JSON file"""
    if not os.path.exists(STATION_LOG_FILE):
        # Create default station log
        default_log = {
            "header": {
                "station_callsign": "KM6KFX",
                "operator": "KM6KFX",
                "created_timestamp": datetime.datetime.now().isoformat(),
                "last_updated": datetime.datetime.now().isoformat(),
                "total_contacts": 0,
                "adif_version": "3.1.4"
            },
            "contacts": []
        }
        save_station_log(default_log)
        return default_log
    
    try:
        with open(STATION_LOG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading station log: {e}")
        return {"header": {}, "contacts": []}

def save_station_log(station_log):
    """Save station log to JSON file"""
    try:
        # Create backup
        if os.path.exists(STATION_LOG_FILE):
            backup_file = 'station_log_backup.json'
            with open(STATION_LOG_FILE, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
        
        with open(STATION_LOG_FILE, 'w') as f:
            json.dump(station_log, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving station log: {e}")
        raise

def load_blog_posts():
    """Load blog posts from JSON file"""
    if not os.path.exists(BLOG_POSTS_FILE):
        # Create default blog posts
        default_posts = {
            "posts": [
                {
                    "id": 1,
                    "title": "Welcome to Hamlogblog",
                    "content": "Welcome to my amateur radio log blog! This is where I'll be sharing my contacts, experiences, and thoughts about amateur radio.\n\nThis blog serves as both a public showcase of my station activities and a personal log of my amateur radio journey. You'll find information about recent contacts, technical discussions, and insights from my time on the air.\n\nThe site features a complete contact management system with ADIF import capabilities, allowing me to maintain a comprehensive log while sharing interesting contacts and experiences with the amateur radio community.\n\nStay tuned for updates about my station setup, interesting DX contacts, contest activities, and technical projects. 73!",
                    "excerpt": "Welcome to my amateur radio log blog! A place to share contacts, experiences, and technical discussions.",
                    "date": datetime.datetime.now().strftime('%Y-%m-%d')
                }
            ],
            "next_id": 2
        }
        save_blog_posts(default_posts)
        return default_posts
    
    try:
        with open(BLOG_POSTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading blog posts: {e}")
        return {"posts": [], "next_id": 1}

def save_blog_posts(blog_posts):
    """Save blog posts to JSON file"""
    try:
        with open(BLOG_POSTS_FILE, 'w') as f:
            json.dump(blog_posts, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving blog posts: {e}")
        raise

def merge_contacts(existing_contacts, new_contacts):
    """Merge new contacts with existing ones, avoiding duplicates"""
    # Create lookup for existing contacts
    existing_lookup = {}
    for i, contact in enumerate(existing_contacts):
        key = (contact.get('call', ''), contact.get('qso_date', ''), contact.get('time_on', ''))
        existing_lookup[key] = i
    
    merged_contacts = existing_contacts.copy()
    updated_count = 0
    
    for new_contact in new_contacts:
        key = (new_contact.get('call', ''), new_contact.get('qso_date', ''), new_contact.get('time_on', ''))
        
        if key in existing_lookup:
            # Contact exists, merge additional fields
            existing_index = existing_lookup[key]
            existing_contact = merged_contacts[existing_index]
            
            # Merge new fields that aren't empty
            for field, value in new_contact.items():
                if value and (field not in existing_contact or not existing_contact[field]):
                    existing_contact[field] = value
            
            updated_count += 1
        else:
            # New contact, add it
            merged_contacts.append(new_contact)
    
    return merged_contacts, updated_count
