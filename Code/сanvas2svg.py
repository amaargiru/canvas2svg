import json
import os
import sys
import xml.etree.ElementTree as XmlTree
from pathlib import Path
from xml.dom import minidom


def main():
    if len(sys.argv) < 2:
        print("Usage: python сanvas2svg.py input.canvas")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = Path(input_file).stem + '.svg'

    if os.path.exists(input_file):  # If file exists in app directory
        with open(input_file, 'r') as f:
            data = json.load(f)
    else:
        print(f"File {input_file} doesn't exist in app directory")
        sys.exit(1)

    nodes = data['nodes']
    edges = data['edges']

    min_x = min(node['x'] for node in nodes)
    min_y = min(node['y'] for node in nodes)
    max_x = max(node['x'] + node['width'] for node in nodes)
    max_y = max(node['y'] + node['height'] for node in nodes)

    padding = 20
    dx = -min_x + padding
    dy = -min_y + padding

    svg_width = max_x - min_x + 2 * padding
    svg_height = max_y - min_y + 2 * padding

    svg = XmlTree.Element('svg', xmlns="http://www.w3.org/2000/svg", width=str(svg_width), height=str(svg_height))

    # Arrow
    defs = XmlTree.SubElement(svg, 'defs')
    marker = XmlTree.SubElement(defs, 'marker',
                                id='arrow',
                                viewBox='0 0 12 12',
                                refX='10',
                                refY='6',
                                markerWidth='8',
                                markerHeight='8',
                                orient='auto')
    XmlTree.SubElement(marker, 'path',
                       d='M0,0 L12,6 L0,12 Z',
                       fill='context-stroke')

    color_map = {
        "0": '#7e7e7e',
        "1": '#aa363d',
        "2": '#a56c3a',
        "3": '#aba960',
        "4": '#199e5c',
        "5": '#249391',
        "6": '#795fac',
        "default": "#444444"
    }

    def get_color(color_code):
        return color_map.get(color_code, color_map['default'])

    # Draw groups
    for node in [node for node in nodes if node['type'] == 'group']:
        x = node['x'] + dx
        y = node['y'] + dy
        width = node['width']
        height = node['height']

        XmlTree.SubElement(svg, 'rect',
                           x=str(x), y=str(y),
                           width=str(width), height=str(height),
                           rx='8', ry='8',
                           fill='#EEEEEE',
                           stroke='#888888',
                           **{'fill-opacity': '0.25',
                              'stroke-width': '1'}
                           )

        if 'label' in node:
            text_elem = XmlTree.SubElement(svg, 'text',
                                           x=str(x),
                                           y=str(y - 20),
                                           **{'text-anchor': 'left',
                                         'dominant-baseline': 'hanging',
                                         'font-family': 'Arial',
                                         'font-size': '18'})
            text_elem.text = node['label']

    # Draw cards
    for node in [node for node in nodes if node['type'] == 'text']:
        x = node['x'] + dx
        y = node['y'] + dy
        width = node['width']
        height = node['height']
        color = get_color(node.get('color', 'default'))

        XmlTree.SubElement(svg, 'rect',
                           x=str(x), y=str(y),
                           width=str(width), height=str(height),
                           rx='8', ry='8',
                           fill=color, stroke=color,
                           **{'fill-opacity': '0.25',
                              'stroke-width': '2'})

        text_elem = XmlTree.SubElement(svg, 'text',
                                       x=str(x + width / 2),
                                       y=str(y + height / 2),
                                       **{'text-anchor': 'middle',
                                     'dominant-baseline': 'middle',
                                     'font-family': 'Arial',
                                     'font-size': '18'})
        text_elem.text = node.get('text', '')

    # Draw edges
    for edge in edges:
        from_node = next(n for n in nodes if n['id'] == edge['fromNode'])
        to_node = next(n for n in nodes if n['id'] == edge['toNode'])

        start_x, start_y = get_side_coordinates(from_node, edge['fromSide'], dx, dy)
        end_x, end_y = get_side_coordinates(to_node, edge['toSide'], dx, dy)

        color = get_color(edge.get('color', 'default'))

        XmlTree.SubElement(svg, 'path',
                           d=f"M {start_x} {start_y} L {end_x} {end_y}",
                           stroke=color,
                           fill='none',
                           **{'marker-end': 'url(#arrow)',
                              'stroke-width': '2'})

    # Save SVG
    rough_xml = XmlTree.tostring(svg, 'utf-8')
    parsed = minidom.parseString(rough_xml)
    pretty_xml = parsed.toprettyxml(indent='  ')

    with open(output_file, 'w') as f:
        f.write(pretty_xml)


def get_side_coordinates(node, side, dx, dy):
    x = node['x'] + dx
    y = node['y'] + dy
    w, h = node['width'], node['height']

    if side == 'top':
        return x + w / 2, y
    elif side == 'bottom':
        return x + w / 2, y + h
    elif side == 'left':
        return x, y + h / 2
    elif side == 'right':
        return x + w, y + h / 2
    else:
        return x + w / 2, y + h / 2


if __name__ == "__main__":
    main()
