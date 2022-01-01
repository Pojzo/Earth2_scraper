class Property:
    def __init__(self, name_: str, net_worth_: float, coordinates_: tuple[float, float], location_: str):
        """
            @name: name of property
            @net_worth: net worth of property 
            @coordinates: coordinates of property, (latitude, longitude)
            @location: precise location with country name as specified in the profile
        """
        self.name = name_
        self.net_worth = net_worth_
        self.coordinates = coordinates_
        self.location = location_
