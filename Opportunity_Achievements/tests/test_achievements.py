from Opportunity_Achievements.app import app

def test_achievements_page_loads():
    """
    Ensure the achievements page loads successfully (status code 200).
    """
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_achievements_page_content():
    """
    Ensure key text appears on the achievements page.
    """
    client = app.test_client()
    response = client.get("/")
    html = response.data.decode()

    # Check for expected content
    assert "Achievements" in html
    assert "Total Volunteer Hours" in html
    assert "Total Organizations Joined" in html
