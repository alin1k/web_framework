from server import HttpServer

server = HttpServer()

@server.route(path="/", methods=["GET"])
def index(*args, **kwargs):
    return server.send_file("index.html")

@server.route(path="/hello", methods=["GET"])
def hello(*args, **kwargs):
    request = kwargs.get("request")
    params = request.get("params", {})

    greeting = f"Hello, {params.get("name", "world")}!"

    return server.send(greeting)

server.listen(8080)