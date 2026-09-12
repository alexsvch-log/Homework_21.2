# Импортируем готовое Flask-приложение из папки src
from src.server import app

if __name__ == "__main__":
    # Запускаем модуль server.py отсюда
    app.run(debug=True)
