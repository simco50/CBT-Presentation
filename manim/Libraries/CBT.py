from manim import *
import Libraries.Utilities as Utils

def bitfield_heap_index(heap_index, max_depth) -> int:
    depth = Utils.most_signficant_bit(heap_index)
    return heap_index * (1 << (max_depth - depth - 1))

def create_cbt(nodes, max_depth) -> 'list[int]':
    data = [0 for x in range(1 << (max_depth))]

    # bitfield setup
    for x in nodes:
        data[bitfield_heap_index(x, max_depth)] = 1

    # sum reduction
    for d in reversed(range(max_depth - 1)):
        for i in range(1 << d, 2 << d):
            l = data[i << 1]
            r = data[(i << 1) | 1]
            data[i] = l + r
    return data

class TreeNode(VMobject):
    def __init__(self, heap_index, value, max_tree_depth, color=WHITE, **kwargs):
        super().__init__(color=color, **kwargs)

        depth = Utils.most_signficant_bit(heap_index)
        
        offset = pow(2, max_tree_depth - depth - 1) * 0.5
        x = (heap_index - pow(2, depth)) * offset
        y = max_tree_depth - depth

        self.value = value
        self.text = Text(f'{value}', color = color).move_to([x, y, 0]).scale(0.6)
        self.rectangle = Rectangle(color = color, height = 0.5, width = 0.5).move_to(self.text)
        self.node = VGroup(self.text, self.rectangle)
        self.add(self.node)

        self.lines = []
        if heap_index > 1:
            if heap_index % 2 == 0:
                self.lines.append(Line(end=[x, y + 0.25, 0], start=[x, y + 0.75, 0], color = color))
            else:
                self.lines.append(Line(end=[x, y + 1, 0], start=[x - offset + 0.25, y + 1, 0], color = color))
                self.lines.append(Line(end=[x, y + 0.25, 0], start=[x, y + 1, 0], color = color))
        self.add(*self.lines)

    def get_value(self) -> int:
        return self.value

    def get_text(self) -> Text:
        return self.text
    
    def get_node(self):
        return self.node

    def get_lines(self):
        return self.lines

    def value_set(self, value):
        self.text.text = f'{value}'

class BinaryTree(VMobject):
    def __init__(self, depth : int, active_nodes : list = None, node_data : list = None, color=WHITE, **kwargs):
        super().__init__(color=color, **kwargs)
        self.nodes = [None]
        self.max_depth = depth
        for x in range(1, 1 << depth):
            value = x
            if node_data:
                value = node_data[x]
            node = TreeNode(x, value, depth, color=color)
            if active_nodes and x not in active_nodes:
                node.set_color(utils.color.rgb_to_color([0.3, 0.3, 0.3]))
                node.set_z_index(-1)
            self.nodes.append(node)
            self.add(self.nodes[-1])

        self.node_rows = []
        self.rows = []
        for d in range(depth):
            self.node_rows.append([x.node for x in self.nodes[(1 << d) : (2 << d)]])
            self.rows.append([x for x in self.nodes[(1 << d) : (2 << d)]])

    def set_node_value(self, index, value):
        self.nodes[index].value_set(value)

    def get_node(self, index) -> VGroup:
        return self.nodes[index].node

    def get_nodes(self) -> 'list[TreeNode]':
        return self.nodes

    def get_node_row(self, depth) -> VGroup:
        return VGroup(*self.node_rows[depth])

    def get_rows(self):
        return self.node_rows

    def get_node_range(self, min_range, max_range):
        return [x.node for x in self.nodes[min_range:max_range]]

    def bitfield_node(self, heap_index) -> VGroup:
        id = bitfield_heap_index(heap_index, self.max_depth)
        return self.get_node(id)

    def get_bitfield_range_for_node(self, heap_index):
        depth = Utils.most_signficant_bit(heap_index)
        zeros = (1 << (self.max_depth - depth - 1))
        id = bitfield_heap_index(heap_index, self.max_depth)
        return self.get_node_range(id, id + zeros + 1)

