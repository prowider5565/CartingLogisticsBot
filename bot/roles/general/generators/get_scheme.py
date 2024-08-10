"""
Example Successful Authenticaton reponse in JSON:

{
    "error": null,
    "message": null,
    "timestamp": 1723093489477,
    "status": 200,
    "path": null,
    "data": {
        "count": 1,
        "check_username": false,
        "insert_user": {
            "status": "OK",
            "timestamp": 1723093489474,
            "data": {
                "message": "success.user_created_or_updated",
                "userId": "28sec861-ed00-4cb9-a9ea-2a9c0df757a3"
            }
        },
        "valid_sms": {
            "phone": "998324234234",
            "status": "VALID"
        },
        "token": {
            "status": "OK",
            "timestamp": 1723093489433,
            "data": {
                "access_token": "eyJhbGciOiJSUzI1NiJ9.eyJ1cGRhdGVfaWQiOjcyNiwwfvsdc3VsdvijojZmZTI5OTItMWE4My00ZjM2LTk4NjYtNWMyM2VjMjZhZDRhIiwicm9sZXMiOiJQbGF0b24gQWRtaW5zLCBEcml2ZXIsIENsaWVudCIsImlzcyI6IiIsInR5cGUiOiJCZWFyZXIiLCJsb2NhbGUiOiJ1eiIsInNpZCI6ImE0MTFkNDE3LTljYjUtNDdhNC1hZjY3LThiODAyZjFiOGFhNCIsImF1ZCI6ImFjY291bnQiLCJmdWxsX25hbWUiOiJCZWd6b2QiLCJleHAiOjE3MjMxMTE0ODksInNlc3Npb25fc3RhdGUiOiJTVEFURUxFU1MiLCJpYXQiOjE3MjMwOTM0ODksImp0aSI6IjRlY2M0MzM3LWUyMTgtNGJjOC1iMjc0LTQ0YzQ1M2JmZmZiNSIsInVzZXJuYW1lIjoiYmVrem9kIn0.MtrTagYaZa5QdlF8gyIC0X5NtfRY4uqmFvbFPTe7AYF8yvUBqvv0OXKrks8FcS1hBnACP4JN_kKlXfn9SquA6gJjHarqMzESo1zXwJkw1jCbCEQ-H3Yh99EMtH5t71b_bvEwKX9LFD07r-HgFYzhLrKJr7JXQNWHnXd768iFU7MUJH3PPMqDR1rEZ6B3wK2lORsQ1fbQf9xGxb1mmB1PDJ_TmBPqx5K5bgMWGuHeRorrSjgwi6EnfkXHybp69g6CB6nqJMQDeBBOAe0rlGFSPOk1XfTPBbSDKYqWzzWBbYAMEzrcAPXDqebtFMWhrCYa0TQbFR1yypDjh-tRlAU7Ow",
                "refresh_token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2NmZlMjk5MiweEWq0xYTgQEWzLTRmasvcvxcTg2Ni01YzIzZWMyNmFkNGEiLCJhdWQiOiJhY2NvdW50IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgyL2dhdGV3YXkvcGxhdG9uLWF1dGgvcmVhbG1zL2RldiIsImV4cCI6MTcyMzExMTQ4OSwic2Vzc2lvbl9zdGF0ZSI6IlNUQVRFTEVTUyIsImlhdCI6MTcyMzA5MzQ4OSwianRpIjoiNGVjYzQzMzctZTIxOC00YmM4LWIyNzQtNDRjNDUzYmZmZmI1Iiwic2lkIjoiYTQxMWQ0MTctOWNiNS00N2E0LWFmNjctOGI4MDJmMWI4YWE0IiwidXNlcm5hbWUiOiJiZWt6b2QifQ.lBW_buxO_h5hcieGFmb4n6WsnR__0r9tto_BS6jJ6U6qJ0CR6RxyFVlqCqdMUwrKK86e4YhoriYMCcCYmZczCcGWEoP_tL4fiQwyLzwSNfjKE4GtJd3P5A1YpK76BsaoQLPPH7x1mqyiJCQkP-sqVJDmqtlthHhUktLy1S6LQODr0ZgDXPwGY8rpIeZwdfjb-58uS5ikdqHP9oH4xw1khC3w8Gobu7oQ-RV2hYWO5gLiZAfhD4QZSUFXnI-4Oe0YKevj2afzy9OAulb4X_wOhP8crX72othMewaIjVriC4wXY4RghOQjFSLl3S1qzdbB4gvFBi3ifQzSi1ljJ7K6_g",
                "token_type": "Bearer",
                "expires_in": 18000000,
                "refresh_expires_in": 18000000
            }
        }
    },
    "response": null
}
"""


def get_context(user_id, response_data, phone_number, password, locale):
    """
    This function constructs a user credentials dictionary based on the provided parameters.

    Parameters:
    user_id (str): The unique identifier of the user.
    response_data (dict): The JSON response data from the Registration process.
    phone_number (str): The user's phone number.
    password (str): The user's password.
    locale (str): The user's locale (language preference).

    Returns:
    dict: A dictionary containing the user's credentials. The dictionary has the following structure:
        {
            "user_id": user_id,
            "credentials": {
                "token": token_data,
                "phone_number": phone_number,
                "password": password,
                "locale": locale,
            }
        }
    """

    user_credentials = {
        "user_id": user_id,
        "credentials": {
            "token": response_data["data"]["token"]["data"],
            "phone_number": phone_number,
            "password": password,
            "locale": locale,
            "status": "OK"
        },
    }
    return user_credentials
