import os
import re
import xml.etree.ElementTree as ET

def sanitize_xml_content_manually(xml_content):
    """Manually sanitize special characters in the XML content."""
    xml_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_content)
    replacements = {
        '<?xml version="1.0" encoding="UTF-8">' : '<?xml version="1.0" encoding="UTF-8"?>'
    }

    for old, new in replacements.items():
        xml_content = xml_content.replace(old, new)

    return xml_content

def sanitize_xml_file(file_path):
    """Read, sanitize, and write the XML content back to the same file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        # Sanitize special characters manually
        sanitized_content = sanitize_xml_content_manually(xml_content)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(sanitized_content)
        
        print(f"Sanitized XML content written to {file_path}")
        check_format(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def sanitize_all_xml_files_in_place(input_dir):
    """Sanitize all XML files in the specified directory in place."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                sanitize_xml_file(file_path)

def check_format(file_path):
    """Sanitize special characters in the XML content."""
    # Create an ElementTree object from the XML content
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
            
        root = ET.fromstring(xml_content)
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        print(f"Problematic XML content in file: {file_path}")
        return None
    
# Example usage
input_dir = './'
sanitize_all_xml_files_in_place(input_dir)
