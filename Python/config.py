url = "" # Пример http://grafana:3000
key = ""
save = "" # Пустой = рядом с скриптами


import os

script_dir = os.path.dirname(os.path.realpath(__file__))
if save == "":
    save = os.path.join(script_dir)