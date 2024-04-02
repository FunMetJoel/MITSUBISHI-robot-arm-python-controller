from __future__ import annotations
from typing import List, Tuple
from enum import Enum

class JointPos:
    def __init__(self, j1:float, j2:float, j3:float, j4:float, j5:float, j6:float) -> None:
        self.j1 = j1
        self.j2 = j2
        self.j3 = j3
        self.j4 = j4
        self.j5 = j5
        self.j6 = j6

    def __str__(self) -> str:
        return f"({self.j1},{self.j2},{self.j3},{self.j4},{self.j5},{self.j6})"
    
    def __add__(self, other:JointPos) -> JointPos:
        return JointPos(self.j1 + other.j1, self.j2 + other.j2, self.j3 + other.j3, self.j4 + other.j4, self.j5 + other.j5, self.j6 + other.j6)
    
    def __iadd__(self, other:JointPos) -> JointPos:
        return JointPos(self.j1 + other.j1, self.j2 + other.j2, self.j3 + other.j3, self.j4 + other.j4, self.j5 + other.j5, self.j6 + other.j6)
    
    def __sub__(self, other:JointPos) -> JointPos:
        return JointPos(self.j1 - other.j1, self.j2 - other.j2, self.j3 - other.j3, self.j4 - other.j4, self.j5 - other.j5, self.j6 - other.j6)
    
    def __isub__(self, other:JointPos) -> JointPos:
        return JointPos(self.j1 - other.j1, self.j2 - other.j2, self.j3 - other.j3, self.j4 - other.j4, self.j5 - other.j5, self.j6 - other.j6)
    
    def __mul__(self, other:float) -> JointPos:
        return JointPos(self.j1 * other, self.j2 * other, self.j3 * other, self.j4 * other, self.j5 * other, self.j6 * other)
    
    def __imul__(self, other:float) -> JointPos:
        return JointPos(self.j1 * other, self.j2 * other, self.j3 * other, self.j4 * other, self.j5 * other, self.j6 * other)
    
    def __truediv__(self, other:float) -> JointPos:
        return JointPos(self.j1 / other, self.j2 / other, self.j3 / other, self.j4 / other, self.j5 / other, self.j6 / other)
    
    def __itruediv__(self, other:float) -> JointPos:
        return JointPos(self.j1 / other, self.j2 / other, self.j3 / other, self.j4 / other, self.j5 / other, self.j6 / other)
    
    def __eq__(self, other:JointPos) -> bool:
        return self.j1 == other.j1 and self.j2 == other.j2 and self.j3 == other.j3 and self.j4 == other.j4 and self.j5 == other.j5 and self.j6 == other.j6
    
    def __ne__(self, other:JointPos) -> bool:
        return not self == other
    
    def __format__(self, __format_spec: str) -> str:
        return f"({self.j1},{self.j2},{self.j3},{self.j4},{self.j5},{self.j6})"
    
    def __neg__(self) -> JointPos:
        return JointPos(-self.j1, -self.j2, -self.j3, -self.j4, -self.j5, -self.j6)
    
    def __abs__(self) -> float:
        return (self.j1**2 + self.j2**2 + self.j3**2 + self.j4**2 + self.j5**2 + self.j6**2)**0.5
    
    def __round__(self, n:int) -> JointPos:
        return JointPos(round(self.j1, n), round(self.j2, n), round(self.j3, n), round(self.j4, n), round(self.j5, n), round(self.j6, n))
    
    def __getitem__(self, index:int) -> float:
        return [self.j1, self.j2, self.j3, self.j4, self.j5, self.j6][index]
    
    def __setitem__(self, index:int, value:float) -> None:
        self[index] = value

    def __iter__(self):
        return iter([self.j1, self.j2, self.j3, self.j4, self.j5, self.j6])
    
    
class AbsPos:
    def __init__(self, x:float, y:float, z:float, a:float, b:float, c:float, idk1:int=6, idk2:int=0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        self.idk1 = idk1
        self.idk2 = idk2

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z},{self.a},{self.b},{self.c})({self.idk1},{self.idk2})"
    
    def __add__(self, other:AbsPos) -> AbsPos:
        return AbsPos(self.x + other.x, self.y + other.y, self.z + other.z, self.a + other.a, self.b + other.b, self.c + other.c)
    
    def __iadd__(self, other:AbsPos) -> AbsPos:
        return AbsPos(self.x + other.x, self.y + other.y, self.z + other.z, self.a + other.a, self.b + other.b, self.c + other.c)
    
    def __sub__(self, other:AbsPos) -> AbsPos:
        return AbsPos(self.x - other.x, self.y - other.y, self.z - other.z, self.a - other.a, self.b - other.b, self.c - other.c)
    
    def __isub__(self, other:AbsPos) -> AbsPos:
        return AbsPos(self.x - other.x, self.y - other.y, self.z - other.z, self.a - other.a, self.b - other.b, self.c - other.c)
    
    def __mul__(self, other:float) -> AbsPos:
        return AbsPos(self.x * other, self.y * other, self.z * other, self.a * other, self.b * other, self.c * other)
    
    def __imul__(self, other:float) -> AbsPos:
        return AbsPos(self.x * other, self.y * other, self.z * other, self.a * other, self.b * other, self.c * other)

    def __truediv__(self, other:float) -> AbsPos:
        return AbsPos(self.x / other, self.y / other, self.z / other, self.a / other, self.b / other, self.c / other)
    
    def __itruediv__(self, other:float) -> AbsPos:
        return AbsPos(self.x / other, self.y / other, self.z / other, self.a / other, self.b / other, self.c / other)
    
    def __eq__(self, other:AbsPos) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z and self.a == other.a and self.b == other.b and self.c == other.c
    
    def __ne__(self, other:AbsPos) -> bool:
        return not self == other
    
    def __format__(self, __format_spec: str) -> str:
        return f"({self.x},{self.y},{self.z},{self.a},{self.b},{self.c})"
    
    def __neg__(self) -> AbsPos:
        return AbsPos(-self.x, -self.y, -self.z, -self.a, -self.b, -self.c)
    
    def __abs__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2 + self.a**2 + self.b**2 + self.c**2)**0.5

    def __round__(self, n:int) -> AbsPos:
        return AbsPos(round(self.x, n), round(self.y, n), round(self.z, n), round(self.a, n), round(self.b, n), round(self.c, n))

    def __getitem__(self, index:int) -> float:
        return [self.x, self.y, self.z, self.a, self.b, self.c][index]
    
    def __setitem__(self, index:int, value:float) -> None:
        self[index] = value

    def __iter__(self):
        return iter([self.x, self.y, self.z, self.a, self.b, self.c])
    
