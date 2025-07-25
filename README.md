# QSOWhat - Amateur Radio Log & Blog System

A Flask-based web application designed for amateur radio operators to manage their station logs and maintain a blog about their radio activities. Features ADIF file parsing, contact management, QSL card generation, and an integrated blog platform.

## Features

- **ADIF File Import**: Parse and import Amateur Data Interchange Format (ADIF) log files
- **Contact Management**: View, search, and manage your station contacts
- **QSL Card Generation**: Generate printable QSL cards for contacts
- **Configuration System**: Customize station info, site settings, and QSL preferences
- **Blog System**: Share your amateur radio experiences and activities
- **Statistics Dashboard**: Track your contacts by band, mode, and country
- **Search & Filter**: Advanced search capabilities across your contact log
- **Responsive Design**: Mobile-friendly interface with Bootstrap dark theme

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd qsowhat
   ```

2. **Install Python 3.11+** (if not already installed)

3. **Install dependencies:**
   ```bash
   pip install flask pillow werkzeug gunicorn
   ```
   
   Or using uv (recommended):
   ```bash
   uv add flask pillow werkzeug gunicorn
   ```

4. **Set environment variables:**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```

5. **Run the application:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

6. **Access the application:**
   Open your browser to `http://localhost:5000`

### Production Deployment

#### Using Docker (Recommended)

1. **Create a Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY . .
   
   RUN pip install -r requirements.txt
   
   EXPOSE 5000
   
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
   ```

2. **Build and run:**
   ```bash
   docker build -t qsowhat .
   docker run -p 5000:5000 -e SESSION_SECRET="your-secret-key" qsowhat
   ```

#### Fly.io Deployment (Recommended for Easy Cloud Hosting)

Fly.io offers an excellent platform for deploying Flask applications with minimal configuration. The included `fly.toml` is optimized for two VMs running under the free tier.

1. **Install flyctl CLI:**
   ```bash
   # macOS
   brew install flyctl
   
   # Linux/WSL
   curl -L https://fly.io/install.sh | sh
   
   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Sign up and authenticate:**
   ```bash
   fly auth signup  # or fly auth login if you have an account
   ```

3. **Deploy your application:**
   ```bash
   # Clone and navigate to the project
   git clone <your-repository-url>
   cd qsowhat
   
   # Launch the app (this uses the included fly.toml)
   fly launch --no-deploy
   
   # Set a secure session secret
   fly secrets set SESSION_SECRET="$(openssl rand -hex 32)"
   
   # Deploy
   fly deploy
   ```

4. **Access your application:**
   ```bash
   fly open  # Opens your app in the browser
   ```

**Free Tier Configuration:**
- The included `fly.toml` is configured for 2 VMs with 256MB RAM each
- Auto-scaling: scales down to 0 when idle, scales up on demand
- Free tier includes 160GB-hours per month (sufficient for most amateur radio logs)
- Includes health checks and automatic HTTPS

**Data Persistence:**
QSOWhat uses JSON files for data storage. On Fly.io, data persists across deployments but may be lost if machines are destroyed. For production use with valuable log data, consider:

```bash
# Create a persistent volume for data storage (optional)
fly volumes create qsowhat_data --region ord --size 1

# Then modify fly.toml to mount the volume
# Add to your fly.toml under [mounts]:
# source = "qsowhat_data"
# destination = "/app/data"
```

**Updating your deployment:**
```bash
fly deploy  # Deploy changes
fly logs    # View application logs
fly ssh console  # SSH into your app for debugging
```

#### Direct Deployment

