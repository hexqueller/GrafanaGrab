import config
import logging0
import http.server
import urllib.parse
import importlib
import os
import datetime

# Путь к папке /data
data_folder, filler = logging0.create_dir(config.save)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            content = "<DOCTYPE html>"
            content += "<html><head><title>GrafanaGrab</title>"
            content += "<meta charset='UTF-8'>"
            content += "<style>"
            content += "body { font-family: Arial, sans-serif; background-color: #111111; color: #fff; }"
            content += "h1 { margin-bottom: 20px; color: #fff; }"
            content += "table { margin-bottom: 20px; border-collapse: collapse; border: 1px solid #337ab7; }"
            content += "table th, table td { padding: 10px; text-align: center; border: 1px solid #337ab7; }"
            content += "table tr:nth-child(2n+1) { background-color: #333; }"
            content += "table tr:nth-child(2n) { background-color: #2f3640; }"
            content += "table th { background-color: #337ab7; color: #fff; font-size: 12px; padding: 5px; }"
            content += "#log-window { width: 100%; height: 300px; overflow-y: scroll; border: 1px solid #337ab7; padding: 10px; background-color: #333; color: #fff; }"
            content += "#run-script-button { background-color: #337ab7; color: #fff; padding: 10px 20px; border: none; border-radius: 0; font-size: 16px; cursor: pointer; }"
            content += "#run-script-button:hover { background-color: #23527c; }"
            content += "</style>"
            content += "</head><body>"
            content += "<h1 style='text-align: center;'>GrafanaGrab</h1>"
            content += "<table style='width: 100%;'>"
            content += "<tr><th style='border: 1px solid #337ab7; font-size: 12px; padding: 5px;'>File Name</th><th style='border: 1px solid #337ab7; font-size: 12px; padding: 5px;'>Date Created</th></tr>"

            data_files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f)) and f != "log.txt"]
            for file in data_files:
                file_path = os.path.join(data_folder, file)
                file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%H:%M %d.%m.%Y')
                content += f"<tr><td style='border: 1px solid #337ab7;'><a href=\"/{file}\" download style='color: #fff'>{file}</a></td><td style='border: 1px solid #337ab7; text-align: center;'>{file_date}</td></tr>"

            content += "</table>"
            content += "<button id='run-script-button' style='position: relative; left: 20px; top: 20px; margin-top: 20px;'>Обновить</button>"
            content += "<div id='log-window'>"
            with open(os.path.join(data_folder, "log.txt"), "r", encoding="utf-8") as log_file:
                log_content = log_file.read()
                content += f"<pre>{log_content}</pre>"
            content += "</div>"

            content += "<script src=\"/jquery-3.6.0.min.js\"></script><script>"
            content += "$(document).ready(function(){$('#run-script-button').click(function(event){event.preventDefault();$.ajax({url:'/run_script',type:'POST',success:function(response){alert('Успех');location.reload();},error:function(jqXHR,textStatus,errorThrown){alert('Ошибка: ' + textStatus);}});});});"
            content += "</script>"
            content += "</body></html>"
            content = content.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
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
