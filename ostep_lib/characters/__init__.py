"""Characters for the OSTEP series: Professor, Student, Computer, Process."""
from .base import Character, CharacterChange
from .bubbles import Bubble, BubbleIn
from .humanoid import Professor, Student
from .computer import Computer
from .process import Process

__all__ = [
    "Character", "CharacterChange", "Bubble", "BubbleIn",
    "Professor", "Student", "Computer", "Process",
]
