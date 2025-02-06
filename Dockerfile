FROM python:3.9-slim

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .
EXPOSE 7100

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:7100", "app.app:app"]