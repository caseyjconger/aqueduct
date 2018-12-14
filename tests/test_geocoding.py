###############################################################################
###############################################################################
##                                                                           ##
##  test_geocoding.py                                                        ##
##  Date Created: 2018/12/13                                                 ##
##                                                                           ##
##  This set of unit tests is used to ensure the functionality of the        ##
##  geocoding module.                                                        ##
##                                                                           ##
###############################################################################
###############################################################################

from .context import geocoding
from geopy.geocoders import GoogleV3

def test_api_key_exists():
    assert geocoding.core.GOOGLE_GEOCODE_API_KEY is not None

def test_api_connection():
    addr = '386 Park Avenue South, New York, NY 10016'
    api_key = geocoding.core.GOOGLE_GEOCODE_API_KEY
    geolocator = GoogleV3(api_key)
    location = geolocator.geocode(addr)
    assert location is not None

def test_address_format():
    addr = '386 Park Avenue South, New York, NY'
    ret_addr = '386 Park Avenue South, Park Ave S, New York, NY 10016, USA'
    api_key = geocoding.core.GOOGLE_GEOCODE_API_KEY
    geolocator = GoogleV3(api_key)
    location = geolocator.geocode(addr)
    assert location.address == ret_addr

