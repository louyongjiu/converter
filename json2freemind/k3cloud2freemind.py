import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


root_name='小K'


def json_to_freemind(json_data):
    root = ET.Element("map")
    root.set("version", "1.0.1")
    main_node = ET.SubElement(root, "node")
    main_node.set('TEXT', root_name)

    for action in json_data:
        if action['actionname'] == "UpdateControlStates":
            for param in action['params']:
                if param['key'] == "FH5CARDMAINSYSTEMMENUFLOWLAYOUT":
                    if 'ItemTipsContent' in param:
                        tips_node = ET.SubElement(main_node, "node")
                        tips_node.set("TEXT", "名词解释")
                        for item in param['ItemTipsContent']:
                            tip_node = ET.SubElement(tips_node, "node")
                            tip_node.set("TEXT", item["text"])
        elif action['actionname'] == "InvokeControlMethod":
            for param in action['params']:
                if param['key'] == "FH5CARDMAINSYSTEMMENUFLOWLAYOUT":
                    if isinstance(param['args'][0], dict) and 'children' in param['args'][0]:
                        children = param['args'][0]['children']
                        for child in children:
                            child_node = ET.SubElement(main_node, "node")
                            child_node.set("TEXT", child["title"])
                            for grandchild in child['children']:
                                grandchild_node = ET.SubElement(child_node, "node")
                                grandchild_node.set("TEXT", grandchild["text"])

    xml_str = ET.tostring(root, 'utf-8')
    pretty_xml_str = parseString(xml_str).toprettyxml(indent="  ")
    
    return pretty_xml_str


def create_freemind(json_filepath, output_filepath, max_depth):
    with open('json_data.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    # 使用示例
    freemind_content = json_to_freemind(json_data)
    print(freemind_content)

    # 保存到文件
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(freemind_content)

create_freemind('json_data.json', root_name+'.mm', 100)