from fastapi import HTTPException, Request


def get_device_token(request: Request):
    device_token = request.headers.get("device-token", None)

    if not device_token:
        raise HTTPException(status_code=401, detail="Device token is required")

    return device_token
