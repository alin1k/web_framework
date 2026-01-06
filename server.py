import socket
import os
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 8080
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path_map = {}

def make_headers(headers_dict):
    response_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers_dict.setdefault("Date", response_date)
    return "".join([f"{key}: {headers_dict[key]}\r\n" for key in headers_dict])

def make_http_response(headers, body, status_code):
    start_line = f"HTTP/1.1 {status_code}"
    headers = make_headers(headers)
    
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

def get_request_headers(headers_string):
    headers = headers_string.split("\r\n")  
    headers_dict = {header.split(": ", 1)[0]: header.split(": ", 1)[1] for header in headers}
     
    return headers_string

def route(path, methods=["GET"]):
    def route_decorator(route_func):
        def route_wrapper(*args, **kwargs):
            return route_func(*args, **kwargs)

        path_map.update({
            path: {method: route_wrapper for method in methods}
        })
        
        return route_wrapper
    return route_decorator

@route(path="/test", methods=["GET"])
def test(*args, **kwargs):
    return make_http_response({}, "Merge!!! URAAa", "200 OK")



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))
    s.listen(1)
    print(f"Server started on: {HOST}:{PORT}\n\n\n")

    while True:
        conn, adr = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data: 
                continue   
    
            data = data.decode("utf-8")
            print(data)

            req_start_line = data.split("\r\n")[0].split(" ")

            req_method = req_start_line[0]
            req_path = req_start_line[1]
            req_headers = get_request_headers(data.split("\r\n", 1)[1].split("\r\n\r\n")[0])            

            if path_map.get(req_path, False):
                response = path_map[req_path][req_method]()
                conn.sendall(response)
                continue

            file_path = os.path.join(ROOT_DIR, "static", req_path.lstrip("/"))
            
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    mime_type = get_mime_type(file.name)
                    headers = { 
                        "Content-Type": mime_type, 
                        "Content-Length": len(file_data)
                    }                    
                    response = make_http_response(headers, file_data, "200 OK")
                    conn.sendall(response)
            except FileNotFoundError:
                response = make_http_response({}, "Not found", "404 Not Found")
                conn.sendall(response)
