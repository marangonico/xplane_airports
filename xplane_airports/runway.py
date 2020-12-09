from contextlib import suppress
from typing import List

from xplane_airports.aptdat_line import AptDatLine
from xplane_airports.types import RunwayType, SurfaceType


class RunwayEnd(object):
    number: str
    lat = float
    lon = float
    displaced_threshold = float

    def __init__(self, runway, rwy_end_values: List):
        if runway.runway_type == RunwayType.LAND_RUNWAY:
            self.parse_land(rwy_end_values)
        elif runway.runway_type == RunwayType.WATER_RUNWAY:
            self.parse_water(rwy_end_values)

    def parse_land(self, rwy_end_values):
        self.number = rwy_end_values[0]
        self.lat = float(rwy_end_values[1])
        self.lon = float(rwy_end_values[2])
        self.displaced_threshold = float(rwy_end_values[3])

    def parse_water(self, rwy_end_values):
        self.number = rwy_end_values[0]
        self.lat = float(rwy_end_values[1])
        self.lon = float(rwy_end_values[2])


class Runway:

    runway_type: RunwayType
    designator: str
    width: float
    surface_type: SurfaceType
    shoulder_type: int
    runway_ends = List[RunwayEnd]
    lat: float  # rwy center
    lon: float  # rwy center

    def __init__(self, aptdat_line: AptDatLine):
        self.aptdat_line_values = aptdat_line.raw.split()
        self.runway_type = RunwayType(int(self.aptdat_line_values[0]))
        if self.runway_type == RunwayType.LAND_RUNWAY:
            self.parse_land()
        elif self.runway_type == RunwayType.WATER_RUNWAY:
            self.parse_water()
        elif self.runway_type == RunwayType.HELIPAD:
            self.parse_helipad()

    def parse_land(self):
        self.width = float(self.aptdat_line_values[1])
        self.surface_type = SurfaceType(int(self.aptdat_line_values[2]))
        self.shoulder_type = int(self.aptdat_line_values[3])
        self.load_rwy_ends(self.aptdat_line_values[8:17], self.aptdat_line_values[17:])

    def parse_water(self):
        self.width = float(self.aptdat_line_values[1])
        self.surface_type = SurfaceType.WATER
        self.load_rwy_ends(self.aptdat_line_values[3:6], self.aptdat_line_values[6:])

    def parse_helipad(self):
        self.designator = self.aptdat_line_values[1]
        self.lat = float(self.aptdat_line_values[2])
        self.lon = float(self.aptdat_line_values[3])
        self.surface_type = SurfaceType(int(self.aptdat_line_values[7]))

    def load_rwy_ends(self, rwy_end_values_1, rwy_end_values_2):
        self.runway_ends = []
        self.runway_ends.append(RunwayEnd(self, rwy_end_values_1))
        self.runway_ends.append(RunwayEnd(self, rwy_end_values_2))
