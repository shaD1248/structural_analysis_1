from analyzer import Analyzer
from test_data_sets import test_data_sets
from visualizer import visualize

test_data_set = test_data_sets[5]
nodes = test_data_set['nodes'].list
elements = test_data_set['elements'].list
analysis = Analyzer(nodes, elements)
analysis.analyze()
visualize(elements, analysis, [[1, 0, 0], [0, 0, 1]])
