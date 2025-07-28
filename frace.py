import ezdxf
import logging as log
from typing import TypeAlias
import turtle
import math

#region config
filePath = "MODELSKETCH_VISIBLE.dxf"
loggingLevel = log.DEBUG
#endregion

log.basicConfig(level=loggingLevel)

#region DXFclasses
point: TypeAlias = tuple[float, float]
pointPair: TypeAlias = tuple[point, point]


class DXFclass:
    def __init__(self) -> None:
        pass
    
    def bounds(self) -> pointPair:
        raise ImportError

class Line(DXFclass):
    def __init__(self, startcords:point, endcords:point) -> None:
        self.start = (startcords[0], startcords[1])
        self.end = (endcords[0], endcords[1])
        self.reverse = False
    
    def bounds(self) -> pointPair:
        minX = min(self.start[0], self.end[0])
        maxX = max(self.start[0], self.end[0])
        minY = min(self.start[1], self.end[1])
        maxY = max(self.start[1], self.end[1])
        
        return ((minX, minY),(maxX,maxY))
    
class Circle(DXFclass):
    def __init__(self, center:point, radius:float) -> None:
        self.center = (center[0], center[1])
        self.radius = radius
        
    def bounds(self) -> pointPair:
        minX = self.center[0] - self.radius
        maxX = self.center[0] + self.radius
        minY = self.center[1] - self.radius
        maxY = self.center[1] + self.radius
        
        return ((minX, minY),(maxX,maxY))
    
class Arc(DXFclass):
    def __init__(self, center:point, radius:float, startAngle:float, endAngle:float) -> None:
        self.center = (center[0], center[1])
        self.radius = radius
        
    def bounds(self) -> pointPair:
        #TODO: Bounds echt maken, nu pakt hij gwn de cirkel
        minX = self.center[0] - self.radius
        maxX = self.center[0] + self.radius
        minY = self.center[1] - self.radius
        maxY = self.center[1] + self.radius
        
        return ((minX, minY),(maxX,maxY))

#endregion

Elements = []

#region  DXFreading

# Read the DXF file
log.info(f"Reading {filePath}")
doc = ezdxf.readfile(filePath)

log.info(f"\nFound the following items:")
# Iterate through the entities in the modelspace
for entity in doc.modelspace().query('*'):
    if entity.dxftype() == 'LINE':
        log.info(f"Line from {entity.dxf.start} to {entity.dxf.end}")
        log.info(entity.dxf.all_existing_dxf_attribs())
        Elements.append(
            Line(entity.dxf.start, entity.dxf.end)
        )
    
    elif entity.dxftype() == 'CIRCLE':
        log.info(f"Circle at {entity.dxf.center} with radius {entity.dxf.radius}")
        log.info(entity.dxf.all_existing_dxf_attribs())
        Elements.append(
            Circle(entity.dxf.center, entity.dxf.radius)
        )
        
    elif entity.dxftype() == 'ARC':
        log.info(f"Arc at {entity.dxf.center} with radius {entity.dxf.radius}, start angle {entity.dxf.start_angle}, end angle {entity.dxf.end_angle}")
        log.info(entity.dxf.all_existing_dxf_attribs())
        Elements.append(
            Arc(entity.dxf.center, entity.dxf.radius, entity.dxf.start_angle, entity.dxf.end_angle)
        )
        
        
    else:
        log.warning(f"Unknown Entity type: {entity.dxftype()} with data: {entity.dxf}")

#endregion

#region optimalisation

#TODO: ook laten werken voor arcs en cirkels
UnsortedElements: list[DXFclass] = Elements
SortedElements: list[DXFclass] = []
lastPosition: point = (0,0)

while len(UnsortedElements) > 0:
    minDistance = 99999999
    minElement = UnsortedElements[0]
    revert = False
    for UnsortedElement in UnsortedElements:
        if isinstance(UnsortedElement, Line):
            UnsortedElement.reverse = False
            
            distance1 = math.sqrt(((lastPosition[0]-UnsortedElement.end[0])**2)+((lastPosition[1]-UnsortedElement.end[1])**2)+0.000000001)
            distance2 = math.sqrt(((lastPosition[0]-UnsortedElement.start[0])**2)+((lastPosition[1]-UnsortedElement.start[1])**2)+0.000000001)
            distance = min(distance1, distance2)
            
            if distance == distance1:
                UnsortedElement.reverse = True
            
        elif isinstance(UnsortedElement, Circle):
            distance  = math.sqrt(((lastPosition[0]-UnsortedElement.center[0])**2)+((lastPosition[1]-UnsortedElement.center[1])**2)+0.000000001)
        elif isinstance(UnsortedElement, Arc):
            distance  = math.sqrt(((lastPosition[0]-UnsortedElement.center[0])**2)+((lastPosition[1]-UnsortedElement.center[1])**2)+0.000000001)
        else:
            distance = 9999999
            
        if distance < minDistance:
            minDistance = distance
            minElement = UnsortedElement
            
            
    SortedElements.append(minElement)
    UnsortedElements.remove(minElement)
    
    if isinstance(minElement, Line):
        if minElement.reverse == True:
            end = minElement.start
            start = minElement.end
            minElement.end = end
            minElement.start = start
            minElement.reverse = False
    
Elements = SortedElements

#endregion

#region TurtleSimulation
turtle.setworldcoordinates(-10, -10, 10, 10)

def turtleUp():
    turtle.color(1, 0, 0)
    turtle.width(1)
    
def turtleDown():
    turtle.color(0, 0, 0)
    turtle.width(3)

for element in Elements:
    if isinstance(element, Line):
        turtleUp()
        turtle.setpos(element.start)
        turtleDown()
        turtle.setpos(element.end)
        turtleUp()
        
    if isinstance(element, Circle):
        turtleUp()
        turtle.setpos((element.center[0], element.center[1] - element.radius))
        turtleDown()
        turtle.circle(element.radius)
        turtleUp()
        
    if isinstance(element, Arc):
        log.error("Arc not implemented")
        
turtle.mainloop()
#endregion
