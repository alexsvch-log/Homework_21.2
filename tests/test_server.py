from typing import Generator

import pytest
from flask.testing import FlaskClient
from werkzeug.wrappers import Response

from src.server import app


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """Фикстура для создания тестового клиента Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_contacts_page(client: FlaskClient) -> None:
    """Тест: любой обычный GET-запрос возвращает контакты."""
    response: Response = client.get("/")
    assert response.status_code == 200

    # Переводим байты в текст и проверяем обычные слова
    page_text = response.data.decode("utf-8")
    assert "<!DOCTYPE html>" in page_text
    assert "Контакты" in page_text


def test_get_individual_page_success(client: FlaskClient) -> None:
    """Тест: JS-роут успешно отдает чистый контент страницы."""
    response: Response = client.get("/get-page/home")
    assert response.status_code == 200

    page_text = response.data.decode("utf-8")
    assert "Главная" in page_text


def test_error_404_on_missing_file(client: FlaskClient) -> None:
    """Тест: роут загрузки страниц выдает 404, если файла не существует."""
    response: Response = client.get("/get-page/non_existent_page_999")
    assert response.status_code == 404

    page_text = response.data.decode("utf-8")
    assert "Страница не найдена" in page_text


def test_error_404_handler_post(client: FlaskClient) -> None:
    """Тест: проверяем поведение системы при POST-запросе на неизвестный адрес."""
    response: Response = client.post("/some-broken-link")

    # Так как наш роут перехватывает все пути для GET,
    # для метода POST этот адрес вернет 405 (Method Not Allowed).
    assert response.status_code == 405


def test_post_feedback_redirect(client: FlaskClient) -> None:
    """Тест: отправка формы (POST) успешно принимает данные и делает редирект (302)."""
    form_data = {"name": "Тест Вася", "email": "test@mail.ru", "message": "Привет от автотеста!"}
    response: Response = client.post("/feedback", data=form_data)
    assert response.status_code == 302
