from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import List, Dict, Union, Iterable, Optional

from xplane_airports.aptdat_line import AptDatLine
from xplane_airports.globals import WED_LINE_ENDING
from xplane_airports.runway import Runway, RunwayLand, RunwayWater, RunwayHelipad
from xplane_airports.types import MetadataKey, RowCode, RunwayType


@dataclass
class Airport:
    """A single airport from an apt.dat file."""
    name: str                     # The name of the airport, like "Seattle-Tacoma Intl"
    id: str                       # The X-Plane identifier for the airport, which may or may not correspond to its ICAO ID
    from_file: Path = Path()      # Path to the apt.dat file from which this airport was read
    has_atc: bool = False         # True if the airport header indicates the airport has air traffic control
    elevation_ft_amsl: float = 0  # The elevation, in feat above mean sea level, indicated in the airport header line
    metadata: Dict[MetadataKey, str] = field(default_factory=dict)  # Metadata about the airport
    text: List[AptDatLine] = field(default_factory=list)  # The complete text of the portion of the apt.dat file pertaining to this airport
    xplane_version: int = 1100    # The version of X-Plane apt.dat spec (1050, 1100, 1130, etc.) used by the airport
    runways: List[Runway] = field(default_factory=list)

    def __init__(self, header_lines, lines, xplane_version='', from_file=''):

        self.id = header_lines[0].tokens[4]
        self.name = ' '.join(header_lines[0].tokens[5:])
        self.elevation_ft_amsl = float(header_lines[0].tokens[1])
        self.has_atc = bool(int(header_lines[0].tokens[2]))  # '0' or '1'
        self.metadata = self.parse_metadata(lines)
        self.text = lines

        self.xplane_version = xplane_version
        self.from_file = from_file

        self.load_runways()

    def load_runways(self):

        self.runways = []
        for aptdat_line in list(line for line in self.text if line.is_runway()):

            if aptdat_line.runway_type == RunwayType.LAND_RUNWAY:
                runway_class = RunwayLand
            elif aptdat_line.runway_type == RunwayType.WATER_RUNWAY:
                runway_class = RunwayWater
            elif aptdat_line.runway_type == RunwayType.HELIPAD:
                runway_class = RunwayHelipad

            self.runways.append(runway_class(aptdat_line))

    def __bool__(self):
        return bool(self.id)

    def __str__(self):
        return WED_LINE_ENDING.join(line.raw for line in self.text
                                    # Fix parsing errors in X-Plane: If a metadata key has no value, it needs to be excluded from the apt.dat!
                                    if line.row_code != RowCode.METADATA or len(line.tokens) > 2)

    def head(self, num_lines: int=10) -> str:
        """
        :param num_lines: The max number of lines to return
        :return: The first `num_lines` of the apt.dat text for this airport
        """
        return WED_LINE_ENDING.join(line.raw for i, line in enumerate(self.text) if i < num_lines)

    def write_to_disk(self, path_to_write_to: Optional[PathLike]):
        """
        Writes a complete apt.dat file containing only this airport
        :param path_to_write_to: A complete file path (ending in .dat); if None, we'll use the path this airport came from
        """
        if not path_to_write_to:
            path_to_write_to = self.from_file
        assert str(path_to_write_to).endswith('.dat')
        with open(str(path_to_write_to), 'w') as f:
            f.write("I" + WED_LINE_ENDING)
            f.write(f"{self.xplane_version} Generated by WorldEditor{WED_LINE_ENDING}{WED_LINE_ENDING}")
            f.write(str(self))
            f.write(str(RowCode.FILE_END) + WED_LINE_ENDING)

    @property
    def has_taxiway(self) -> bool:
        """
        :returns: True if this airport defines any taxiway geometry
        """
        return self.has_row_code([RowCode.RING_SEGMENT, RowCode.RING_CURVE])

    @property
    def has_taxi_route(self) -> bool:
        """
        :returns: True if this airport defines routing rules for ATC's use of its taxiways.
        """
        return self.has_row_code(RowCode.TAXI_ROUTE_HEADER)

    @property
    def has_traffic_flow(self) -> bool:
        """
        :returns: True if this airport defines rules for when and under what conditions certain runways should be used by ATC
        """
        return self.has_row_code(RowCode.FLOW_DEFINITION)

    @property
    def has_ground_routes(self) -> bool:
        """
        :returns: True if this airport defines any destinations for ground vehicles (like baggage cars, fuel trucks, etc.), ground truck parking locations, or taxi routes
        """
        return self.has_row_code([RowCode.TRUCK_PARKING, RowCode.TRUCK_DESTINATION, RowCode.TAXI_ROUTE_HEADER])

    @property
    def has_taxiway_sign(self) -> bool:
        """
        :returns: True if this airport defines any taxi signs
        """
        return self.has_row_code(RowCode.TAXI_SIGN)

    @property
    def has_comm_freq(self) -> bool:
        """
        :returns: True if this airport defines communication radio frequencies for interacting with ATC
        """
        return self.has_row_code([RowCode.FREQUENCY_AWOS, RowCode.FREQUENCY_CTAF, RowCode.FREQUENCY_DELIVERY, RowCode.FREQUENCY_GROUND, RowCode.FREQUENCY_TOWER, RowCode.FREQUENCY_APPROACH, RowCode.FREQUENCY_CENTER])

    def has_row_code(self, row_code_or_codes: Union[int, str, Iterable[int]]) -> bool:
        """
        :param row_code_or_codes: One or more "row codes" (the first token at the beginning of a line; almost always int)
        :returns: True if the airport has any lines in its text that begin with the specified row code(s)
        """
        if isinstance(row_code_or_codes, int) or isinstance(row_code_or_codes, str):
            return any(line for line in self.text if line.row_code == row_code_or_codes)
        return any(line for line in self.text if line.row_code in row_code_or_codes)

    @staticmethod
    def _rwy_center(rwy: AptDatLine, start: int, end: int) -> float:
        """
        :param rwy: Runway line
        :param start: index of the start coordinate in the tokens property of the runway
        :param end: index of the end coordinate in the tokens property of the runway
        :returns: Runway center
        """
        assert isinstance(rwy, AptDatLine)
        return 0.5 * (float(rwy.tokens[start]) + float(rwy.tokens[end]))

    # def runways(self):
    #     for runway in list(line for line in self.text if line.is_runway()):
    #         yield runway

    @property
    def latitude(self) -> float:
        """
        :returns: The latitude of the airport, which X-Plane calculates as the latitude of the center of the first runway.
        """
        runways = list(line for line in self.text if line.is_runway())
        assert runways, "Airport appears to have no runway lines"
        rwy_0 = runways[0]
        if rwy_0.runway_type == RunwayType.LAND_RUNWAY:
            return Airport._rwy_center(rwy_0, 9, 18)
        elif rwy_0.runway_type == RunwayType.WATER_RUNWAY:
            return Airport._rwy_center(rwy_0, 4, 7)
        elif rwy_0.runway_type == RunwayType.HELIPAD:
            return float(rwy_0.tokens[2])

    @property
    def longitude(self) -> float:
        """
        :returns: The longitude of the airport, which X-Plane calculates as the longitude of the center of the first runway.
        """
        runways = list(line for line in self.text if line.is_runway())
        assert runways, "Airport appears to have no runway lines"
        rwy_0 = runways[0]
        if rwy_0.runway_type == RunwayType.LAND_RUNWAY:
            return Airport._rwy_center(rwy_0, 10, 19)
        elif rwy_0.runway_type == RunwayType.WATER_RUNWAY:
            return Airport._rwy_center(rwy_0, 5, 8)
        elif rwy_0.runway_type == RunwayType.HELIPAD:
            return float(rwy_0.tokens[3])

    @staticmethod
    def parse_metadata(apt_lines: List[AptDatLine]) -> Dict[MetadataKey, str]:
        out = {}
        for line in apt_lines:
            if line.row_code == RowCode.METADATA:
                try:
                    val = ' '.join(line.tokens[2:])
                    if val:
                        out[MetadataKey(line.tokens[1])] = val
                except:
                    pass
        return out

    @staticmethod
    def from_lines(
            dat_lines: Iterable[Union[str, AptDatLine]],
            from_file_name: Optional[Path] = None,
            xplane_version: int = 1100) -> 'Airport':
        """
        :param dat_lines: The lines of the apt.dat file (either strings or parsed AptDatLine objects)
        :param from_file_name: The name of the apt.dat file you read this airport in from
        :param xplane_version: The version of the apt.dat spec this airport uses (1050, 1100, 1130, etc.)
        """
        lines = list(line if isinstance(line, AptDatLine) else AptDatLine(line) for line in dat_lines)
        header_lines = list(line for line in lines if line.is_airport_header())
        assert len(header_lines), f"Failed to find an airport header line in airport from file {from_file_name}"
        assert len(header_lines) == 1, f"Expected only one airport header line in airport from file {from_file_name}"
        return Airport(
            header_lines, lines, xplane_version=xplane_version, from_file=from_file_name if from_file_name else Path())

    @staticmethod
    def from_str(file_text: str, from_file_name: Optional[PathLike] = None, xplane_version: int = 1100) -> 'Airport':
        """
        :param file_text: The portion of the apt.dat file text that specifies this airport
        :param from_file_name: The name of the apt.dat file you read this airport in from
        """
        return Airport.from_lines((AptDatLine(line) for line in file_text.splitlines()), from_file_name, xplane_version)
