from .context import geocoding

def test_api_key_exists():
    assert geocoding.core.GOOGLE_GEOCODE_API_KEY is not None
