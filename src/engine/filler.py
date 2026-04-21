import pygame

class Filler:
    def __init__(self, renderer):
        """
        Inicializa a classe de preenchimento vinculando-a ao renderizador.
        O renderizador fornece a função set_pixel necessária para desenhar no buffer.
        """
        self.renderer = renderer

    def flood_fill(self, target, x, y, fill_color, boundary_color):
            """
            Requisito C: Algoritmo de Preenchimento por Inundação (Flood Fill).
            Funciona expandindo uma cor a partir de um ponto semente (x, y). 
            Utiliza uma estrutura de pilha (stack) para evitar a recursão profunda, 
            preenchendo todos os pixels vizinhos até encontrar a cor de borda (boundary_color) 
            ou a própria cor de preenchimento (fill_color).
            """
            
            fill_rgb = pygame.Color(fill_color)
            bound_rgb = pygame.Color(boundary_color)
            
            stack = [(int(x), int(y))]
            while stack:
                cx, cy = stack.pop()
                if 0 <= cx < self.renderer.width and 0 <= cy < self.renderer.height:
                    current_pixel = target[cx, cy]
                    if current_pixel != target.surface.map_rgb(bound_rgb) and \
                    current_pixel != target.surface.map_rgb(fill_rgb):
                        self.renderer.set_pixel(target, cx, cy, fill_color)
                        stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])

    def scanline_fill(self, target, points, color):
        """
        Requisito C: Scanline simplificado com o método auxiliar. Percorre o polígono 
        linha por linha (de y_min a y_max), encontrando as interseções da linha 
        horizontal com as arestas do polígono e preenchendo os intervalos entre elas.
        """
        if not points: return
        ys = [int(p[1]) for p in points]
        y_min, y_max = min(ys), max(ys)
        
        for y in range(y_min, y_max + 1):
                    intersections = self._get_scanline_intersections(points, y)
                    for i in range(0, len(intersections), 2):
                        x_start = int(intersections[i])
                        x_end = int(intersections[i+1])
                        for x in range(x_start, x_end):
                            self.renderer.set_pixel(target, x, y, color)
                    

    def draw_gradient_scanline(self, x_start, x_end, y, color_start, color_end):
        """
        Interpola cores entre dois pontos em uma linha horizontal.
        Calcula a variação (delta) de R, G e B ao longo da distância (span) 
        para criar um efeito de gradiente suave
        """
        span = x_end - x_start
        if span <= 0: return
        
        r1, g1, b1 = color_start
        r2, g2, b2 = color_end
        
        dr = (r2 - r1) / span
        dg = (g2 - g1) / span
        db = (b2 - b1) / span
        
        for i in range(int(span)):
            r = int(r1 + i * dr)
            g = int(g1 + i * dg)
            b = int(b1 + i * db)
            self.renderer.set_pixel(x_start + i, y, (r, g, b))

    def load_texture(self, path):
        """Converte uma imagem em matriz numérica para o mapeamento de textura."""
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_size()
        matrix = [[img.get_at((x, y)) for y in range(h)] for x in range(w)]
        return matrix, w, h

    def paint_textured_polygon(self, target, screen_w, screen_h, vertices_uv, texture_matrix, tex_w, tex_h):
        """
        Requisito H: Mapeamento de Textura via Scanline.
        Para cada linha horizontal do polígono, o algoritmo interpola as coordenadas 
        de textura (u, v) correspondentes aos pontos de tela. Com as coordenadas (u, v) 
        calculadas para cada pixel, busca-se a cor na matriz da textura.
        """
        n = len(vertices_uv)
        y_coords = [v[1] for v in vertices_uv]
        y_min, y_max = int(min(y_coords)), int(max(y_coords))

        y_min = max(0, y_min)
        y_max = min(screen_h - 1, y_max)

        for y in range(y_min, y_max + 1):
            intersecoes = []
            for i in range(n):
                v0 = vertices_uv[i]
                v1 = vertices_uv[(i + 1) % n]
                
                if int(v0[1]) == int(v1[1]): continue
                if v0[1] > v1[1]: v0, v1 = v1, v0
                if y < v0[1] or y >= v1[1]: continue

                t = (y - v0[1]) / (v1[1] - v0[1])
                x = v0[0] + (v1[0] - v0[0]) * t
                u = v0[2] + (v1[2] - v0[2]) * t
                v = v0[3] + (v1[3] - v0[3]) * t
                intersecoes.append((x, u, v))

            intersecoes.sort(key=lambda k: k[0])

            for i in range(0, len(intersecoes), 2):
                if i + 1 >= len(intersecoes): break
                x_start, u_s, v_s = intersecoes[i]
                x_end, u_e, v_e = intersecoes[i+1]
                
                span = x_end - x_start
                if span <= 0: continue
                
                u_step = (u_e - u_s) / span
                v_step = (v_e - v_s) / span
                
                curr_u, curr_v = u_s, v_s
                
                ix_start = max(0, int(x_start))
                ix_end = min(screen_w - 1, int(x_end))
                
                for x in range(ix_start, ix_end):
                    tx = max(0, min(int(curr_u), tex_w - 1))
                    ty = max(0, min(int(curr_v), tex_h - 1))
                    color = texture_matrix[tx][ty]
                    
                    if color[3] > 10: 
                        self.renderer.set_pixel(target, x, y, color)
                    
                    curr_u += u_step
                    curr_v += v_step

    def _get_scanline_intersections(self, points, y):
        """
        Método auxiliar para encontrar as coordenadas X de interseção entre 
        uma linha horizontal (y) e as arestas do polígono.
        """
        intersections = []
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x)
        
        intersections.sort()
        return intersections
    
    def fill_polygon_gradient(self, target, points, color_top, color_bottom):
        """
        Preenche um polígono aplicando um gradiente de cor vertical.
        Combina o algoritmo de Scanline com a Interpolação Linear (LERP) 
        das cores baseado na altura (y) do pixel em relação à altura total do polígono.
        """
        if not points: return
        
        ys = [int(p[1]) for p in points]
        y_min, y_max = min(ys), max(ys)
        height = y_max - y_min

        screen_h = self.renderer.height

        for y in range(y_min, y_max + 1):
            if y < 0 or y >= screen_h: continue

            t = (y - y_min) / height if height > 0 else 0
            r = int(color_top[0] * (1 - t) + color_bottom[0] * t)
            g = int(color_top[1] * (1 - t) + color_bottom[1] * t)
            b = int(color_top[2] * (1 - t) + color_bottom[2] * t)
            cor_atual = (r, g, b)
            
            intersections = self._get_scanline_intersections(points, y)
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    self.renderer.draw_line(target, intersections[i], y, intersections[i+1], y, cor_atual)