import os

from flask import Flask, make_response, redirect, render_template_string, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, "../templates")
static_dir = os.path.join(base_dir, "../static")

app = Flask(__name__, static_folder=static_dir)


# Вспомогательная функция для чтения файлов через контекстный менеджер (требование ДЗ!)
def read_html_file(file_name: str) -> str:
    file_path = os.path.join(template_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# НА ЛЮБОЙ GET-ЗАПРОС ОТДАЕМ КОНТАКТЫ
@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def get_contacts(path: str) -> Response:
    _ = path
    html_raw = read_html_file("contacts.html")

    # ВАЖНО: заставляем Flask обработать {{ url_for }} внутри считанного текста!
    html_processed = render_template_string(html_raw)

    # Специфичный метод Flask возвращает полноценный объект Response
    response: Response = make_response(html_processed)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response


# РОУТ ДЛЯ ПОДГРУЗКИ КУСОЧКОВ СТРАНИЦ ЧЕРЕЗ JS
@app.route("/get-page/<page_name>")
def get_page(page_name: str) -> str | Response | tuple[str, int]:
    try:
        html_raw = read_html_file(f"{page_name}.html")
        # Тут тоже обрабатываем, если внутри страниц будут картинки или ссылки через url_for
        return render_template_string(html_raw)
    except FileNotFoundError:
        return "Страница не найдена", 404


# Прием POST-запроса и печать данных в консоль без ошибок
@app.route("/feedback", methods=["POST"])
def handle_feedback() -> Response:
    user_data = request.form.to_dict()
    print("\n================== ПОЛУЧЕН POST-ЗАПРОС ==================")
    print(f"Данные от пользователя: {user_data}")
    print("=========================================================\n")
    return redirect(url_for("get_contacts"))


# --- ДОПОЛНИТЕЛЬНЫЙ ФУНКЦИОНАЛ: ОБРАБОТКА ОШИБОК (требование ДЗ!) ---
@app.errorhandler(404)
def page_not_found(_e: HTTPException) -> tuple[str, int]:
    return "<h1>Ошибка 404: Страница не найдена</h1><p>Вернитесь на главную.</p>", 404


@app.errorhandler(500)
def internal_server_error(_e: Exception) -> tuple[str, int]:
    return "<h1>Ошибка 500: Внутренняя ошибка сервера</h1>", 500

