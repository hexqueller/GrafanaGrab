import os

url = os.getenv('URL', 'http://grafana:3000')
key = os.getenv('KEY', '')
save = os.getenv('SAVE', '')
port = int(os.getenv('PORT', '8000'))

# Если save пустой, устанавливаем его в текущую директорию скрипта
if save == "":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    save = os.path.join(script_dir)
