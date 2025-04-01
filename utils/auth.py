import streamlit_authenticator as stauth

def get_authenticator():
    # Example credentials (replace with your own)
    credentials = {
        "usernames": {
            "user1": {
                "name": "User One",
                "password": stauth.Hasher(["password123"]).generate()[0]
            },
            "user2": {
                "name": "User Two",
                "password": stauth.Hasher(["password456"]).generate()[0]
            }
        }
    }
    authenticator = stauth.Authenticate(
        credentials,
        "cookie_name",
        "random_key",
        cookie_expiry_days=30
    )
    return authenticator