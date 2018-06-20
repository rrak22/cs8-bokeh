import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

from graph import *

graph_data = Graph()
graph_data.debug_create_test_data()
print(graph_data.vertexes)

N = len(graph_data.vertexes)
node_indices = list(range(N))

print('Node indices: ', node_indices)

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, 500), y_range=(0, 500),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Oval(height=25, width=25, fill_color='color')

# this is drawing edges from start to end

graph.edge_renderer.data_source.data = dict(start=[], end=[])

# take value of edges and convert to 0-base index

for vertex in graph_data.vertexes:
    for edge in vertex.edges:
        graph.edge_renderer.data_source.data['start'].append(int(edge.origin.value[-1]) - 1)
        graph.edge_renderer.data_source.data['end'].append(int(edge.destination.value[-1]) - 1)

print(graph.edge_renderer.data_source.data)

### start of layout code
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)
