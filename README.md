# Guru Quotes API 🧘

[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-informational.svg)](https://pytest.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff_&_isort-purple.svg)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Микросервис на **FastAPI** для получения мудрых цитат от различных гуру. Проект демонстрирует лучшие практики построения API, включая работу с базой данных, асинхронность, полное тестовое покрытие и поддержку контейнеризации.

---

## 📜 Оглавление

* [✨ Ключевые возможности](#-ключевые-возможности)
* [🛠️ Технологический стек](#-технологический-стек)
* [🚀 Быстрый старт](#-быстрый-старт)
    * [Предварительные требования](#предварительные-требования)
    * [Установка и запуск](#установка-и-запуск)
* [🧪 Запуск тестов](#-запуск-тестов)
* [📚 Документация API](#-документация-api)
    * [Gurus](#gurus)
    * [Quotes](#quotes)
    * [Status](#status)
* [📂 Структура проекта](#-структура-проекта)
* [🤝 Контрибьюторы](#-контрибьюторы)

---

## ✨ Ключевые возможности

* **Полный CRUD**: Реализованы все операции (Create, Read, Update, Delete) для сущностей "Гуру" и "Цитаты".
* **Пагинация**: Список гуру поддерживает пагинацию для эффективной работы с большими объемами данных.
* **Валидация данных**: Надежная валидация запросов и сериализация ответов с помощью `Pydantic` и `SQLModel`.
* **Работа с БД**: Интеграция с PostgreSQL через `SQLAlchemy` и `SQLModel` для асинхронной и синхронной работы.
* **Автоматическая генерация документации**: Интерактивная документация API доступна через Swagger UI и ReDoc.
* **Контейнеризация**: Готовая конфигурация `docker-compose.yaml` для легкого развертывания с PostgreSQL и Adminer.
* **Комплексное тестирование**: Высокий уровень тестового покрытия с использованием `Pytest` и `HTTPX`.

---

## 🛠️ Технологический стек

| Назначение             | Технология                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Веб-фреймворк** | [**FastAPI**](https://fastapi.tiangolo.com/)                                                                       |
| **База данных** | [**PostgreSQL**](https://www.postgresql.org/)                                                                     |
| **ORM** | [**SQLAlchemy**](https://www.sqlalchemy.org/) & [**SQLModel**](https://sqlmodel.tiangolo.com/)                     |
| **Тестирование** | [**Pytest**](https://docs.pytest.org/) & [**HTTPX**](https://www.python-httpx.org/)                                |
| **Валидация** | [**Pydantic**](https://docs.pydantic.dev/)                                                                        |
| **Менеджер пакетов** | [**Poetry**](https://python-poetry.org/)                                                                          |
| **Линтинг/Форматирование**| [**Ruff**](https://github.com/astral-sh/ruff) & [**isort**](https://pycqa.github.io/isort/)                      |
| **Контейнеризация** | [**Docker**](https://www.docker.com/)                                                                             |

---

## 🚀 Быстрый старт

### Предварительные требования

* **Python 3.12+**
* **Poetry**
* **Docker** и **Docker Compose**

### Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL-вашего-репозитория>
    cd <имя-папки-проекта>
    ```

2.  **Создайте файл окружения:**
    Создайте файл `.env` в корне проекта, скопировав `.env.example`, или создайте его вручную со следующим содержимым:
    ```dotenv
    # .env
    DATABASE_ENGINE="postgresql://postgres:example@localhost:5432/postgres"
    DATABASE_POOL_SIZE=10
    API_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)"
    ```
    *Я добавил файл-пример `.env.example`, который стоит добавить в репозиторий.*

3.  **Установите зависимости:**
    ```bash
    poetry install
    ```

4.  **Запустите Docker-контейнеры:**
    Эта команда поднимет базу данных PostgreSQL и Adminer для управления БД.
    ```bash
    docker-compose up -d
    ```

5.  **Запустите приложение:**
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

После этого API будет доступен по адресу **`http://127.0.0.1:8000`**.

---

## 🧪 Запуск тестов

Для запуска полного набора тестов убедитесь, что вы установили все зависимости, и выполните команду:

```bash
poetry run pytest -v
