import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

# Embedded XML template
xml_template = '''<?xml version='1.0' encoding='UTF-8'?><a:feed xmlns="http://marketplace.xboxlive.com/resource/product/v1" xmlns:a="http://www.w3.org/2005/Atom"></a:feed>'''
def add_entry_to_xml(file_path, new_entry_data):
    # Parse the existing XML file
    root = ET.fromstring(xml_template)

    # Define namespaces
    namespaces = {'a': 'http://www.w3.org/2005/Atom', '': 'http://marketplace.xboxlive.com/resource/product/v1'}

    # Create a new entry element
    entry = ET.Element('{http://www.w3.org/2005/Atom}entry', attrib={'itemNum': '1'})

    # Add sub-elements to the new entry
    full_title = ET.SubElement(entry, 'fullTitle')
    full_title.text = new_entry_data['title']
    
    full_description = ET.SubElement(entry, 'fullDescription')
    full_description.text = new_entry_data['description']
    
    release_date = ET.SubElement(entry, 'globalOriginalReleaseDate')
    release_date.text = new_entry_data['release_date']
    
    rating_id = ET.SubElement(entry, 'ratingId')
    rating_id.text = new_entry_data['rating_id']

    rating_descriptors = ET.SubElement(entry, 'ratingDescriptors')
    for descriptor in new_entry_data['rating_descriptors']:
        rating_descriptor = ET.SubElement(rating_descriptors, 'ratingDescriptor', attrib={'level': '1.0000'})
        rating_descriptor.text = descriptor

    developer_name = ET.SubElement(entry, 'developerName')
    developer_name.text = new_entry_data['developer']

    publisher_name = ET.SubElement(entry, 'publisherName')
    publisher_name.text = new_entry_data['publisher']

    game_capabilities = ET.SubElement(entry, 'gameCapabilities')
    for capability in new_entry_data['game_capabilities']:
        capability_elem = ET.SubElement(game_capabilities, capability)
        capability_elem.text = '1'

    images = ET.SubElement(entry, 'images')
    for image_url in new_entry_data['image_urls']:
        image = ET.SubElement(images, 'image')
        file_url = ET.SubElement(image, 'fileUrl')
        file_url.text = image_url
        
    slideshows = ET.SubElement(entry, 'slideShows')
    for image_url in new_entry_data['slideshows']:
        slideshow = ET.SubElement(slideshows, 'slideshow')
        image = ET.SubElement(slideshow, 'image')
        file_url = ET.SubElement(image, 'fileUrl')
        file_url.text = image_url

    # Append the new entry to the root element
    root.append(entry)
    
    ET.register_namespace('a', 'http://www.w3.org/2005/Atom')
    ET.register_namespace('', 'http://marketplace.xboxlive.com/resource/product/v1')
    
    tree = ET.ElementTree(root)
    # Save the updated XML back to the file
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)
    
    with open(file_path, 'r', encoding='UTF-8') as file:
        xml_str = file.read()
    
    dom = minidom.parseString(xml_str)
    formatted_xml_str = dom.toprettyxml(indent="  ")
    
    # Write the formatted XML back to the file
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(formatted_xml_str)

if __name__ == '__main__':
    
    file_name = input("Enter the new file name (without .xml extension): ").lower()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'{file_name}'))
    os.makedirs(path, exist_ok=True)
    
    # Create the output folder path
    output_folder = os.path.join(path, f'{file_name}.xml')
    
    title = input("Enter the new title: ")
    description = input("Enter the new description: ")
    release_date = input("Enter the new release date (YYYY-MM-DD): ")
    developer = input("Enter the new developer name: ")
    publisher = input("Enter the new publisher name: ")
    xboxlive = int(input("Has Xbox Live? ( 1 = Yes | 0 = No): "))
    systemlink = int(input("Has SystemLink? ( 1 = Yes | 0 = No): "))
    coop = int(input("Has Coop? ( 1 = Yes | 0 = No): "))
    banner = input("Game file icon name? (boxartlg): ")
    gallery = int(input("How many slideshow images?: "))
    
    capabilities = []
    images = []
    slidshows = []
    if xboxlive == 1:
        capabilities.append("onlineMultiplayerMin")
    
    if systemlink == 1:
        capabilities.append("offlineSystemLinkMin")
        
    if coop == 1:
        capabilities.append("onlineCoopPlayersMin")
        
    
    for i in range(gallery):
        slidshows.append(f"https://raw.githubusercontent.com/wildmaster84/restored-media/main/{file_name.upper()}/screenlg{i + 1}.jpg")
    
    images = [
        f"https://raw.githubusercontent.com/wildmaster84/restored-media/main/{file_name.upper()}/tile.png",
        f"https://raw.githubusercontent.com/wildmaster84/restored-media/main/{file_name.upper()}/background.jpg",
        f"https://raw.githubusercontent.com/wildmaster84/restored-media/main/{file_name.upper()}/{banner}.jpg",
        f"https://raw.githubusercontent.com/wildmaster84/restored-media/main/{file_name.upper()}/banner.png"
    ]
    
    new_entry_data = {
        'title': title,
        'description': description,
        'release_date': f'{release_date}T00:00:00',
        'rating_id': '30',
        'rating_descriptors': ['2', '12', '26', '31'],
        'developer': developer,
        'publisher': publisher,
        'game_capabilities': capabilities,
        'image_urls': images,
        'slideshows': slidshows
    }
    
    add_entry_to_xml(output_folder, new_entry_data)
