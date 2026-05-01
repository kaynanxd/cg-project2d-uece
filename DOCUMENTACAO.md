# Documentação da Engine 2D — UECE CG

Motor gráfico 2D em Python/Pygame com implementação manual de algoritmos de renderização, transformações e detecção de colisão.

---

## Índice

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Como Criar uma Tela](#como-criar-uma-tela)
3. [Como Criar Botões e Atribuir Funções](#como-criar-botões-e-atribuir-funções)
4. [Como Criar Objetos/Componentes para Telas](#como-criar-objetoscomponentes-para-telas)
5. [Referência da API](#referência-da-api)
   - [Engine](#engine)
   - [Renderer](#renderer)
   - [Filler](#filler)
   - [Clipping](#clipping)
   - [Matrix3x3](#matrix3x3)
   - [Collision](#collision)

---

## Visão Geral da Arquitetura

A engine segue um padrão de **máquina de estados**: o `Engine` central gerencia qual tela está ativa e delega eventos e renderização para a tela correspondente.

```
Engine (loop principal + estado)
 ├── state = "SPLASH" → SplashScreen
 ├── state = "MENU"   → MainMenu
 └── state = "GAME"   → [sua tela de jogo]

Camadas internas:
 ├── Renderer   — desenho de pixels, linhas, círculos, elipses
 ├── Filler     — preenchimento de polígonos, flood fill, gradientes, texturas
 ├── Clipping   — recorte de linhas (Cohen-Sutherland)
 └── Matrix3x3  — transformações 2D (translação, escala, rotação)
```

### Fluxo de renderização por frame

```
Engine.run()
 ├── Processa eventos pygame → tela_ativa.handle_event(event)
 ├── Atualiza lógica       → tela_ativa.update()
 ├── Abre PixelArray
 ├── Desenha pixels        → tela_ativa.draw(px_array)
 ├── Fecha PixelArray
 ├── Desenha UI (texto)    → tela_ativa.draw_ui()
 └── pygame.display.flip()
```

> **Regra importante:** Tudo que usa `set_pixel` / `draw_line` / `scanline_fill` deve estar dentro de `draw(px_array)`. Texto renderizado por Pygame (`font.render`) deve estar em `draw_ui()`, que roda depois do PixelArray ser fechado.

---

## Como Criar uma Tela

Uma tela é uma classe Python comum que segue um contrato de quatro métodos. Não há classe base obrigatória — o contrato é implícito.

### Contrato de uma tela

```python
class MinhaTela:
    def __init__(self, engine): ...   # recebe referência ao Engine
    def update(self):           ...   # lógica por frame (sem desenho)
    def draw(self, px_array):   ...   # renderização pixel a pixel
    def draw_ui(self):          ...   # texto e UI Pygame (após fechar px_array)
    def handle_event(self, event): ...  # eventos de mouse/teclado
```

### Exemplo mínimo — tela com fundo e título

```python
# src/game/minha_tela.py
import pygame

class MinhaTela:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler

        self.COR_FUNDO = (20, 20, 50)
        self.COR_BORDA = (255, 255, 255)
        self.fonte = pygame.font.SysFont("Arial", 36, bold=True)

    def update(self):
        pass  # lógica de animação viria aqui

    def draw(self, px_array):
        w = self.renderer.width
        h = self.renderer.height

        # 1. desenha borda para o flood_fill ter onde parar
        self.renderer.draw_line(px_array, 0,   0,   w-1, 0,   self.COR_BORDA)
        self.renderer.draw_line(px_array, w-1, 0,   w-1, h-1, self.COR_BORDA)
        self.renderer.draw_line(px_array, w-1, h-1, 0,   h-1, self.COR_BORDA)
        self.renderer.draw_line(px_array, 0,   h-1, 0,   0,   self.COR_BORDA)

        # 2. preenche o fundo
        self.filler.flood_fill(px_array, w//2, h//2, self.COR_FUNDO, self.COR_BORDA)

    def draw_ui(self):
        surf = self.engine.screen
        texto = self.fonte.render("Minha Tela", True, (255, 255, 255))
        surf.blit(texto, (self.renderer.width//2 - texto.get_width()//2, 40))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.state = "MENU"
```

### Registrando a tela no Engine

No `Engine.__init__`, instancie sua tela e adicione a lógica de roteamento no `run()`:

```python
# src/game/engine.py

# __init__ — instanciar
self.minha_tela = MinhaTela(self)

# run() — dentro do loop, bloco de eventos
if self.state == "MINHA_TELA":
    minha_tela.handle_event(event)

# run() — dentro do loop, bloco de renderização
if self.state == "MINHA_TELA":
    with pygame.PixelArray(self.screen) as px:
        self.minha_tela.draw(px)
    self.minha_tela.update()
    self.minha_tela.draw_ui()
```

### Navegando entre telas

A troca de tela é feita simplesmente alterando `engine.state`:

```python
# Ir para o menu
self.engine.state = "MENU"

# Ir para uma tela de jogo customizada
self.engine.state = "MINHA_TELA"
```

---

## Como Criar Botões e Atribuir Funções

Botões são representados como **tuplas de retângulo** `(x, y, largura, altura)`. A detecção de clique usa `is_clicked()` de `collision.py`.

### Estrutura básica

```python
from src.engine.collision import is_clicked
from src.engine.math2d import Matrix3x3
import pygame

class MinhaTelaComBotoes:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler

        # 1. Defina geometria dos botões como tuplas (x, y, w, h)
        btn_w, btn_h = 200, 50
        cx = (self.renderer.width - btn_w) // 2

        self.botoes = [
            (cx, 300, btn_w, btn_h),  # botão 0
            (cx, 380, btn_w, btn_h),  # botão 1
            (cx, 460, btn_w, btn_h),  # botão 2
        ]
        self.labels = ["Jogar", "Opções", "Sair"]

        # 2. Mapeie cada índice para uma função callback
        self.callbacks = {
            0: self._on_jogar,
            1: self._on_opcoes,
            2: self._on_sair,
        }

        # Cores
        self.COR_NORMAL = (30, 30, 80)
        self.COR_HOVER  = (60, 60, 140)
        self.COR_BORDA  = (255, 255, 255)
        self.fonte = pygame.font.SysFont("Arial", 22)

    # --- callbacks ---

    def _on_jogar(self):
        self.engine.state = "GAME"

    def _on_opcoes(self):
        print("opções ainda não implementadas")

    def _on_sair(self):
        pygame.quit()
        exit()

    # --- eventos ---

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for i, rect in enumerate(self.botoes):
                if is_clicked(mouse, rect) and i in self.callbacks:
                    self.callbacks[i]()   # chama a função associada

    # --- renderização ---

    def draw(self, px_array):
        mouse = pygame.mouse.get_pos()

        for rect in self.botoes:
            x, y, w, h = rect
            hover = is_clicked(mouse, rect)
            cor = self.COR_HOVER if hover else self.COR_NORMAL

            # efeito de escala ao passar o mouse
            if hover:
                cx, cy = x + w / 2, y + h / 2
                m = Matrix3x3.translation(-cx, -cy)
                m = Matrix3x3.multiply(Matrix3x3.scale(1.05, 1.05), m)
                m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
                pontos = [Matrix3x3.apply(m, p)
                          for p in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]]
            else:
                pontos = [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]

            self.filler.scanline_fill(px_array, pontos, cor)

            # borda com clipping
            lados = list(zip(pontos, pontos[1:] + [pontos[0]]))
            for p1, p2 in lados:
                ok, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(
                    p1[0], p1[1], p2[0], p2[1]
                )
                if ok:
                    self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.COR_BORDA)

    def draw_ui(self):
        surf = self.engine.screen
        for i, rect in enumerate(self.botoes):
            x, y, w, h = rect
            t = self.fonte.render(self.labels[i], True, (255, 255, 255))
            surf.blit(t, (x + (w - t.get_width()) // 2,
                          y + (h - t.get_height()) // 2))

    def update(self):
        pass
```

### Adicionando um botão de ícone com textura

```python
# No __init__:
tex, tw, th = self.filler.load_texture("assets/star.png")
self.icone, self.iw, self.ih = Matrix3x3.scale_image_matrix(tex, tw, th, 0.5)
self.icone_pos = (50, 50)

# No draw(px_array):
self.filler.draw_image_manual(px_array, self.icone,
                               self.icone_pos[0], self.icone_pos[1],
                               self.iw, self.ih)
```

---

## Como Criar Objetos/Componentes para Telas

Assim como componentes em React encapsulam estado e renderização, você pode criar classes de objeto que se auto-desenham — análogo ao padrão **Component/Entity**.

### Padrão de componente

```python
class MeuComponente:
    def __init__(self, engine, x, y):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.x = x
        self.y = y

    def update(self):
        """Atualiza estado interno (animação, lógica)."""
        pass

    def draw(self, px_array):
        """Renderiza o componente no pixel array."""
        pass

    def draw_ui(self):
        """Renderiza texto/UI Pygame por cima."""
        pass

    def handle_event(self, event):
        """Responde a eventos, se necessário."""
        pass
```

A tela que contém o componente simplesmente delega as chamadas:

```python
class MinhaTelaComComponentes:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler

        # instancia componentes como atributos
        self.painel = Painel(engine, x=100, y=100, largura=400, altura=300)
        self.avatar = Avatar(engine, x=50, y=50, imagem="assets/star.png")
        self.hud    = HUD(engine)

    def update(self):
        self.painel.update()
        self.avatar.update()
        self.hud.update()

    def draw(self, px_array):
        self.painel.draw(px_array)
        self.avatar.draw(px_array)
        self.hud.draw(px_array)

    def draw_ui(self):
        self.painel.draw_ui()
        self.avatar.draw_ui()
        self.hud.draw_ui()

    def handle_event(self, event):
        self.painel.handle_event(event)
        self.avatar.handle_event(event)
```

### Exemplo completo — componente Painel

```python
class Painel:
    def __init__(self, engine, x, y, largura, altura, titulo="Painel"):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.x, self.y = x, y
        self.w, self.h = largura, altura
        self.titulo = titulo

        self.COR_FUNDO  = (20, 20, 60)
        self.COR_BORDA  = (100, 180, 255)
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def update(self):
        pass

    def draw(self, px_array):
        x, y, w, h = self.x, self.y, self.w, self.h
        pontos = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]

        self.filler.scanline_fill(px_array, pontos, self.COR_FUNDO)

        lados = list(zip(pontos, pontos[1:] + [pontos[0]]))
        for p1, p2 in lados:
            ok, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(
                p1[0], p1[1], p2[0], p2[1]
            )
            if ok:
                self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.COR_BORDA)

    def draw_ui(self):
        t = self.fonte.render(self.titulo, True, (255, 255, 255))
        self.engine.screen.blit(t, (self.x + 8, self.y + 6))
```

### Exemplo completo — componente Avatar (imagem + animação)

```python
import math

class Avatar:
    def __init__(self, engine, x, y, imagem_path):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.x, self.y = x, y

        tex, tw, th = self.filler.load_texture(imagem_path)
        self.tex, self.tw, self.th = Matrix3x3.scale_image_matrix(tex, tw, th, 1.0)

        self.frame = 0          # contador para animações

    def update(self):
        self.frame += 1

    def draw(self, px_array):
        # flutua verticalmente usando seno
        offset_y = int(math.sin(self.frame * 0.05) * 8)
        self.filler.draw_image_manual(
            px_array, self.tex,
            self.x, self.y + offset_y,
            self.tw, self.th
        )

    def draw_ui(self):
        pass

    def handle_event(self, event):
        pass
```

### Lista dinâmica de componentes

Para telas com quantidade variável de objetos (ex.: inimigos, projéteis):

```python
class TelaJogo:
    def __init__(self, engine):
        self.engine = engine
        self.objetos = []   # lista dinâmica

    def adicionar(self, obj):
        self.objetos.append(obj)

    def remover(self, obj):
        self.objetos.remove(obj)

    def update(self):
        for obj in self.objetos:
            obj.update()
        # remove objetos marcados para destruição
        self.objetos = [o for o in self.objetos if not getattr(o, "destruido", False)]

    def draw(self, px_array):
        for obj in self.objetos:
            obj.draw(px_array)

    def draw_ui(self):
        for obj in self.objetos:
            obj.draw_ui()

    def handle_event(self, event):
        for obj in self.objetos:
            obj.handle_event(event)
```

---

## Referência da API

### Engine

**`Engine(width, height)`** — inicializa o motor gráfico.

| Atributo | Tipo | Descrição |
|---|---|---|
| `engine.screen` | `pygame.Surface` | Superfície de exibição |
| `engine.renderer` | `Renderer` | Instância do renderizador |
| `engine.filler` | `Filler` | Instância do preenchedor |
| `engine.clipping` | `Clipping` | Instância do recortador |
| `engine.state` | `str` | Estado atual: `"SPLASH"`, `"MENU"`, `"GAME"` |
| `engine.click_sound` | `Sound` | Som de clique (pode ser `None`) |

---

### Renderer

**`Renderer(surface)`** — operações de renderização de baixo nível.

```python
renderer.set_pixel(px_array, x, y, cor)
```
Define um pixel na posição `(x, y)`. `cor` é uma tupla `(R, G, B)` ou `(R, G, B, A)`.

```python
renderer.draw_line(px_array, x0, y0, x1, y1, cor)
```
Linha de `(x0, y0)` a `(x1, y1)` pelo algoritmo de Bresenham.

```python
renderer.draw_circle(px_array, xc, yc, raio, cor)
```
Circunferência centrada em `(xc, yc)` pelo algoritmo do ponto médio.

```python
renderer.draw_ellipse(px_array, xc, yc, rx, ry, cor)
```
Elipse centrada em `(xc, yc)` com semi-eixos `rx` (horizontal) e `ry` (vertical).

---

### Filler

**`Filler(renderer)`** — preenchimento de formas e texturas.

```python
filler.flood_fill(px_array, x, y, cor_fill, cor_borda)
```
Preenche a região a partir do ponto semente `(x, y)` com `cor_fill`, parando em `cor_borda`.

```python
filler.scanline_fill(px_array, pontos, cor)
```
Preenche o polígono definido por `pontos` (lista de `(x, y)`) com `cor` uniforme.

```python
filler.fill_polygon_gradient(px_array, pontos, cor_topo, cor_base)
```
Preenche o polígono com gradiente vertical de `cor_topo` a `cor_base`.

```python
matrix, w, h = filler.load_texture(caminho)
```
Carrega imagem do disco como matriz 2D `matrix[x][y] = (R, G, B, A)`.

```python
filler.draw_image_manual(px_array, matrix, start_x, start_y, tex_w, tex_h)
```
Renderiza a matriz de textura na posição `(start_x, start_y)`. Respeita canal alfa.

```python
filler.paint_textured_polygon(px_array, sw, sh, vertices_uv, tex_matrix, tw, th)
```
Renderiza polígono texturizado. `vertices_uv` é lista de `(x, y, u, v)`.

---

### Clipping

**`Clipping(xmin, ymin, xmax, ymax)`** — recorte de segmentos de reta.

```python
aceito, x0, y0, x1, y1 = clipping.cohen_sutherland(x0, y0, x1, y1)
```
Recorta o segmento à janela definida no construtor. Retorna `(bool, x0, y0, x1, y1)`.

```python
codigo = clipping.get_code(x, y)
```
Retorna o código de região do ponto (bits: LEFT=1, RIGHT=2, TOP=4, BOTTOM=8).

---

### Matrix3x3

Métodos estáticos para transformações 2D em coordenadas homogêneas.

```python
m = Matrix3x3.identity()
m = Matrix3x3.translation(tx, ty)
m = Matrix3x3.scale(sx, sy)
m = Matrix3x3.rotation(radianos)
```

```python
m = Matrix3x3.multiply(A, B)   # C = A * B
x2, y2 = Matrix3x3.apply(m, (x, y))
```

**Escalar em torno de um ponto arbitrário:**
```python
cx, cy = centro_x, centro_y
m = Matrix3x3.translation(-cx, -cy)
m = Matrix3x3.multiply(Matrix3x3.scale(sx, sy), m)
m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
pontos_transformados = [Matrix3x3.apply(m, p) for p in pontos]
```

**Rotacionar em torno de um pivô:**
```python
m = Matrix3x3.rotate_around_point(Matrix3x3.identity(), angulo_rad, px, py)
```

**Mapear coordenadas de mundo para viewport:**
```python
janela   = (Wxmin, Wymin, Wxmax, Wymax)
viewport = (Vxmin, Vymin, Vxmax, Vymax)
m = Matrix3x3.window_to_viewport(janela, viewport)
```

**Redimensionar matriz de imagem:**
```python
nova_matrix, nw, nh = Matrix3x3.scale_image_matrix(matrix, w, h, fator)
# fator=0.5 → metade do tamanho; fator=2.0 → dobro
```

---

### Collision

Funções livres em `src/engine/collision.py`.

```python
from src.engine.collision import point_box, is_clicked

dentro = point_box(px, py, (box_x, box_y, box_w, box_h))
clicou = is_clicked((mx, my), (rx, ry, rw, rh))
```

Ambas retornam `bool`. `is_clicked` é a mais usada para botões.
