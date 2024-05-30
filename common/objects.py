class BaseDTO:
    success = True
    message = ""
    data = None

    def __init__(self, success=True, message="", data=None):
        if isinstance(success, bool):
            self.success = success
        if isinstance(message, str):
            self.message = message
        if isinstance(data, dict):
            self.data = data
