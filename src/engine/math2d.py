import math

class Matrix3x3:
    """
    Classe utilitária para operações de Álgebra Linear em 2D utilizando Coordenadas Homogêneas.
    O uso de matrizes 3x3 permite que translação, rotação e escala sejam tratadas 
    uniformemente como multiplicações de matrizes, facilitando a composição de transformações.
    """
    @staticmethod
    def identity(): return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    @staticmethod
    def translation(tx, ty): return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]

    @staticmethod
    def scale(sx, sy): return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]

    @staticmethod
    def rotation(rad):
        c, s = math.cos(rad), math.sin(rad)
        return [[c, -s, 0], [s, c, 0], [0, 0, 1]]

    @staticmethod
    def multiply(A, B):
        C = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3): C[i][j] += A[i][k] * B[k][j]
        return C
    
    @staticmethod
    def apply(matrix, point):
        """Aplica a matriz 3x3 a um ponto (x, y) retornando (nx, ny)."""
        x, y = point
        nx = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
        ny = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
        return (nx, ny)
    
    @staticmethod
    def rotate_around_point(matrix, angle_rad, pivot_x, pivot_y):
        """Requisito E/D: Garante rotação em torno de um ponto ."""
        m = Matrix3x3.multiply(Matrix3x3.translation(-pivot_x, -pivot_y), matrix)
        m = Matrix3x3.multiply(Matrix3x3.rotation(angle_rad), m)
        return Matrix3x3.multiply(Matrix3x3.translation(pivot_x, pivot_y), m)

    @staticmethod
    def window_to_viewport(janela, viewport):
        """Requisito F: Mapeamento de coordenadas mundo para dispositivo."""
        Wxmin, Wymin, Wxmax, Wymax = janela
        Vxmin, Vymin, Vxmax, Vymax = viewport
        sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
        sy = (Vymin - Vymax) / (Wymax - Wymin)
        m = Matrix3x3.translation(-Wxmin, -Wymin)
        m = Matrix3x3.multiply(Matrix3x3.scale(sx, sy), m)
        return Matrix3x3.multiply(Matrix3x3.translation(Vxmin, Vymax), m)