from bot.settings import settings


def get_context(user_id, response_data, phone_number, password, locale, full_name):
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
            "token": response_data,
            "phone_number": phone_number,
            "password": password,
            "locale": locale,
            "status": "OK",
            "full_name": full_name,
            "role": {"id": settings.DEFAULT_ROLE_ID, "label": "client"},
        },
    }
    return user_credentials
