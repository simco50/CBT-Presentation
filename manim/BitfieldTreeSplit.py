from manim import *
import Libraries.LEB as LEB
import Libraries.CBT as CBT
import Libraries.Utilities as Utils

def get_leaf_nodes(nodes):
    leaf_nodes = []
    for node in nodes:
        if node << 1 not in nodes:
            leaf_nodes.append(node)
    return leaf_nodes      

class Main(Scene):
    def construct(self):

        tree_nodes = [
            1,
            2, 3,
            4, 5,
            8, 9
        ]

        node_to_split = 3

        depth = 4
        sum_reduction_values = CBT.create_cbt(tree_nodes, depth)

        tree = CBT.BinaryTree(depth, active_nodes = tree_nodes)
        g0 = VGroup(tree)

        cbt = CBT.BinaryTree(depth, node_data = sum_reduction_values)
        bitfield_row = cbt.rows[-1]
        for node in bitfield_row:
            node.remove(*node.get_lines())
        bitfield = VGroup(*bitfield_row)

        tree_group = VGroup(g0, bitfield).arrange(DOWN).move_to([0, 0, 0])

        self.add(tree_group)

        self.wait(2)
