## canvas2svg

Obsidian Canvas to SVG images converter.

The program is designed to convert Obsidian Canvas files into SVG images. It processes text files in JSON format, which contain information about the positioning and connections of elements on the canvas.

When launched, the program takes a file with the .canvas extension as input. If the file exists, it reads and analyzes its structure. First, the boundaries of the entire canvas are determined based on the coordinates of all elements to establish the dimensions of the final SVG image with small margins around the edges.

The program processes two main types of elements: groups and cards. Groups are displayed as rectangles with rounded corners and a semi-transparent fill, accompanied by text labels. Text cards are visualized as colored rectangles with rounded corners containing text inside. Element colors are determined from a predefined palette based on their color codes.

Connections between elements (edges) are displayed as curved lines with arrowhead markers at the end. Horizontally oriented lines use vertical curvature, while vertically oriented lines use horizontal curvature. The bend magnitude is dynamically adapted based on the line length.

The resulting SVG image is saved into a file with the same name as the input file but with the .svg extension. The output file contains readable, indented markup and should display correctly in any SVG viewer, preserving the structure and relationships of the original Obsidian canvas.

Samples:

Python Multithreading Canvas:

![Multithreading Multiprocessing Python Roadmap](https://raw.githubusercontent.com/amaargiru/canvas2svg/refs/heads/main/Samples/Drawings%20(for%20readme)/pyroadmap.com-multithreading-multiprocessing-canvas.png)

SVG:

![Multithreading Multiprocessing Python Roadmap](https://raw.githubusercontent.com/amaargiru/canvas2svg/refs/heads/main/Samples/Drawings%20(for%20readme)/pyroadmap.com-multithreading-multiprocessing-svg.png)

Python Data Science Canvas:

![Data Science Python Roadmap](https://raw.githubusercontent.com/amaargiru/canvas2svg/refs/heads/main/Samples/Drawings%20(for%20readme)/pyroadmap.com-data-science-canvas.png)

SVG:

![Data Science Python Roadmap](https://raw.githubusercontent.com/amaargiru/canvas2svg/refs/heads/main/Samples/Drawings%20(for%20readme)/pyroadmap.com-data-science-svg.png)