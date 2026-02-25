from portion.core import Terminal


class CommandBase:
    def __init__(self, **kwargs: str) -> None:
        self.logger = Terminal()
