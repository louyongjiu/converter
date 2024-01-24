import json
import re

def convert_to_id(text):
    """
    Convert a given text to a valid Mermaid ID by replacing special characters with underscores.
    """
    text = re.sub(r'[^\w]', '_', text)
    text = re.sub(r'_+', '_', text).strip('_')
    return text

def parse_json_to_mermaid(item, parent_id=None, current_depth=0, max_depth=2, nodes=None, edges=None):
    """
    Parse the JSON data to create nodes and edges for a Mermaid flowchart.
    """
    if nodes is None:
        nodes = []
    if edges is None:
        edges = []

    indent = '    ' * (current_depth + 1)
    current_id = convert_to_id(item['t'])  # 清理标题以形成有效的 ID
    current_label = item['t'].replace('"', '').replace('\'', '')  # 使用原始标题
    nodes.append(f'{indent}{current_id}["{current_label}"]')  # 定义节点
    if parent_id:
        edges.append(f'{indent}{parent_id} --> {current_id}')
    # 限制深度为2层，depth从0开始计数，所以0和1代表两层
    if 'c' in item and current_depth < max_depth:
        for child in item['c']:
            parse_json_to_mermaid(child, current_id, current_depth + 1, max_depth, nodes, edges)
    return nodes, edges

def create_mermaid_chart(json_filepath, output_filepath, max_depth):
    """
    Load JSON data from a file and create a Mermaid chart, saving the output to a file.
    """
    with open(json_filepath, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    nodes, edges = parse_json_to_mermaid(json_data, max_depth=max_depth)
    mermaid_output = 'graph TD\n' + '\n'.join(nodes) + '\n\n' + '\n'.join(edges)

    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(mermaid_output)

# 使用函数开始转换过程
create_mermaid_chart('json_data.json', 'mermaid_diagram.txt', 2)
