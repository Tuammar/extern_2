FROM python:3.12.1

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-dev

RUN poetry add uvicorn

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
