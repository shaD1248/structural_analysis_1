from analyzer import Analyzer
from test_data_sets import test_data_sets

test_data_set = test_data_sets[4]
analysis = Analyzer(test_data_set['nodes'].list, test_data_set['elements'].list)
analysis.analyze()

