import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, Label, LabelSet, ColumnDataSource
from bokeh.palettes import Spectral8

from graph import *

WIDTH = 500
HEIGHT = 500
CIRCLE_SIZE = 30

graph_data = Graph()
graph_data.debug_create_test_data()
graph_data.bfs(graph_data.vertexes[0])
# print(graph_data.vertexes)

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Circle(size=CIRCLE_SIZE, fill_color='color')

# this is drawing edges from start to end

graph.edge_renderer.data_source.data = dict(start=[], end=[])

# take value of edges and convert to 0-base index

for vertex in graph_data.vertexes:
    for edge in vertex.edges:
        graph.edge_renderer.data_source.data['start'].append(int(edge.origin.value[-1]) - 1)
        graph.edge_renderer.data_source.data['end'].append(int(edge.destination.value[-1]) - 1)

### start of layout code
x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]
name = [v.value for v in graph_data.vertexes]

### create labels
source = ColumnDataSource(data=dict(x=x, y=y, name=name))
labels = LabelSet(x='x', y='y', text='name', level='overlay', source=source, render_mode='canvas', text_align='center', text_baseline='middle')

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)
plot.add_layout(labels) # remember to draw labels after circles


output_file('graph.html')
show(plot)
