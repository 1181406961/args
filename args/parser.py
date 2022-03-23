from dataclasses import dataclass


@dataclass
class Option:
    logging: bool = False
    directory: str = ''
    port: int = 0