1. **Install dependencies and set up environment variables**
2. **Use a production WSGI server:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 2 main:app
   ```

3. **Set up reverse proxy (nginx example):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

#### Environment Variables

- `SESSION_SECRET`: Required for secure sessions (generate a random string)
  - For fly.io: Set using `fly secrets set SESSION_SECRET="$(openssl rand -hex 32)"`
  - For Docker: Pass as `-e SESSION_SECRET="your-secret-key"`
  - For direct deployment: Export in your shell or use a .env file
- `FLASK_ENV`: Set to `production` for production deployments

## Admin Guide

### Initial Setup

1. **Configure Your Station:**
   - Access Admin Panel → Site Configuration
   - Set your call sign, QTH, grid square, and operator name
   - Customize site title, admin password, and QSL preferences
   - Save configuration (changes take effect after restart)

2. **Access Admin Panel:**
   - Navigate to `/admin_login`
   - Login with your call sign and configured admin password
   - Default: `KM6KFX` / `happyham` (change via configuration)

3. **Import Your Log:**
   - Go to Admin Panel → Upload ADIF File
   - Select your `.adi` or `.adif` file
   - The system will parse and import all contacts

### Managing Contacts

- **View All Contacts**: Browse paginated contact list with search and filter options
- **Contact Details**: Click any contact to see full information
- **Generate QSL Cards**: Create printable QSL cards for individual contacts
- **Export Data**: Download your log as JSON or ADIF format

### Blog Management

1. **Create Posts:**
   - Admin Panel → Blog Management → New Post
   - Add title, content, and publish

2. **Edit/Delete Posts:**
   - Use Blog Management interface to modify existing posts
   - Posts appear immediately on the public blog

### Configuration Management

The application uses a `config.json` file to store all station and site settings:

**Station Information:**
- Call sign (used for site title and admin login)
- Operator name, QTH, grid square, email
- Equipment details for QSL cards

**Site Settings:**
- Site title, subtitle, description
- Admin password and display preferences
- QSL card default message and equipment info

**Configuration Interface:**
- Access via Admin Panel → Site Configuration
- Changes take effect after application restart
- All templates and QSL cards use configuration values

### Data Management

- **Backup**: Regularly export your data using the JSON export feature
- **File Storage**: All data is stored in JSON files (`station_log.json`, `blog_posts.json`, `config.json`)
- **Uploads**: ADIF files are temporarily stored in the `uploads/` directory

## Developer Documentation

### Architecture Overview

```
qsowhat/
├── main.py              # Application entry point
├── app.py              # Flask app configuration and setup
├── routes.py           # All URL routes and view functions
├── models.py           # Data models and file operations
├── adif_parser.py      # ADIF file parsing logic
├── qsl_generator.py    # QSL card image generation
├── config_manager.py   # Configuration management utilities
├── templates/          # Jinja2 HTML templates
├── static/            # CSS, JavaScript, and static assets
├── uploads/           # Temporary file storage
├── config.json        # Station and site configuration
├── station_log.json   # Main contact database
└── blog_posts.json    # Blog content storage
```

### Key Components

#### Data Layer (`models.py`)
- **File-based storage** using JSON for simplicity
- **No database required** - perfect for single-user deployments
- **Backup system** automatically creates backups before data updates

#### ADIF Parser (`adif_parser.py`)
- **Standards compliant** ADIF 3.1.4 parsing
- **Data validation** and cleaning for imported contacts
- **Header extraction** for station information
- **Export capability** back to ADIF format

#### QSL Generator (`qsl_generator.py`)
- **PIL-based image generation** for QSL cards
- **Standard QSL format** with contact details
- **Font fallback system** for cross-platform compatibility

#### Web Interface (`routes.py`)
- **Public routes**: Home, blog, contact viewing, search
- **Admin routes**: File upload, blog management, admin panel
- **Authentication**: Simple session-based admin access

### Technology Stack

- **Backend**: Flask (Python 3.11+)
- **Frontend**: Bootstrap 5 with dark theme
- **Image Processing**: Pillow (PIL)
- **Data Storage**: JSON files
- **Deployment**: Gunicorn WSGI server

### Development Guidelines

#### Adding New Features

1. **Routes**: Add new endpoints in `routes.py`
2. **Templates**: Create HTML templates in `templates/`
3. **Styling**: Use Bootstrap classes, add custom CSS to `static/css/style.css`
4. **Data**: Extend JSON structures in `models.py`

#### Code Style

- **Simple, readable code** following Flask best practices
- **Minimal dependencies** for easy deployment
- **Error handling** with user-friendly messages
- **Security considerations** for file uploads and admin access

#### Testing

```bash
# Run the application in debug mode
export FLASK_ENV=development
python main.py

# Test ADIF parsing
python -c "from adif_parser import parse_adif_file; print(parse_adif_file('test.adi'))"

# Test QSL generation
python -c "from qsl_generator import generate_qsl_card; generate_qsl_card({'call': 'W1AW'}, {})"
```

### API Reference

While primarily a web application, key functions can be used programmatically:

#### ADIF Parser
```python
from adif_parser import parse_adif_file, contacts_to_adif

# Parse ADIF file
result = parse_adif_file('logbook.adi')
contacts = result['contacts']
header = result['header']

# Convert back to ADIF
adif_content = contacts_to_adif(contacts, header)
```

#### Data Models
```python
from models import load_station_log, save_station_log

# Load current log
station_log = load_station_log()

# Access contacts
contacts = station_log['contacts']

# Save changes
save_station_log(station_log)
```

## Security Considerations

- **Change default admin credentials** before deployment
- **Use HTTPS** in production with proper TLS certificates
- **Secure SESSION_SECRET** environment variable
- **File upload validation** restricts to ADIF files only
- **Input sanitization** for search and form inputs

## Troubleshooting

### Common Issues

1. **Application won't start**: Check that all dependencies are installed
2. **ADIF import fails**: Verify file format and encoding (UTF-8 recommended)
3. **QSL cards not generating**: Ensure Pillow is installed correctly
4. **Search results wrong**: Clear browser cache and restart application

### Logs and Debugging

- **Application logs**: Check console output where gunicorn is running
- **Debug mode**: Set `FLASK_ENV=development` for detailed error messages
- **File permissions**: Ensure write access to application directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the developer documentation for technical details