import config
import http.server
import urllib.parse
import importlib
import os
import datetime

# Путь к папке /data
data_folder = config.save + "/data"
os.makedirs(data_folder, exist_ok=True)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            content = "<DOCTYPE html>"
            content += "<html><head><title>GrafanaGrab</title></head><body>"
            content += "<h1 style='text-align: center;'>GrafanaGrab</h1>"
            content += "<button id='run-script-button' style='position: absolute; left: 20px; top: 50px;'>Run Script</button>"
            content += "<table style='width: 100%; border: 1px solid #ccc; border-collapse: collapse;'>"
            content += "<tr><th style='border: 1px solid #ccc;'>File Name</th><th style='border: 1px solid #ccc;'>Date Created</th></tr>"

            data_files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]
            for file in data_files:
                file_path = os.path.join(data_folder, file)
                file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                content += f"<tr><td style='border: 1px solid #ccc;'><a href=\"/{file}\" download>{file}</a></td><td style='border: 1px solid #ccc;'>{file_date}</td></tr>"

            content += "</table>"
            content += "<script src=\"/jquery-3.6.0.min.js\"></script><script>"
            content += "$(document).ready(function(){$('#run-script-button').click(function(event){event.preventDefault();$.ajax({url:'/run_script',type:'POST',success:function(response){alert('Script executed successfully.');},error:function(jqXHR,textStatus,errorThrown){alert('Error executing script: ' + textStatus);}});});});"
            content += "</script>"
            content += "</body></html>"
            content = content.encode()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        elif self.path.startswith("/"):
            file_path = os.path.join(data_folder, urllib.parse.unquote(self.path[1:]))

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename=\"{os.path.basename(file_path)}\"")
                self.end_headers()
                self.wfile.write(content)
            elif self.path == "/favicon.ico":
                file_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
                with open(file_path, "rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.end_headers()
                self.wfile.write(content)
            elif self.path == "/jquery-3.6.0.min.js":
                file_path = os.path.join(os.path.dirname(__file__), "jquery-3.6.0.min.js")
                with open(file_path, "rb") as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()
                self.wfile.write(content)
        else:
            self.send_response(404)

    def do_POST(self):
        if self.path == "/run_script":
            script_module = importlib.import_module("main")
            script_module.main()

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Refresh", "0")
            self.end_headers()
            self.wfile.write(b"Script executed successfully.")
        else:
            self.send_response(404)

if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, CustomHandler)
    print(f"Starting server on http://localhost:8000")
    httpd.serve_forever()
