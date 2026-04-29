class Timer:
    def __init__(self):
        self._elapsed_ms: int = 0

    def update(self, delta_ms: int) -> None:
        self._elapsed_ms += delta_ms

    def elapsed_seconds(self) -> float:
        return self._elapsed_ms / 1000

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass
