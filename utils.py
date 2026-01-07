from datetime import datetime, timezone

def headers_dict_to_str(headers_dict):
    response_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers_dict.setdefault("Date", response_date)
    return "".join([f"{key}: {headers_dict[key]}\r\n" for key in headers_dict])

def http_response(headers_dict, body, status_code=200):
    start_line = f"HTTP/1.1 {str(status_code)}"
    headers = headers_dict_to_str(headers_dict)

    return f"{start_line}\r\n{headers}\r\n".encode("utf-8") + (body if type(body) == bytes else body.encode("utf-8"))

def get_mime_type(file_name):
    type_map = {
        "html": "text/html",
        "png": "image/apng",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "css": "text/css",
        "js": "text/javascript"
    }

    file_extension = file_name.split(".")[1]

    return type_map[file_extension]

def headers_str_to_dict(headers_string):
    headers = headers_string.split("\r\n")
    headers_dict = {header.split(": ", 1)[0]: header.split(": ", 1)[1] for header in headers}

    return headers_dict

def get_parameters_from_path(req_path):
    if "?" not in req_path:
        return req_path, {}

    path, params_string = req_path.split("?")

    if "#" in params_string:
        params_string = params_string.split("#")[0]

    params_list = params_string.split("&")
    params_dict = {}
    for param in params_list:
        if len(param.split("=")) == 1:
            params_dict[param] = True
            continue

        key, value = param.split("=")
        params_dict[key] = value

    return path, params_dict