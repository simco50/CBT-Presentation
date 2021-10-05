from manim import *
import Libraries.LEB as LEB
import Libraries.CBT as CBT
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
        tree_groups = []
    
        for x in range(subd):
            tris = get_polys(x)
            polys = [Polygon(*x[1]) for x in tris]
            texts = []
            nodes = []
            for i in range(len(tris)):
                texts += [Text(f'{tris[i][0]}').move_to(polys[i].get_center_of_mass()).scale(0.6)]
                nodes += CBT.TreeNode(tris[i][0], tris[i][0], subd)

            poly_groups.append(VGroup(*[p for p in polys]))
            text_groups.append(VGroup(*[t for t in texts]))

            tree_groups.append(VGroup(*nodes))
        
        tree_group_main = VGroup(*tree_groups).scale(0.7)
        poly_group_main = VGroup(*poly_groups, *text_groups)

        f = VGroup(poly_group_main, tree_group_main).arrange(RIGHT)
        print(*f)

        for i in range(len(poly_groups)):
            if i > 0:
                self.remove(text_groups[i - 1])
            t = (i + 1)
            self.play(Create(poly_groups[i]), Create(tree_groups[i]), Create(text_groups[i]), run_time=t)
            self.wait(1)

        self.wait(5)