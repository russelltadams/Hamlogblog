# Hamlogblog - Amateur Radio Log & Blog System

## Overview

Hamlogblog is a Flask-based web application designed for amateur radio operators to manage their station logs and maintain a blog about their radio activities. The system provides ADIF file parsing, contact management, QSL card generation, and a simple blog platform, all integrated into a single amateur radio-focused website.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### July 12, 2025
- **Configuration System**: Implemented complete configuration management with config.json
- **Station Customization**: Added configurable station info (call sign, QTH, grid square, operator name)
- **Site Personalization**: Site title, footer, and admin login now use configurable call sign
- **QSL Customization**: Added configurable QSL card settings (message, equipment, antenna, power)
- **Admin Interface**: Created user-friendly configuration management page accessible via Admin Panel
- **Template Integration**: Updated all templates to use configuration values for consistent branding
- Fixed search function bug where contact details showed wrong contact information
- Created comprehensive README.md with deployment, admin, and developer documentation

### July 13, 2025
- **Contact Sorting**: Fixed all contact displays to sort by newest first (homepage, contact list, search results)
- **Configuration Integration**: Contact pagination and recent contacts now use configurable limits
- **RST Display**: Enhanced RST column to properly handle digital modes and missing data
- **Digital Mode Detection**: Expanded digital mode list for better RST handling across all templates

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **File-based Storage**: JSON files for data persistence (no database required)
- **Session Management**: Flask sessions for admin authentication
- **File Processing**: Custom ADIF parser for amateur radio log files

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome for UI icons
- **Responsive Design**: Mobile-friendly interface using Bootstrap grid system

### Authentication System
- **Simple Admin Auth**: Hardcoded credentials (KM6KFX/happyham)
- **Session-based**: Flask sessions to maintain login state
- **Decorator Protection**: `@admin_required` decorator for protected routes

## Key Components

### 1. ADIF Parser (`adif_parser.py`)
- **Purpose**: Parse Amateur Data Interchange Format (ADIF) files
- **Features**: Extract contact records and header information
- **Data Cleaning**: Standardize and validate contact data
- **Output**: Structured JSON format for storage

### 2. Contact Management (`models.py`)
- **Station Log**: JSON-based storage for all contacts
- **Blog Posts**: Separate JSON storage for blog content
- **Data Operations**: Load, save, and merge contact records
- **Backup System**: Automatic backup creation before data updates

### 3. QSL Card Generator (`qsl_generator.py`)
- **Image Generation**: PIL-based QSL card creation
- **Template System**: Standard QSL card format with contact details
- **Font Handling**: Graceful fallback for font loading
- **Export Format**: PNG images for download

### 4. Web Interface (`routes.py`)
- **Public Pages**: Home, blog, contact log viewing, search
- **Admin Pages**: File upload, blog management, admin panel
- **Contact Details**: Individual contact view with QSL generation
- **Search Functionality**: Multi-field contact search

### 5. Blog System
- **CRUD Operations**: Create, read, update, delete blog posts
- **Admin Management**: Protected blog creation and editing
- **Public Display**: Blog listing and individual post views
- **Content Formatting**: Basic text formatting with line breaks

## Data Flow

### Contact Import Process
1. Admin uploads ADIF file through web interface
2. ADIF parser extracts contact records and metadata
3. Data validation and cleaning applied
4. Contacts merged with existing station log
5. Updated log saved to JSON file
6. Statistics recalculated and displayed

### Blog Publishing Process
1. Admin creates/edits blog post through web interface
2. Post content validated and stored in JSON
3. Post appears on public blog pages immediately
4. Admin can edit or delete posts as needed

### QSL Card Generation
1. User selects contact from log view
2. Contact details passed to QSL generator
3. PIL creates formatted QSL card image
4. Generated image sent as download to user

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Pillow (PIL)**: Image generation for QSL cards
- **Werkzeug**: WSGI utilities and file handling

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icon library
- **DejaVu Fonts**: System fonts for QSL card generation

### Browser Dependencies
- Modern browser with JavaScript enabled
- Support for HTML5 file uploads
- CSS Grid and Flexbox support

## Deployment Strategy

### File Structure
- **Static Files**: CSS and potential future assets in `/static`
- **Templates**: Jinja2 templates in `/templates`
- **Data Storage**: JSON files in root directory
- **Uploads**: Temporary ADIF files in `/uploads`

### Environment Configuration
- **Session Secret**: Configurable via environment variable
- **Upload Limits**: 16MB maximum file size
- **Development Mode**: Debug enabled for development

### Scaling Considerations
- **File-based Storage**: Suitable for single-user amateur radio logs
- **No Database**: Simplifies deployment and maintenance
- **JSON Performance**: Efficient for typical amateur radio log sizes
- **Future Migration**: Data structure supports eventual database migration

### Security Measures
- **File Upload Validation**: ADIF file type restrictions
- **Session Management**: Secure session handling
- **Input Sanitization**: Basic protection against malicious input
- **Admin Authentication**: Simple but effective access control

The application is designed as a self-contained amateur radio logging solution that can be easily deployed without complex database setup, making it ideal for personal use by amateur radio operators who want to share their activities online.