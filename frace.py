import ezdxf
import ezdxf.units
import ezdxf.enums
import logging as log
from typing import TypeAlias
import turtle
import math
from gerrard import *
import time

#region config
filePath = "VierkantMetRondjeEnPunt.dxf"
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

dxfScale = doc.header.get('$INSUNITS', ezdxf.enums.InsertUnits.Millimeters)  # Default to 1 if not specified
log.info(f"DXF scale is {dxfScale}, which corresponds to unit: {ezdxf.units.unit_name(dxfScale)}")
log.info(ezdxf.enums.InsertUnits(dxfScale))
unitConversion  = ezdxf.units.conversion_factor(ezdxf.enums.InsertUnits(dxfScale), ezdxf.enums.InsertUnits.Millimeters) * 10 # Convert to mm

log.info(f"DXF scale is set to {dxfScale}, which corresponds to unit: {doc.header.get('$INSUNITS', 'unknown')}")
log.info(f"Unit conversion factor to millimeters is {unitConversion}")

log.info(f"\nFound the following items:")
# Iterate through the entities in the modelspace
for entity in doc.modelspace().query('*'):
    if entity.dxftype() == 'LINE':
        log.info(f"Line from {entity.dxf.start} to {entity.dxf.end}")
        log.debug(entity.dxf.all_existing_dxf_attribs())

        # Convert coordinates to millimeters
        start = (entity.dxf.start.x * unitConversion, entity.dxf.start.y * unitConversion)
        end = (entity.dxf.end.x * unitConversion, entity.dxf.end.y * unitConversion)
        Elements.append(
            Line(start, end)
        )
    
    elif entity.dxftype() == 'CIRCLE':
        log.info(f"Circle at {entity.dxf.center} with radius {entity.dxf.radius}")
        log.debug(entity.dxf.all_existing_dxf_attribs())
        # Convert coordinates to millimeters
        center = (entity.dxf.center.x * unitConversion, entity.dxf.center.y * unitConversion)
        radius = entity.dxf.radius * unitConversion  # Convert radius to millimeters
        Elements.append(
            Circle(center, radius)
        )
        
    elif entity.dxftype() == 'ARC':
        log.info(f"Arc at {entity.dxf.center} with radius {entity.dxf.radius}, start angle {entity.dxf.start_angle}, end angle {entity.dxf.end_angle}")
        log.debug(entity.dxf.all_existing_dxf_attribs())
        # Convert coordinates to millimeters
        center = (entity.dxf.center.x * unitConversion, entity.dxf.center.y * unitConversion)
        radius = entity.dxf.radius * unitConversion  # Convert radius to millimeters
        Elements.append(
            Arc(center, radius, entity.dxf.start_angle, entity.dxf.end_angle)
        )
    elif entity.dxftype() == 'LWPOLYLINE':
        vertices = list(entity.get_points())
        log.info(f"Polyline with {len(vertices)} vertices")
        log.debug(entity.dxf.all_existing_dxf_attribs())
        # Convert coordinates to millimeters
        vertices = [(v[0] * unitConversion, v[1] * unitConversion, v[2] * unitConversion) for v in vertices]
        Elements.append(entity)
        log.info(f"Converted vertices: {vertices}")

        # Create line segments between consecutive vertices
        for i in range(len(vertices) - 1):
            start_vertex = vertices[i][:2]  # Take only x, y coordinates
            end_vertex = vertices[i + 1][:2]  # Take only x, y coordinates
            Elements.append(Line(start_vertex, end_vertex))

        # Handle closed polylines
        if entity.closed:
            start_vertex = vertices[-1][:2]
            end_vertex = vertices[0][:2]
            Elements.append(Line(start_vertex, end_vertex))

    else:
        log.warning(f"Unknown Entity type: {entity.dxftype()} with data: {entity.dxf}")

#endregion

#region centering

centeredElements: list[DXFclass] = []

