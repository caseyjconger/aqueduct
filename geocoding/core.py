###############################################################################
###############################################################################
##                                                                           ##
##  water_resource.py                                                        ##
##  Date Created: 2018/12/12                                                 ##
##                                                                           ##
##  This module contains a collection of functions for connecting business   ##
##  addresses to their geolocations (latitude & longitude) and then          ##
##  connecting that to various data sets fromt the water resource institure  ##
##                                                                           ##
###############################################################################
###############################################################################

import geopandas
import fiona
from geopy.geocoders import GoogleV3

###############################################################################
## CONSTANTS ##################################################################
###############################################################################

#TODO: move this to a configuration file
GOOGLE_GEOCODE_API_KEY = 'AIzaSyAnM0TuA8nP9NUUfCeqb-JBjk93eD2Bdlw'

###############################################################################
## ADDRESS TO LAT/LONG ########################################################
###############################################################################

def address_to_loc(addr, api_key=GOOGLE_GEOCODE_API_KEY, return_level=0):
    """This function takes in an address and maps it to a lattitude/longitude.

    Arguments:
      + addr (str)[]: address to map to location
      + api_key (str)[GOOGLE_GEOCODE_API_KEY]: a string containing the google
          geocoder API key
      + return_level (int)[0]: an integer encoding the level of detail
          included in the returned data.
            0 -> Only latitude and longitude
            1 -> Latitude, Longitude, and formatted address used
            2 -> {WARNING} Raw return data dictionary format not compatible
                   with levels 0 and 1

    Returns:
      + loc (tuple): a tuple of floats representing the geolocation
    """
    _valid_return_levels = [0, 1, 2]
    assert (return_level in _valid_return_levels), \
            'return_level must be a positive integer less than {}'.format(
                max(_valid_return_levels) + 1
            )

    geolocator = GoogleV3(GOOGLE_GEOCODE_API_KEY)
    location = geolocator.geocode(addr)

    loc = {
        'lat': location.latitude,
        'long': location.longitude
    }

    if return_level == 0:
        return loc
    elif return_level == 1:
        loc['addr'] = loc.address
        return loc
    elif return_level == 2:
        loc = location.raw
        return loc



###############################################################################
## MAIN #######################################################################
###############################################################################

def main():
    print()

if __name__ == '__main__':
    main
