class Clipping:
    """
    Implementação do algoritmo de recorte (clipping) de linhas.
    Essencial para garantir que o motor gráfico não tente processar ou desenhar
    pixels fora da área visível da janela ou viewport, economizando processamento.
    """
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def __init__(self, xmin, ymin, xmax, ymax):
        """
        Define os limites da região de recorte (geralmente os limites da tela ou de uma janela).
        """
        self.limits = (xmin, ymin, xmax, ymax)

    def get_code(self, x, y):
        """
        Atribui um código binário (Region Code) a um ponto (x, y) baseado em sua 
        posição em relação ao retângulo de recorte.
        Determina se o ponto está à esquerda, direita, acima ou abaixo dos limites.
        """
        xmin, ymin, xmax, ymax = self.limits
        code = self.INSIDE
        if x < xmin: code |= self.LEFT
        elif x > xmax: code |= self.RIGHT
        if y < ymin: code |= self.TOP
        elif y > ymax: code |= self.BOTTOM
        return code

    def cohen_sutherland(self, x0, y0, x1, y1):
        """
        Requisito G: Algoritmo de Recorte de Linhas de Cohen-Sutherland.
        Utiliza os códigos de região para decidir rapidamente se uma linha está:
        1. Totalmente dentro (Aceite trivial);
        2. Totalmente fora (Rejeição trivial via operação AND binária);
        3. Parcialmente dentro (Divide a linha nas bordas e testa novamente).
        Retorna (True, x_clipped, y_clipped) se houver algo a desenhar, ou False caso contrário.
        """
        xmin, ymin, xmax, ymax = self.limits
        c0, c1 = self.get_code(x0, y0), self.get_code(x1, y1)
        while True:
            if not (c0 | c1): return True, x0, y0, x1, y1
            if c0 & c1: return False, 0, 0, 0, 0
            code_out = c0 if c0 else c1
            if code_out & self.TOP: x = x0 + (x1-x0)*(ymin-y0)/(y1-y0); y = ymin
            elif code_out & self.BOTTOM: x = x0 + (x1-x0)*(ymax-y0)/(y1-y0); y = ymax
            elif code_out & self.RIGHT: y = y0 + (y1-y0)*(xmax-x0)/(x1-x0); x = xmax
            elif code_out & self.LEFT: y = y0 + (y1-y0)*(xmin-x0)/(x1-x0); x = xmin
            if code_out == c0: x0, y0, c0 = x, y, self.get_code(x, y)
            else: x1, y1, c1 = x, y, self.get_code(x, y)