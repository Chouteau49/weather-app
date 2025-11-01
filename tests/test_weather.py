import requests_mock
from weather_app.weather import get_weather


def test_get_weather_success():
    """Test récupération météo réussie."""
    mock_data = {
        "current_condition": [{"temp_C": "20", "weatherDesc": [{"value": "Sunny"}]}]
    }
    with requests_mock.Mocker() as m:
        m.get("https://wttr.in/Paris?format=j1", json=mock_data)
        result = get_weather("Paris")
        assert result == {"temp": "20", "description": "Sunny"}


def test_get_weather_failure():
    """Test échec de récupération météo."""
    with requests_mock.Mocker() as m:
        m.get("https://wttr.in/Unknown?format=j1", status_code=404)
        result = get_weather("Unknown")
        assert result is None
