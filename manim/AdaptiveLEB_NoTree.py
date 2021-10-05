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

class Main(Scene):
    def construct(self):
        point = [0.3, 0.1, 0]
        circle = Circle(0.1).move_to(LEB.transform_vertices([point])[0])
        pnt = Circle(0.01).move_to(LEB.transform_vertices([point])[0])

        base_tri = Polygon(*LEB.transform_vertices(LEB.get_vertices(1)))

        triangle_groups = []

        subd = 5

        texts = []
        index_to_poly = {}

        for i in range(0, subd):
            tris = get_adaptive_triangles(1, point, i, i + 1)
            if len(tris) > 0:

                polys = []
                for x in tris:
                    poly = Polygon(*LEB.transform_vertices(x[1]))

                    index_to_poly[x[0]] = poly
                    polys.append(poly)

                triangle_groups.append(VGroup(*polys))
        
        VGroup(*triangle_groups, circle, pnt, base_tri)

        self.add(base_tri)

        self.wait(4)

        self.play(Create(pnt))
        self.play(Create(circle))

        self.wait(2)

        for i in range(len(triangle_groups)):
            self.play(Create(triangle_groups[i]))
            self.wait(0.5)

        self.wait(1)

        self.wait(5)