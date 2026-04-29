import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self._music_volume = 0.05
        self._sfx = {}

    def load_sfx(self, name, path):
        try:
            self._sfx[name] = pygame.mixer.Sound(path)
        except:
            print(f"Erro ao carregar SFX: {path}")
            self._sfx[name] = None

    def play_sfx(self, name):
        sfx = self._sfx.get(name)
        if sfx: sfx.play()

    def play_music(self, path, loop=True):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self._music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except:
            print(f"Erro ao carregar música: {path}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, vol):
        self._music_volume = vol
        pygame.mixer.music.set_volume(vol)