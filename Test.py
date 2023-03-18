import unittest
from CSP import *


class GraphColoringCSPTestCase(unittest.TestCase):
    def test1_constraint_satisfied(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        current_assignment = {'1': 0, '2': 1, '3': 2}
        csp_instance = GraphColoringCSP(input_graph, set(current_assignment.values()))
        result = csp_instance.constraint_satisfied('3', 2, current_assignment)
        self.assertEqual(result, True)

    def test2_constraint_satisfied(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        current_assignment = {'1': 0, '2': 1}
        csp_instance = GraphColoringCSP(input_graph, set(current_assignment.values()))
        result = csp_instance.constraint_satisfied('3', 1, current_assignment)
        self.assertEqual(result, False)

    def test3_select_unassigned_variable(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        csp_instance = GraphColoringCSP(input_graph, {0, 1})
        current_assignment = {}
        result = csp_instance.select_unassigned_variable(current_assignment)
        self.assertEqual(result, '2')

    def test4_order_domain_values(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        csp_instance = GraphColoringCSP(input_graph, {0, 1, 2})
        current_assignment = {}
        vertex = '1'
        result = csp_instance.order_domain_values(vertex, current_assignment)
        self.assertEqual(result, [0, 1, 2])

    def test5_revise(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        csp_instance = GraphColoringCSP(input_graph, {0, 1, 2})
        vertex1 = '1'
        vertex2 = '2'
        result = csp_instance.revise(vertex1, vertex2)
        self.assertEqual(result, False)

    def test6_ac3(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        csp_instance = GraphColoringCSP(input_graph, {0, 1, 2})
        result = csp_instance.ac3()
        self.assertEqual(result, True)

    def test7_backtracking_search(self):
        input_graph = {'1': ['2'], '2': ['1', '3'], '3': ['2']}
        csp_instance = GraphColoringCSP(input_graph, {0, 1})
        result = csp_instance.backtracking_search()
        self.assertIsNotNone(result)

    def test8_read_graph(self):
        file_path = "test1.txt"
        result = read_graph(file_path)
        self.assertIsInstance(result, tuple)

if __name__ == '__main__':
    unittest.main()
