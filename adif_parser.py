import re
import datetime
import logging

def parse_adif_file(file_path):
    """Parse ADIF file and return structured data"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract header and records
    header_data = extract_header_info(content)
    contacts = parse_adif_records(content)
    
    # Clean and standardize contacts
    cleaned_contacts = [clean_contact_data(contact) for contact in contacts]
    
    result = {
        'header': header_data,
        'contacts': cleaned_contacts
    }
    
    logging.info(f"Parsed {len(cleaned_contacts)} contacts from ADIF file")
    return result

def extract_header_info(content):
    """Extract header information from ADIF content"""
    header = {
        'created_timestamp': datetime.datetime.now().isoformat(),
        'last_updated': datetime.datetime.now().isoformat(),
        'adif_version': '3.1.4'
    }
    
    # Look for common header fields
    header_patterns = {
        'station_callsign': r'<station_callsign:\d+>([^<]+)',
        'operator': r'<operator:\d+>([^<]+)',
        'adif_ver': r'<adif_ver:\d+>([^<]+)'
    }
    
    for field, pattern in header_patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            if field == 'adif_ver':
                header['adif_version'] = match.group(1).strip()
            else:
                header[field] = match.group(1).strip().upper()
    
    return header

def parse_adif_records(content):
    """Parse individual ADIF records"""
    contacts = []
    
    # Split by <eor> (end of record)
    records = re.split(r'<eor>', content, flags=re.IGNORECASE)
    
    for record in records:
        if not record.strip():
            continue
        
        contact = parse_single_record(record)
        if contact:
            contacts.append(contact)
    
    return contacts

def parse_single_record(record):
    """Parse a single ADIF record"""
    contact = {}
    
    # Pattern to match ADIF fields: <field:length>value
    pattern = r'<([^:>]+):(\d+)(?::[^>]*)?>([^<]*)'
    matches = re.findall(pattern, record, re.IGNORECASE)
    
    for field_name, length, value in matches:
        field_name = field_name.lower().strip()
        length = int(length)
        value = value[:length].strip() if value else ''
        
        if value:
            contact[field_name] = value
    
    return contact if contact else None

def clean_contact_data(contact):
    """Clean and standardize contact data"""
    cleaned = {}
    
    # Map common ADIF fields
    field_mapping = {
        'call': 'call',
        'qso_date': 'qso_date',
        'time_on': 'time_on',
        'time_off': 'time_off',
        'band': 'band',
        'freq': 'freq',
        'mode': 'mode',
        'submode': 'submode',
        'rst_sent': 'rst_sent',
        'rst_rcvd': 'rst_rcvd',
        'gridsquare': 'gridsquare',
        'country': 'country',
        'state': 'state',
        'county': 'county',
        'station_callsign': 'station_callsign',
        'operator': 'operator',
        'qsl_sent': 'qsl_sent',
        'qsl_rcvd': 'qsl_rcvd',
        'qsl_sent_date': 'qsl_sent_date',
        'qsl_rcvd_date': 'qsl_rcvd_date',
        'contest_id': 'contest_id',
        'srx': 'srx',
        'stx': 'stx',
        'comment': 'comment',
        'comments': 'comments',
        'notes': 'notes',
        'remarks': 'remarks'
    }
    
    # Process mapped fields
    for adif_field, standard_field in field_mapping.items():
        if adif_field in contact:
            value = contact[adif_field].strip()
            if value:
                cleaned[standard_field] = clean_field_value(standard_field, value)
    
    # Store additional fields
    additional_fields = {}
    for field, value in contact.items():
        if field not in field_mapping and value.strip():
            additional_fields[field] = value.strip()
    
    if additional_fields:
        cleaned['additional_fields'] = additional_fields
    
    return cleaned

def clean_field_value(field_name, value):
    """Clean individual field values"""
    value = value.strip()
    
    if field_name == 'call':
        return clean_callsign(value)
    elif field_name in ['qso_date', 'qsl_sent_date', 'qsl_rcvd_date']:
        return clean_date(value)
    elif field_name in ['time_on', 'time_off']:
        return clean_time(value)
    elif field_name == 'band':
        return clean_band(value)
    elif field_name in ['mode', 'submode']:
        return clean_mode(value)
    elif field_name == 'gridsquare':
        return clean_gridsquare(value)
    elif field_name == 'freq':
        return clean_frequency(value)
    elif field_name in ['country', 'state', 'county']:
        return clean_location(value)
    else:
        return value

def clean_callsign(callsign):
    """Clean and standardize callsign"""
    # Remove invalid characters and convert to uppercase
    callsign = re.sub(r'[^A-Z0-9/]', '', callsign.upper())
    return callsign

def clean_date(date_str):
    """Clean and standardize date format to YYYY-MM-DD"""
    date_str = re.sub(r'[^\d/\-]', '', date_str)
    
    # Try different date formats
    formats = [
        '%Y%m%d',     # YYYYMMDD
        '%Y-%m-%d',   # YYYY-MM-DD
        '%m/%d/%Y',   # MM/DD/YYYY
        '%d/%m/%Y',   # DD/MM/YYYY
        '%m-%d-%Y',   # MM-DD-YYYY
        '%d-%m-%Y'    # DD-MM-YYYY
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return date_str  # Return original if no format matches

def clean_time(time_str):
    """Clean and standardize time format to HH:MM:SS"""
    time_str = re.sub(r'[^\d:]', '', time_str)
    
    # Try different time formats
    formats = [
        '%H%M%S',   # HHMMSS
        '%H:%M:%S', # HH:MM:SS
        '%H%M',     # HHMM
        '%H:%M'     # HH:MM
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(time_str, fmt)
            return dt.strftime('%H:%M:%S')
        except ValueError:
            continue
    
    return time_str  # Return original if no format matches

def clean_band(band):
    """Clean and standardize band designation"""
    band = band.upper().strip()
    
    # Standardize common band formats
    band_mapping = {
        '160': '160M',
        '80': '80M',
        '40': '40M',
        '30': '30M',
        '20': '20M',
        '17': '17M',
        '15': '15M',
        '12': '12M',
        '10': '10M',
        '6': '6M',
        '2': '2M',
        '70CM': '70CM',
        '23CM': '23CM'
    }
    
    # Remove 'M' suffix temporarily for mapping
    band_clean = band.replace('M', '')
    
    if band_clean in band_mapping:
        return band_mapping[band_clean]
    
    # If not in mapping, add 'M' if it's missing and looks like a band
    if re.match(r'^\d+$', band_clean):
        return band_clean + 'M'
    
    return band

def clean_mode(mode):
    """Clean and standardize mode"""
    mode = mode.upper().strip()
    
    # Standardize common modes
    mode_mapping = {
        'CW': 'CW',
        'SSB': 'SSB',
        'USB': 'USB',
        'LSB': 'LSB',
        'AM': 'AM',
        'FM': 'FM',
        'FT8': 'FT8',
        'FT4': 'FT4',
        'JS8': 'JS8',
        'PSK31': 'PSK31',
        'RTTY': 'RTTY',
        'DIGITAL': 'DIGITAL',
        'DATA': 'DATA'
    }
    
    return mode_mapping.get(mode, mode)

def clean_gridsquare(gridsquare):
    """Clean and validate gridsquare"""
    gridsquare = gridsquare.upper().strip()
    
    # Validate gridsquare format (4 or 6 characters)
    if re.match(r'^[A-R]{2}[0-9]{2}([A-X]{2})?$', gridsquare):
        return gridsquare
    
    return gridsquare  # Return as-is if invalid

def clean_frequency(freq):
    """Clean frequency value"""
    # Remove non-numeric characters except decimal point
    freq = re.sub(r'[^\d.]', '', freq)
    
    try:
        float(freq)
        return freq
    except ValueError:
        return freq

def clean_location(location):
    """Clean location (country, state, county)"""
    # Proper case formatting
    return location.strip().title()

def contacts_to_adif(contacts, header):
    """Convert contacts back to ADIF format"""
    adif_lines = []
    
    # Add header
    adif_lines.append(f"<ADIF_VER:{len(header.get('adif_version', '3.1.4'))}>{header.get('adif_version', '3.1.4')}")
    adif_lines.append(f"<PROGRAMID:10>Hamlogblog")
    adif_lines.append(f"<STATION_CALLSIGN:{len(header.get('station_callsign', ''))}>{header.get('station_callsign', '')}")
    adif_lines.append("<EOH>")
    adif_lines.append("")
    
    # Add contacts
    for contact in contacts:
        contact_lines = []
        
        # Standard fields
        for field, value in contact.items():
            if field == 'additional_fields':
                continue
            
            if value:
                value_str = str(value)
                contact_lines.append(f"<{field.upper()}:{len(value_str)}>{value_str}")
        
        # Additional fields
        if 'additional_fields' in contact:
            for field, value in contact['additional_fields'].items():
                if value:
                    value_str = str(value)
                    contact_lines.append(f"<{field.upper()}:{len(value_str)}>{value_str}")
        
        contact_lines.append("<EOR>")
        adif_lines.extend(contact_lines)
        adif_lines.append("")
    
    return '\n'.join(adif_lines)
