# Импортируем наше готовое Flask-приложение из папки src
from src.server import app

if __name__ == "__main__":
    # Запускаем сервер отсюда
    app.run(debug=True)