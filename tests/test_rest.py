from web import webapp
import json


# def pytest_sessionstart(session):
#     """
#     Called after the Session object has been created and
#     before performing collection and entering the run test loop.
#     """
#     session.app = app.test_client()


# @pytest.fixture(scope="session", autouse=True)
def test_successful_signup():
    app = webapp.app.test_client()
    # Given
    payload = json.dumps({
        "email": "paurakh011@gmail.com",
        "password": "mycoolpassword"
    })

    # When
    response = app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)


