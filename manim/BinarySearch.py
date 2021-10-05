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
            4, 5, 6,
            8, 9, 12, 13
        ]

        leaf_index = 3
        depth = 4
        cbt_values = CBT.create_cbt(tree_nodes, depth)
        cbt = CBT.BinaryTree(depth, node_data = cbt_values).move_to([0, 0, 0])

        current_leaf_index = 0
        bitfield_nodes = cbt.rows[-1]
        leaf_node_numbers = []
        for bitfield_node in bitfield_nodes:
            if bitfield_node.get_value() > 0:
                leaf_node_numbers.append(Text(f'{current_leaf_index}', color=GREEN).scale(0.6).move_to(bitfield_node, aligned_edge=DOWN).shift([0, -0.5, 0]))
                current_leaf_index += 1
        leaf_node_indices = VGroup(*leaf_node_numbers)


        self.add(cbt)
        self.add(leaf_node_indices)

