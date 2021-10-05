from manim import *
import Libraries.LEB as LEB
import Libraries.CBT as CBT
import Libraries.Utilities as Utils

def point_in_triangle(p, v1, v2, v3):
    def _test(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = _test(p, v1, v2) <= 0.0
    b2 = _test(p, v2, v3) <= 0.0
    b3 = _test(p, v3, v1) <= 0.0

    return (b1 == b2) and (b2 == b3) 

def get_adaptive_triangles(heap_index, target, min_depth, max_depth):
    result = []
    depth = Utils.most_signficant_bit(heap_index)
    if depth < max_depth:
        tri = LEB.get_vertices(heap_index)
        in_tri = point_in_triangle(target, tri[0], tri[1], tri[2])
        if depth >= min_depth:
            result.append((heap_index, LEB.get_vertices(heap_index)))
        if in_tri:
            result += get_adaptive_triangles(heap_index * 2, target, min_depth, max_depth)
            result += get_adaptive_triangles(heap_index * 2 + 1, target, min_depth, max_depth)
    return result

def create_scene(scene, with_tree):
    point = [0.3, 0.1, 0]
    circle = Circle(0.1).move_to(LEB.transform_vertices([point])[0])
    pnt = Circle(0.01).move_to(LEB.transform_vertices([point])[0])

    base_tri = Polygon(*LEB.transform_vertices(LEB.get_vertices(1)))

    node_groups = []
    triangle_groups = []

    subd = 5

    leaf_nodes = []
    texts = []
    index_to_node = {}
    index_to_poly = {}

    for i in range(0, subd):
        tris = get_adaptive_triangles(1, point, i, i + 1)
        if len(tris) > 0:
            polys = []
            nodes = []
            for x in tris:
                if x[0] >> 1 in leaf_nodes:
                    leaf_nodes.remove(x[0] >> 1)
                leaf_nodes.append(x[0])

                poly = Polygon(*LEB.transform_vertices(x[1]))

                node = CBT.TreeNode(x[0], x[0], subd)

                index_to_node[x[0]] = node[0]
                index_to_poly[x[0]] = poly
                nodes += node
                polys.append(poly)

            triangle_groups.append(VGroup(*polys))
            node_groups.append(VGroup(*nodes))
    
    triangle_group = VGroup(*triangle_groups, circle, pnt, base_tri)
    node_group = VGroup(*node_groups).scale(0.7)
    VGroup(triangle_group, node_group).arrange(RIGHT)
    
    leaf_boxes = [BackgroundRectangle(index_to_node[x], color=YELLOW, fill_opacity=0.4) for x in leaf_nodes]
    texts = [Text(f'{x}').scale(0.6).move_to(index_to_poly[x].get_center_of_mass()) for x in leaf_nodes]

    scene.add(base_tri)

    scene.play(Create(pnt))
    scene.play(Create(circle))

    scene.wait(2)

    for i in range(len(triangle_groups)):
        scene.play(Create(node_groups[i]), Create(triangle_groups[i]))
        scene.wait(0.5)

    scene.wait(1)

    scene.play(*[Create(x) for x in leaf_boxes], *[Create(x) for x in texts])

    scene.wait(5)

class Main(Scene):
    def construct(self):
        create_scene(self, True)