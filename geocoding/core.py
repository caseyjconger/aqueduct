###############################################################################
###############################################################################
##                                                                           ##
##  core.py                                                                  ##
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
import os

from geopy.geocoders import GoogleV3
from shapely import Point

###############################################################################
## CONSTANTS ##################################################################
###############################################################################

#TODO: move this to a configuration file
GOOGLE_GEOCODE_API_KEY = 'AIzaSyAnM0TuA8nP9NUUfCeqb-JBjk93eD2Bdlw'
GDBS = {
    'aqueduct_global': os.path.join(
        os.getcwd(), 'data/aqueduct_global/aqueduct_global_dl_20150409.gdb'
    )
}
GDB_LAYERS = {
    'aqueduct_global': 'global_master_20150409'
}


###############################################################################
## HELPER FUNCTIONS ###########################################################
###############################################################################

def get_gu(pt, df):
    """This function maps from a location to a GU (unique identifier in the
    geodatbase. Intention is to be used in a pandas .apply()

    Arguments:
      + pt (shapely.Point)[]: this is a shapely Point object representing
          a geographic location parametrized as (longitude, latitude)
      + df (geopandas.geodataframe)[]: this is a geodatabase containing the
          regions, parametrized as shapely.Polygons enclosing a region of
          interest
    Returns:
      + gu (np.array): returns a numpy array of matching GUs corresponding
          to regions which enclose the given point, pt.
    """
    return df[df['geometry'].contains(pt)]['GU'].values

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
      + loc (dict): a dictionary containing the geolocation data
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
        loc.update({'addr': location.address})
        return loc
    elif return_level == 2:
        loc = location.raw
        return loc


###############################################################################
## LOAD GEODATABASE ###########################################################
###############################################################################

def load_GDB(gdb_path, layer=None, df_processor=None):
    """This function loads the geodatabse into a geopandas geodataframe.

    Arguments:
      + gdb_path (str)[]: string containing the path to the geodatabase to be
          loaded
      + layer (str)[None]: string containing the layer to be loaded. Defaults
          to None to make it an optional parameter in the case that there is
          only one layer.
      + df_processor (func)[None]: an optional function to perform some
          processing on the dataframe before it is returned.

    Returns:
      + df (geodataframe): geodataframe downloaded from the water resource
          institute website.
    """
    df = geopandas.read_file(gdb_path, layer=layer)
    if df_processor is not None:
        df = df_processor(df)
    return df

###############################################################################
## JOIN LOCATION AND GEODATABASE ##############################################
###############################################################################




###############################################################################
## MAIN #######################################################################
###############################################################################

def main():
    addr = '386 Park Avenue South, New York NY'
    for ii in range(0,3):
        location = address_to_loc(addr, return_level=ii)
        print('Level {}:\n{}\n'.format(ii, location))
    df = load_GDB(GDBS['aqueduct_global'], GDB_LAYERS['aqueduct_global'])


if __name__ == '__main__':
    main()
