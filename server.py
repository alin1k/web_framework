import socket
import os
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 8080
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def make_headers(headers_dict):
    return  "\n".join([f"{key}: {headers_dict[key]}" for key in headers_dict])

def make_http_response(headers, body, status_code):
    start_line = f"HTTP/1.1 {status_code}"
    headers = make_headers(headers)
    
    return f"{start_line}\n{headers}\n\n{body}".encode("utf-8")

def get_mime_type(file_name):
    type_map = {
        "html": "text/html",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "css": "text/css",
        "js": "text/javascript"
    }

    file_extension = file_name.split(".")[1]

    return type_map[file_extension]

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

            req_start_line = data.split("\n")[0].split(" ")

            req_method = req_start_line[0]
            req_path = req_start_line[1]
           
            file_path = os.path.join(ROOT_DIR, "static", req_path.lstrip("/"))
            
            try:
                with open(file_path, "r") as file:
                    file_data = file.read()
                    mime_type = get_mime_type(file.name)
                    response_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
                    headers = {
                        "Date": response_date,
                        "Content-Type": mime_type, 
                        "Content-Length": len(file_data)
                    }   
                    response = make_http_response(headers, file_data, "200 OK")
                    conn.sendall(response)
            except FileNotFoundError:
                response = make_http_response({}, "Not found", "Not Found")
                conn.sendall(response)
