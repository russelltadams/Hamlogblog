import os
import logging
from flask import Flask, session
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "hamlogblog-default-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Admin credentials
ADMIN_USERNAME = "KM6KFX"
ADMIN_PASSWORD = "happyham"

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            from flask import redirect, url_for
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Import routes after app initialization
import routes  # noqa: F401
