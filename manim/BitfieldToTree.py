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

        depth = 4
        sum_reduction_values = CBT.create_cbt(tree_nodes, depth)

        tree = CBT.BinaryTree(depth, active_nodes = tree_nodes)
        g0 = VGroup(tree)

        cbt = CBT.BinaryTree(depth, node_data = sum_reduction_values)
        bitfield_row = cbt.rows[-1]
        for node in bitfield_row:
            node.remove(*node.get_lines())
        bitfield = VGroup(*bitfield_row)

        bitfield_range = cbt.get_bitfield_range_for_node(3)
        bitfield_node_3 = bitfield_range[0]

        zeros_t = Text(f'{len(bitfield_range) - 1} zero\'s = Depth - 2').scale(0.6)
        eq_t = MathTex('D = D_{max} - log_2(N + 1)').scale(0.8)

        tree_group = VGroup(g0, bitfield, eq_t, zeros_t).arrange(DOWN).move_to([0, 0, 0])

        bitfield_node_rect = SurroundingRectangle(VGroup(*bitfield_node_3), color=YELLOW, buff=0)
        depth_example_rect = SurroundingRectangle(VGroup(*bitfield_range[1:]), color=GREEN, buff=0)

        tree_node_rect_start = SurroundingRectangle(VGroup(*tree.get_node(12)), color=YELLOW, buff=0)
        tree_node_rect_final = SurroundingRectangle(VGroup(*tree.get_node(3)), color=YELLOW, buff=0)

        leaf_ints = sorted(get_leaf_nodes(tree_nodes))
        leaves = [BackgroundRectangle(VGroup(*tree.get_node(x)), color=RED, fill_opacity=0.5) for x in leaf_ints]
        bitfield_nodes = [BackgroundRectangle(VGroup(*cbt.bitfield_node(x)), color=RED, fill_opacity=0.5) for x in leaf_ints]

        leaf_node_highlights = [None]*(len(leaves)+len(bitfield_nodes))
        leaf_node_highlights[::2] = bitfield_nodes
        leaf_node_highlights[1::2] = leaves     

        leaf_node_bgs = VGroup(*leaf_node_highlights)

        self.play(Create(bitfield))

        self.wait(3)

        self.play(Create(g0))

        self.wait(3)

        self.play(Create(leaf_node_bgs), run_time = 4)

        self.wait(2)

        self.play(Create(bitfield_node_rect))

        self.wait(2)

        self.play(Create(eq_t))

        self.wait(2)
        self.play(Create(tree_node_rect_start))

        self.wait(1)

        self.play(Create(depth_example_rect))
        self.play(Create(zeros_t))

        self.wait(1)

        self.play(Transform(tree_node_rect_start, tree_node_rect_final))

        self.wait(2)

