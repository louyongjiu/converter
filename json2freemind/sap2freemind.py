import json
import xml.etree.ElementTree as ET

def parse_json_to_freemind(json_node, current_depth=0, max_depth=2):
    """
    Recursively convert JSON node to FreeMind XML node, up to a certain depth.
    """
    node_element = ET.Element('node')
    node_element.set('TEXT', json_node['text'])
    
    # Only process children if the current depth is less than the maximum depth
    if 'children' in json_node and current_depth < max_depth:
        for child in json_node['children']:
            child_element = parse_json_to_freemind(child, current_depth + 1, max_depth)
            node_element.append(child_element)
    
    return node_element

def create_freemind(json_filepath, output_filepath, max_depth):
    """
    Load JSON data from a file and create a FreeMind chart, saving the output to a file.
    """
    with open(json_filepath, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Create a FreeMind mind map from JSON data, up to a certain depth.
    freemind_root = ET.Element('map')
    freemind_root.set('version', '1.0.1')
    main_node = parse_json_to_freemind(json_data, max_depth=max_depth)  # Start counting depth from 1
    freemind_root.append(main_node)
    
    # Save the FreeMind XML element to a file.
    tree = ET.ElementTree(freemind_root)
    tree.write(output_filepath, encoding='utf-8', xml_declaration=True)

# 使用函数开始转换过程，指定最大层数为3
create_freemind('json_data.json', 'freemind_diagram.mm', 100)
