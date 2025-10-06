import math

input_coordinates = []
output_coordinates = []

class PolarCoordinate:
    def __init__(self, distance: float, angle: float):
        self.distance = distance
        self.angle = angle
    
    def __str__(self):
        return f"<PolarCoordinate, distance={self.distance:.4f}, angle={self.angle:.4f}>"

class RectangularCoordinate:
    def __init__(self, northing: float, easting: float):
        self.northing = northing
        self.easting = easting

    def __str__(self):
        return f"<RectangularCoordinate, northing={self.northing:.4f}, easting={self.easting:.4f}>"

def polar_to_rect(coord: PolarCoordinate) -> RectangularCoordinate:
    northing = coord.distance * math.cos(coord.angle)
    easting = coord.distance * math.sin(coord.angle)
    return RectangularCoordinate(northing, easting)

def rect_to_polar(coord: RectangularCoordinate) -> PolarCoordinate:
    distance = math.sqrt(coord.northing ** 2 + coord.easting ** 2)
    angle = math.atan2(coord.easting, coord.northing)
    return PolarCoordinate(distance, angle)

def transform_coordinates(input: list):
    if isinstance(input[0], PolarCoordinate):
        for i in range(0, len(input)):
            coord = polar_to_rect(input[i])
            output_coordinates.append(coord)
            print(coord)
    else:
        for i in range(0, len(input)):
            coord = rect_to_polar(input[i])
            output_coordinates.append(coord)
            print(coord)

def collect_coordinates():
    print("Hello")
    global input_coordinates
    coordinate_system = input("Enter input the coordinate system 'Rectangular | Polar': ").lower()
    input_count = int(input("Enter number of coordinates to insert: "))
    
    if coordinate_system == "polar":
        for count in range(0, input_count):
            coord = PolarCoordinate(0, 0)
            coord.distance = float(input(f"Distance ({count + 1}): "))
            coord.angle = float(input(f"Angle ({count + 1}): "))
            input_coordinates.append(coord)
    else:
        for count in range(0, input_count):
            coord = RectangularCoordinate(0, 0)
            coord.northing = float(input(f"Northing ({count + 1}): "))
            coord.easting = float(input(f"Easting ({count + 1}): "))
            input_coordinates.append(coord)
    transform_coordinates(input_coordinates)

def start():
    collect_coordinates()