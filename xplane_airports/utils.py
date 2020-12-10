def get_lat_lon_center(lat_1: float, lon_1: float, lat_2: float, lon_2: float) -> float:
    """
    :param rwy: Runway line
    :param start: index of the start coordinate in the tokens property of the runway
    :param end: index of the end coordinate in the tokens property of the runway
    :returns: Runway center
    """
    return 0.5 * (lat_1 + lat_2), 0.5 * (lon_1 + lon_2)
