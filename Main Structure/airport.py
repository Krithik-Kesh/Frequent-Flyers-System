"""Defines Airport Class"""
from typing import Tuple


class Airport:
    """ An ADT representing international airports and their locations on a map

    === Public Attributes ===
    name:
        this is the name of the airport.

    >>> toronto = Airport("YYZ", "Lester B. Pearson International Airport", \
    (-79.63059998, 43.67720032))
    >>> toronto.get_airport_id() == "YYZ"
    True
    >>> toronto.get_location() == (-79.63059998, 43.67720032)
    True
    """
    # === Private Attributes ===
    # _airport_id:
    #     this is a unique 3-character airport identifier (i.e. the IATA
    #     location identifier; e.g. Toronto Pearson is "YYZ").
    #
    # _map_location:
    #     this is a tuple containing the longitude and latitude of
    #     the airport's coordinates on the world map.

    name: str
    _airport_id: str
    _map_location: Tuple[float, float]

    def __init__(self, aid: str, name: str,
                 location: Tuple[float, float]) -> None:
        """ Initialize a new Airport object with the given parameters. """

        self.name = name
        self._airport_id = aid
        self._map_location = location

    def get_airport_id(self) -> str:
        """ Returns the unique IATA location identifier for this airport. """

        return self._airport_id

    def get_name(self) -> str:
        """ Returns the airport's name. """

        return self.name

    def get_location(self) -> Tuple[float, float]:
        """ Returns the airport's location <longitude, latitude>. """

        return self._map_location


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'doctest'
        ]
    })
