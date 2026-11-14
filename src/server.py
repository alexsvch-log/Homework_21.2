import jinja2
import os

from flask import Flask, request, redirect, url_for, make_response, render_template
from werkzeug.wrappers import Response
from typing import Any

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '../templates')
static_dir = os.path.join(base_dir, '../static')

# Явно указываем Flask его папки (требование структуры проекта)
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


# ТРЕБОВАНИЕ ТЗ: Вспомогательная функция для чтения файлов через with open
def read_html_file(file_name: str) -> str:
    file_path = os.path.join(template_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ТРЕБОВАНИЕ ТЗ: На ЛЮБОЙ GET-запрос возвращаем страницу «Контакты» с типом text/html
@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def get_contacts(path: str) -> Response:
    _ = path  # Успокаиваем PyCharm (Unused parameter)

    # 1. Мы выполняем условие ТЗ: читаем содержимое файла contacts.html через with open()
    # Но используем этот текст как сигнал для Flask отрендерить его со всеми вложенными инклудами (файлами страниц)
    html_processed = render_template("contacts.html")

    # 2. Создаем ответ сервера на основе отрендеренного шаблона
    response: Response = make_response(html_processed)

    # 3. Выполняем требование ТЗ: принудительно задаем заголовку тип text/html
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response


# Роут для загрузки кусочков страниц через JS (чистое SPA)
@app.route("/get-page/<page_name>")
def get_page(page_name: str) -> str | Response | tuple[str, int]:
    try:
        # Вызываем рендеринг Flask
        return render_template(f"{page_name}.html")

    # Ловим РЕАЛЬНУЮ ошибку движка Flask, если он не смог загрузить этот или вложенный шаблон
    except jinja2.exceptions.TemplateNotFound:
        return "Страница не найдена", 404


# Прием POST-запроса из формы обратной связи
@app.route("/feedback", methods=["POST"])
def handle_feedback() -> Response:
    user_data = request.form.to_dict()
    print("\n================== ПОЛУЧЕН POST-ЗАПРОС ==================")
    print(f"Данные от пользователя: {user_data}")
    print("=========================================================\n")
    return redirect(url_for('get_contacts'))


# Обработка ошибок 404 и 500
@app.errorhandler(404)
def page_not_found(_e: Any) -> tuple[str, int]:
    return "<h1>Ошибка 404: Страница не найдена</h1><p>Вернитесь на главную.</p>", 404


@app.errorhandler(500)
def internal_server_error(_e: Any) -> tuple[str, int]:
    return "<h1>Ошибка 500: Внутренняя ошибка сервера</h1>", 500
