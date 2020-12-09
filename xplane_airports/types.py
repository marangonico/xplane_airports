from enum import IntEnum, Enum


class RowCode(IntEnum):
    AIRPORT_HEADER		= 1
    _RUNWAY_OLD			= 10  # Legacy runway/taxiway record from X-Plane 8.10 and earlier
    TOWER_LOCATION		= 14
    STARTUP_LOCATION	= 15
    SEAPORT_HEADER		= 16
    HELIPORT_HEADER		= 17
    BEACON 				= 18
    WINDSOCK 			= 19
    FREQUENCY_AWOS 		= 50
    FREQUENCY_CTAF 		= 51
    FREQUENCY_DELIVERY 	= 52
    FREQUENCY_GROUND 	= 53
    FREQUENCY_TOWER 	= 54
    FREQUENCY_APPROACH 	= 55
    FREQUENCY_CENTER 	= 56
    FREQUENCY_UNICOM 	= 57
    FILE_END			= 99
    # These records were new with X-Plane 8.50
    TAXI_SIGN 			= 20
    PAPI_LIGHTS			= 21

    LAND_RUNWAY		= 100  # These replace the old type 10 record.
    WATER_RUNWAY	= 101
    HELIPAD 		= 102
    TAXIWAY 		= 110
    FREE_CHAIN		= 120
    BOUNDARY 		= 130

    LINE_SEGMENT	= 111
    LINE_CURVE		= 112
    RING_SEGMENT	= 113
    RING_CURVE 		= 114
    END_SEGMENT	 	= 115
    END_CURVE 		= 116

    # These records were new with X-Plane 10
    FLOW_DEFINITION	= 1000  # 1000 <traffic flow name, must be unique to the ICAO airport>
    FLOW_WIND		= 1001  # 1001 <metar icao> <wind dir min> <wind dir max> <wind max speed>
    FLOW_CEILING	= 1002  # 1002 <metar icao> <ceiling minimum>
    FLOW_VISIBILITY	= 1003  # 1003 <metar icao> <vis minimum>
    FLOW_TIME		= 1004  # 1004 <zulu time start> <zulu time end>

    CHANNEL_AWOS 		= 1050  # 8.33kHz 6-digit COM channels replacing the 50..57 records
    CHANNEL_CTAF 		= 1051
    CHANNEL_DELIVERY	= 1052
    CHANNEL_GROUND 		= 1053
    CHANNEL_TOWER 		= 1054
    CHANNEL_APPROACH	= 1055
    CHANNEL_CENTER 		= 1056
    CHANNEL_UNICOM 		= 1057

    FLOW_RUNWAY_RULE		= 1100
    FLOW_PATTERN			= 1101
    FLOW_RUNWAY_RULE_CHANNEL= 1110

    TAXI_ROUTE_HEADER	= 1200
    TAXI_ROUTE_NODE		= 1201
    TAXI_ROUTE_EDGE		= 1202
    TAXI_ROUTE_SHAPE	= 1203
    TAXI_ROUTE_HOLD		= 1204
    TAXI_ROUTE_ROAD		= 1206

    START_LOCATION_NEW	= 1300 # Replaces 15 record
    START_LOCATION_EXT	= 1301
    METADATA			= 1302

    TRUCK_PARKING		= 1400
    TRUCK_DESTINATION	= 1401

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)


class RunwayType(IntEnum):
    """Row codes used to identify different types of runways"""
    LAND_RUNWAY = RowCode.LAND_RUNWAY
    WATER_RUNWAY = RowCode.WATER_RUNWAY
    HELIPAD = RowCode.HELIPAD

    def __int__(self):
        return self.value


class SurfaceType(IntEnum):
    """codes used to identify different surface types"""
    ASPHALT = 1
    CONCRETE = 2
    TURF_GRASS = 3
    DIRT = 4
    GRAVEL = 5
    DRY_LAKEBED = 12
    WATER = 13
    SNOW_ICE = 14
    TRANSPARENT = 15

    def __int__(self):
        return self.value


class MetadataKey(Enum):
    # NOTE: These have to match the key names in WED_MetaDataKeys.cpp
    CITY = 'city'
    COUNTRY = 'country'
    DATUM_LAT = 'datum_lat'
    DATUM_LON = 'datum_lon'
    FAA_CODE = 'faa_code'
    LABEL_3D_OR_2D = 'gui_label'
    IATA_CODE = 'iata_code'
    ICAO_CODE = 'icao_code'
    LOCAL_CODE = 'local_code'
    LOCAL_AUTHORITY = 'local_authority'
    REGION_CODE = 'region_code'
    STATE = 'state'
    TRANSITION_ALT = 'transition_alt'
    TRANSITION_LEVEL = 'transition_level'
