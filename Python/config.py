url = "" # Пример http://grafana:3000
key = ""
save = "" # Пустой = рядом с скриптами
port = 8000

import os

if save == "":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    save = os.path.join(script_dir)