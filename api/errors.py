def get_error_by_code(code):
    errors = {
        701: "method is not POST",
        702: "request's method not found",
        703: "invalid request's method",

        721: "invalid data request",
    }
    return errors.get(code, '')