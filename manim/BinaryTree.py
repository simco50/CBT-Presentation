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

class PerfectTree(Scene):
    def construct(self):
        depth = 4
        tree_nodes = [x for x in range(1, 1 << depth)]
        tree = CBT.BinaryTree(depth, active_nodes = tree_nodes)

        sum_reduction_values = CBT.create_cbt(tree_nodes, depth)
        cbt = CBT.BinaryTree(depth, node_data = sum_reduction_values)
        for node in cbt.get_nodes():
            if node:
                node.get_text().set_opacity(0)

        row_texts = []
        for row in cbt.get_rows():
            row_texts.append(VGroup(*[x[0] for x in row]))

        VGroup(tree, cbt).arrange(RIGHT, buff=1.5).move_to([0, 0, 0])

        bitfield_rect = SurroundingRectangle(VGroup(*cbt.get_node_row(depth - 1)), color=BLUE)
        bitfield_text = Text('Bitfield', color=BLUE).scale(0.6).next_to(bitfield_rect, direction=DOWN)

        sum_reduction_rect = SurroundingRectangle(VGroup(* cbt.get_node_range(1, 1 << (depth - 1))), color=RED)
        sum_reduction_text = Text('Sum Reduction Tree', color=RED).scale(0.6).next_to(sum_reduction_rect, direction=UP)
        
        self.add(tree)

        self.wait(2)

        self.play(Create(cbt), run_time=2)

        self.wait(2)

        self.play(row_texts[-1].animate.set_opacity(1))
        self.play(Create(bitfield_rect), Create(bitfield_text))
        self.wait(1)

        for d in range(1, depth):
            self.play(row_texts[depth - d - 1].animate.set_opacity(1))
            self.wait(1)

        self.play(Create(sum_reduction_rect), Create(sum_reduction_text))

        self.wait(2)
        

class ExampleTree(Scene):
    def construct(self):

        depth = 4
        tree_nodes = [
            1,
            2, 3,
            4, 5,
            8, 9
        ]

        tree = CBT.BinaryTree(depth, active_nodes = tree_nodes)

        sum_reduction_values = CBT.create_cbt(tree_nodes, depth)
        cbt = CBT.BinaryTree(depth, node_data = sum_reduction_values)
        for node in cbt.get_nodes():
            if node:
                node.get_text().set_opacity(0)

        row_texts = []
        for row in cbt.get_rows():
            row_texts.append(VGroup(*[x[0] for x in row]))

        VGroup(tree, cbt).arrange(RIGHT, buff=1.5).move_to([0, 0, 0])

        bitfield_rect = SurroundingRectangle(VGroup(*cbt.get_node_row(depth - 1)), color=BLUE)
        bitfield_text = Text('Bitfield', color=BLUE).scale(0.6).next_to(bitfield_rect, direction=DOWN)

        sum_reduction_rect = SurroundingRectangle(VGroup(* cbt.get_node_range(1, 1 << (depth - 1))), color=RED)
        sum_reduction_text = Text('Sum Reduction Tree', color=RED).scale(0.6).next_to(sum_reduction_rect, direction=UP)
        
        self.add(tree)

        self.wait(6)

        self.play(Create(cbt), run_time=2)

        self.wait(2)

        self.play(row_texts[-1].animate.set_opacity(1))
        self.play(Create(bitfield_rect), Create(bitfield_text))
        self.wait(1)

        for d in range(1, depth):
            self.play(row_texts[depth - d - 1].animate.set_opacity(1))
            self.wait(1)

        self.play(Create(sum_reduction_rect), Create(sum_reduction_text))

        self.wait(2)

class ExampleTreeStatic(Scene):
    def construct(self):

        depth = 4
        tree_nodes = [
            1,
            2, 3,
            4, 5,
            8, 9
        ]

        tree = CBT.BinaryTree(depth, active_nodes = tree_nodes)

        sum_reduction_values = CBT.create_cbt(tree_nodes, depth)
        cbt = CBT.BinaryTree(depth, node_data = sum_reduction_values)

        VGroup(tree, cbt).arrange(RIGHT, buff=1.5).move_to([0, 0, 0])

        self.add(tree)
        self.add(cbt)