minX = min(element.bounds()[0][0] for element in Elements)
maxX = max(element.bounds()[1][0] for element in Elements)
minY = min(element.bounds()[0][1] for element in Elements)
maxY = max(element.bounds()[1][1] for element in Elements)

# goal: minX = maxX and minY = maxY
centerX = (minX + maxX) / 2
centerY = (minY + maxY) / 2

for element in Elements:
    if isinstance(element, Line):
        # Center the line by adjusting start and end points
        new_start = (element.start[0] - centerX, element.start[1] - centerY)
        new_end = (element.end[0] - centerX, element.end[1] - centerY)
        centeredElements.append(Line(new_start, new_end))
        
    elif isinstance(element, Circle):
        # Center the circle by adjusting its center
        new_center = (element.center[0] - centerX, element.center[1] - centerY)
        centeredElements.append(Circle(new_center, element.radius))
        
    elif isinstance(element, Arc):
        # Center the arc by adjusting its center
        new_center = (element.center[0] - centerX, element.center[1] - centerY)
        centeredElements.append(Arc(new_center, element.radius, element.startAngle, element.endAngle))
        
    else:
        log.warning(f"Unknown Element type: {type(element)}")
        
Elements = centeredElements

#endregion centering

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
            log.debug(f"Distance to {UnsortedElement} is {distance} (start: {distance1}, end: {distance2})")
            
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
            
        lastPosition = minElement.end
    elif isinstance(minElement, Circle):
        lastPosition = minElement.center
    elif isinstance(minElement, Arc):
        lastPosition = minElement.center
    
Elements = SortedElements

#endregion

#region TurtleSimulation
turtle.setup(width=800, height=800)
turtle.setworldcoordinates(-100, -100, 100, 100)

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

#region Frace
log.debug("Setting up fracing parameters...")
fraceSpeed = 0.5
notFraceSpeed = 20
zeroPosition = AbsPos(570,0,312.5,180,0,180) # 420
upvector = AbsPos(0,0,-83,0,0,0)
downvector = AbsPos(0,0,-105,0,0,0)
bounds:pointPair = (
    (
        min(element.bounds()[0][0] for element in Elements),
        min(element.bounds()[0][1] for element in Elements)
    ),
    (
        max(element.bounds()[1][0] for element in Elements),
        max(element.bounds()[1][1] for element in Elements)
    )
)
log.debug(f"Bounds: {bounds}")

robotBoundCorners: tuple[AbsPos, AbsPos, AbsPos, AbsPos] = (
    AbsPos(bounds[0][0], bounds[0][1], 0, 0, 0, 0),
    AbsPos(bounds[1][0], bounds[0][1], 0, 0, 0, 0),
    AbsPos(bounds[1][0], bounds[1][1], 0, 0, 0, 0),
    AbsPos(bounds[0][0], bounds[1][1], 0, 0, 0, 0)
)

log.debug(f"Robot bound corners: {robotBoundCorners}")

log.debug("Setting up robot arm...")
arm = Robot(
    port="/dev/ttyUSB0"
)
log.debug(f"Connecting to robot...")
arm.connect()

