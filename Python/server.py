import http.server
import urllib.parse
import importlib

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            with open("index.html", "rb") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/favicon.ico":
            with open("favicon.ico", "rb") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "image/x-icon")
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/jquery-3.6.0.min.js":
            with open("jquery-3.6.0.min.js", "rb") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)


    def do_POST(self):
        if self.path == "/run_script":
            # Импортируем модуль main.py и вызываем функцию main()
            script_module = importlib.import_module("main")
            script_module.main()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Script executed successfully.")
        else:
            self.send_response(404)

if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, CustomHandler)
    print(f"Starting server on http://localhost:8000")
    httpd.serve_forever()
