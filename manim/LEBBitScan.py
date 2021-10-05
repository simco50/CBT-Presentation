from manim import *
import Libraries.LEB as LEB

def create_scene(scene, heap_index):
    num_bits = heap_index.bit_length()
    base_tri = LEB.leb_triangle()
    current_matrix = LEB.identity()

    # Numbers and grid
    value_text = Text(f'{heap_index}')
    bits = [x for x in f'{heap_index:b}']
    bit_table = Table([bits], include_outer_lines=True).scale(0.4)
    number_group = VGroup(value_text, bit_table).arrange(DOWN, center=False)

    # Triangle
    start_tri = Polygon(*LEB.transform_vertices(base_tri), color = RED)

    # Main start
    start_group = VGroup(number_group, start_tri).arrange()

    highlighters = []
    for i in range(len(bits)):
        highlighters.append(BackgroundRectangle(bit_table.get_cell((1, i+1)).scale(0.4), color=YELLOW))
    
    # Build triangle sets and texts
    texts = []
    triangles = []
    matrices = [base_tri]
    triangles.append(LEB.transform_vertices(base_tri))
    texts.append('1')

    for bit_index in range(num_bits - 1):
        bit = LEB.get_bit(heap_index, bit_index)
        current_matrix = np.matmul(LEB.split_matrix(bit), current_matrix)
        tri = np.matmul(current_matrix, base_tri)
        matrices.append(tri)
        triangles.append(LEB.transform_vertices(tri))
        current_heap_index = heap_index >> (num_bits - bit_index - 2)
        texts.append(f'{current_heap_index}')

    # Move all triangles to the base triangle location
    triangles = [Polygon(*tri) for tri in triangles]
    texts = [Text(t) for t in texts]

    triangles[-1].set_fill(GREEN, 1)

    matrices = [np.delete(a, np.s_[-1:], axis=1) for a in matrices]
    matrices = [Matrix(m).to_edge(UR) for m in matrices]

    gp = VGroup(*triangles)
    gp.move_to(start_tri)

    # Play everything!
    scene.add(start_group)
    scene.wait(5)

    scene.play(Create(matrices[0]), Create(highlighters[0]), Create(triangles[0]), Create(texts[0].move_to(triangles[0].get_center_of_mass())))
    scene.wait(3)

    for i in range(len(triangles) - 1):
        scene.play(
            ReplacementTransform(highlighters[i], highlighters[i + 1]),
            Transform(triangles[i], triangles[i + 1]), 
            ReplacementTransform(matrices[i], matrices[i + 1]), 
            Create(texts[i + 1].move_to(triangles[i + 1].get_center_of_mass())), 
            ReplacementTransform(texts[i], texts[i + 1]))
        scene.wait(1)

    scene.wait(5)

class Demo1(Scene):
    def construct(self):
        create_scene(self, 39)

class Demo2(Scene):
    def construct(self):
        create_scene(self, 52)