with arm:
    #ARM setup
    arm.end()
    arm.resetError()
    arm.overrideSpeed(notFraceSpeed)
    arm.executeCommand("SPD M_NSPD", True)
    arm.setVariable("HOME", zeroPosition + upvector)
    arm.setVariable("ZERO", zeroPosition)
    arm.servoOn()
    time.sleep(1.5)
    
    arm.moveTo("HOME", True, "P")
    input("Press Enter to show bounds...")
    
    # Show bounds
    for corner in robotBoundCorners:
        arm.setVariable("Corner", corner + zeroPosition + upvector)
        log.debug(f"Moving to corner: {corner + zeroPosition + upvector}")
        arm.moveTo("Corner", True, "P")
        time.sleep(2)
        
    arm.moveTo("HOME", True, "P")
        
    input("Press Enter to start fracing...")
    
    lastPosition:AbsPos = zeroPosition
    
    for element in Elements:
        if isinstance(element, Line):
            start = AbsPos(element.start[0], element.start[1], 0, 0, 0, 0)
            end = AbsPos(element.end[0], element.end[1], 0, 0, 0, 0)

            if lastPosition != start:
                log.info(f"Not at correct position, moving up and then to start position: {start} from {lastPosition}")
                log.debug(f"Moving to last position: {lastPosition + upvector}")
                arm.setVariable("Up", lastPosition + upvector)
                time.sleep(0.2)
                log.debug(f"Moving up")
                arm.moveTo("Up", True, "P")
                time.sleep(4)
                arm.overrideSpeed(notFraceSpeed)
                arm.setVariable("StartUp", start + zeroPosition + upvector)
                time.sleep(0.2)
                arm.moveTo("StartUp", True, "P")
                time.sleep(1)
            
                arm.overrideSpeed(fraceSpeed)
                log.debug(f"Moving down")
                arm.setVariable("P1", start + zeroPosition + downvector)
                arm.moveTo("P1", True, "P")
                time.sleep(3)

            log.debug(f"Moving to end position: {end}, {end + zeroPosition + downvector}")
            arm.setVariable("P2", end + zeroPosition + downvector)
            arm.moveTo("P2", True, "P")
            time.sleep(20)
            
            lastPosition = end + zeroPosition
            
            
        elif isinstance(element, Circle):
            center = AbsPos(element.center[0], element.center[1], 0, 0, 0, 0)
            radius = element.radius
            
            startPosition = center + AbsPos(radius, 0, 0, 0, 0, 0)

            points = []
            for i in range(3):
                angle = 2 * math.pi * i / 3  # Divide the circle into three equal parts
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                points.append(AbsPos(x, y, 0, 0, 0, 0))

            log.info(f"Processing Circle at {center} with radius {radius}")
            start = points[0]
            mid = points[1]
            end = points[2]
            log.info(f"Start: {start}, Mid: {mid}, End: {end}")

            if lastPosition != start:
                log.info(f"Not at correct position, moving up and then to start position: {start} from {lastPosition}")
                log.debug(f"Moving to last position: {lastPosition + upvector}")
                arm.setVariable("Up", lastPosition + upvector)
                time.sleep(0.2)
                log.debug(f"Moving up")
                arm.moveTo("Up", True, "P")
                time.sleep(3)
                arm.overrideSpeed(notFraceSpeed)
                arm.setVariable("StartUp", start + zeroPosition + upvector)
                time.sleep(0.2)
                arm.moveTo("StartUp", True, "P")
                time.sleep(1)
            

            arm.setVariable("L1", start + zeroPosition + downvector)
            time.sleep(0.2)
            arm.setVariable("LU1", start + zeroPosition + upvector)
            time.sleep(0.2)
            arm.setVariable("L2", mid + zeroPosition + downvector)
            time.sleep(0.2)
            arm.setVariable("LU2", mid + zeroPosition + upvector)
            time.sleep(0.2)
            arm.setVariable("L3", end + zeroPosition + downvector)
            time.sleep(0.2)
            arm.setVariable("LU3", end + zeroPosition + upvector)
            time.sleep(0.2)

            arm.overrideSpeed(fraceSpeed)
            arm.moveLinearTo("L1", True, "P")
            time.sleep(5)

            arm.executeCommand(f"MVC PL1, PL2, PL3", True)
            print("Moving in circle")
            time.sleep(30)

            lastPosition = start + zeroPosition

    log.info(f"Moving home after fracing")
    log.debug(f"Moving to last position: {lastPosition + upvector}")
    arm.setVariable("Up", lastPosition + upvector)
    time.sleep(0.2)
    log.debug(f"Moving up")
    arm.moveTo("Up", True, "P")
    time.sleep(5)
    arm.overrideSpeed(notFraceSpeed)
    
    arm.moveTo("HOME", True, "P")
    time.sleep(1)

    arm.servoOff()
    arm.end()
    arm.resetError()
    log.info("Fracing completed successfully.")
    log.info("Robot disconnected.")
#endregion