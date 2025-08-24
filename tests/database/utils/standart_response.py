def standard_response(status: str, message: str, code: int, data=None, details=None):
    response = {
        "status": status,
        "message": message,
        "code": code,
    }
    if data:
        response["data"] = data
    if details:
        response["details"] = details
    return response
