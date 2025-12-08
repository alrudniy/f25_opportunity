import pytest
from opportunity_company_info.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_company_info_page_loads(client):
    """Test that the company info page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Opportunity Company Info" in response.data # Assuming this text is present on the page
