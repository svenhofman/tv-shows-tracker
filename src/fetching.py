import requests


def fetch(url, auth_key):

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_key}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
    except requests.HTTPError as err:
        # Handle HTTP errors
        if err.response.status_code == 401:
            # Incorrect API key
            raise ValueError(
                "Unauthorized: The API key is incorrect or missing."
            ) from err
        elif err.response.status_code == 403:
            # Forbidden access
            raise ValueError(
                "Forbidden: The API key does not have permission to access this resource."
            ) from err
        else:
            raise err
    except requests.ConnectionError as err:
        # Handle network connection errors
        raise RuntimeError("Network error: Unable to connect to the API.") from err
    except requests.Timeout as err:
        # Handle request timeout errors
        raise RuntimeError(
            "Request timeout: The request to the API timed out."
        ) from err2


def fetch_show(show_id, auth_key):
    try:
        url = f"https://api.themoviedb.org/3/tv/{show_id}?language=en-US"
        return fetch(url, auth_key)
    except requests.HTTPError as err:
        if err.response.status_code == 404:
            raise ValueError(
                f"Error most likely called by incorrect show id: {err}"
            ) from err


def fetch_search_results(query, auth_key):
    try:
        url = f"https://api.themoviedb.org/3/search/tv?query={query}&include_adult=false&language=en-US&page=1"
        result = fetch(url, auth_key)
        return result["results"]
    except requests.HTTPError as err:
        if err.response.status_code == 404:
            raise ValueError(
                f"Error most likely called by incorrect show id: {err}"
            ) from err
