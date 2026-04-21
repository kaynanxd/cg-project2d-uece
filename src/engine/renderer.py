class Renderer:
    def __init__(self, surface):
        """
        Inicializa o renderizador vinculando-o a uma superfície do Pygame.
        Armazena largura e altura para realizar o clipping (recorte) de segurança.
        """
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()

    def set_pixel(self, target, x, y, color):
        """
        Requisito A: Única função que interage com o buffer de pixels.
        Verifica se as coordenadas estão dentro dos limites da tela para evitar 
        erros de índice no PixelArray. Converte para inteiro para garantir 
        o endereçamento correto na matriz de pixels.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            target[int(x), int(y)] = color

    def draw_line(self, target, x0, y0, x1, y1, color):
        """
        Requisito B: Algoritmo de Bresenham.
        O algoritmo utiliza apenas aritmética de inteiros para decidir qual pixel 
        melhor aproxima a reta ideal. Ele calcula um parâmetro de decisão (d) 
        que define se a próxima coordenada deve ser incrementada apenas no eixo 
        principal ou em ambos, minimizando o erro acumulado.
        """
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep: x0, y0 = y0, x0; x1, y1 = y1, x1
        if x0 > x1: x0, x1 = x1, x0; y0, y1 = y1, y0
        dx = x1 - x0; dy = abs(y1 - y0)
        ystep = 1 if y0 < y1 else -1
        d = 2 * dy - dx
        y = y0
        for x in range(x0, x1 + 1):
            if steep: self.set_pixel(target, y, x, color) 
            else: self.set_pixel(target, x, y, color)
            if d > 0: y += ystep; d -= 2 * dx
            d += 2 * dy

    def draw_circle(self, target, xc, yc, r, color):
        """
        Requisito B: Algoritmo de Ponto Médio para Círculo.
        Baseia-se na simetria de oito octantes do círculo. O algoritmo calcula 
        os pontos para apenas um octante (45°) e utiliza a função auxiliar 
        _circle_points para replicar o ponto nos outros sete, otimizando o cálculo.
        """
        x, y = 0, r
        d = 1 - r
        self._circle_points(target, xc, yc, x, y, color)
        while x < y:
            if d < 0: d += 2 * x + 3
            else: d += 2 * (x - y) + 5; y -= 1
            x += 1
            self._circle_points(target, xc, yc, x, y, color)

    def _circle_points(self, target, xc, yc, x, y, color):
        """
        Aplica a simetria de 8 vias do círculo. Desenha os pontos correspondentes 
        em todos os quadrantes a partir de um único cálculo de octante.
        """
        for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
            self.set_pixel(target, xc + dx, yc + dy, color)

    def draw_ellipse(self, target, xc, yc, rx, ry, color):
        """
        Requisito B: Algoritmo de Ponto Médio para Elipse.
        Dividido em duas regiões baseadas na inclinação da curva. 
        Região 1: Inclinação < 1 (mais horizontal).
        Região 2: Inclinação > 1 (mais vertical).
        Em cada região, o algoritmo avalia o parâmetro de decisão para escolher 
        o pixel que minimiza a distância da curva teórica da elipse.
        """
        x, y = 0, ry
        rx2, ry2 = rx*rx, ry*ry
        d1 = ry2 - (rx2 * ry) + (0.25 * rx2)
        dx, dy = 2 * ry2 * x, 2 * rx2 * y
        while dx < dy:
            self._ellipse_points(target, xc, yc, x, y, color)
            x += 1; dx += 2 * ry2
            if d1 < 0: d1 += dx + ry2
            else: y -= 1; dy -= 2 * rx2; d1 += dx - dy + ry2
        d2 = (ry2 * (x + 0.5)**2) + (rx2 * (y - 1)**2) - (rx2 * ry2)
        while y >= 0:
            self._ellipse_points(target, xc, yc, x, y, color)
            y -= 1; dy -= 2 * rx2
            if d2 > 0: d2 += rx2 - dy
            else: x += 1; dx += 2 * ry2; d2 += dx - dy + rx2

    def _ellipse_points(self, target, xc, yc, x, y, color):
        for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y)]:
            self.set_pixel(target, xc + dx, yc + dy, color)