

def handle_api_response(response):
    """
    Check if the web service response was successful and handle errors.

    Args:
        response (requests.Response): The response object from the web service request.

    Returns:
        dict: A dictionary containing either the successful response data or error information.
    """
    obj = {
        "status": True,
        "data": response.json(),
        "error_code": response.status_code,
        "error_message": response.text
    }

    if response.status_code in [200,201,202]:
        obj["status"] = True
        obj["data"] = response.json()
        obj["error_code"] = response.status_code
        obj["error_message"] = response.text
        return obj

    else:
        obj["status"] = False
        obj["data"] = response.json()
        obj["error_code"] = response.status_code
        obj["error_message"] = response.text
        return obj
