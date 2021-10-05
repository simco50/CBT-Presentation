from manim import *
import Libraries.LEB as LEB
import Libraries.Utilities as Utils

def get_triangle_polys(heap_index, polys, depth):
    d = Utils.most_signficant_bit(heap_index)
    if d < depth:
        get_triangle_polys(heap_index * 2, polys, depth)
        get_triangle_polys(heap_index * 2 + 1, polys, depth)
    else:
        verts = LEB.get_vertices(heap_index)
        tri_list = LEB.transform_vertices(verts)
        polys.append((heap_index, tri_list))

def get_polys(depth):
    polys = []
    get_triangle_polys(1, polys, depth)
    return polys

class Main(Scene):
    def construct(self):
        subd = 5

        poly_groups = []
        text_groups = []
    
        for x in range(subd):
            tris = get_polys(x)
            polys = [Polygon(*x[1]) for x in tris]
            texts = []
            for i in range(len(tris)):
                texts += [Text(f'{tris[i][0]}').move_to(polys[i].get_center_of_mass()).scale(0.6)]

            poly_groups.append(polys)
            text_groups.append(texts)

        for i in range(len(poly_groups)):
            if i > 0:
                self.remove(*text_groups[i - 1])
            f = [Create(p) for p in poly_groups[i]] + [Create(t) for t in text_groups[i]]
            self.play(*f)
            self.wait(1)

        self.wait(5)