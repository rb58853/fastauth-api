import httpx
from typing import Optional


DATABASE_API_URL: str = "http://localhost:8000/data/token"


def save_token(
    client_id: str,
    access_token: str,
    refresh_token: str,
) -> bool:
    """
    Save the access and refresh tokens for a given client ID to the database via a POST request.

    Args:
        client_id (str): The unique identifier for the client.
        access_token (str): The access token to be saved.
        refresh_token (str): The refresh token to be saved.

    Returns:
        bool: True if the tokens were saved successfully, False otherwise.
    """
    url = f"{DATABASE_API_URL}/save?client_id={client_id}"
    payload = {"access_token": access_token, "refresh_token": refresh_token}

    response = httpx.post(url, json=payload)
    return response.status_code == 200


def load_access_token(client_id: str) -> Optional[str]:
    """
    Retrieve the access token for a given client ID from the database via a GET request.

    Args:
        client_id (str): The unique identifier for the client.

    Returns:
        Optional[str]: The access token if found, None otherwise.
    """
    url = f"{DATABASE_API_URL}/load?client_id={client_id}"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    return None


def load_refresh_token(client_id: str) -> Optional[str]:
    """
    Retrieve the refresh token for a given client ID from the database via a GET request.

    Args:
        client_id (str): The unique identifier for the client.

    Returns:
        Optional[str]: The refresh token if found, None otherwise.
    """
    url = f"{DATABASE_API_URL}/load?client_id={client_id}"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("refresh_token")
    return None
