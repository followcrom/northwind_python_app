import requests
import pytest

# Run tests by navigating to tests folder and running "pytest"

# Can be improved by checking based on current machine's ip rather than localhost

@pytest.fixture(scope='session')
def app_url():
    return 'http://localhost:5000'  # Adjust the URL if your Flask app is running on a different address/port

def test_flask_app_running(app_url):
    response = requests.get(app_url)
    assert response.status_code == 200, f"Flask app is not running on {app_url}"
