FROM python:3.10-slim

RUN apt-get update \
  && apt-get install -y curl build-essential \
  && apt-get clean

# 🚀 Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /water-intake-tracker-server-app

COPY . /water-intake-tracker-server-app

ENV PYTHONPATH=/water-intake-tracker-server-app/src

RUN poetry install --no-root --without dev

RUN poetry run prisma generate --schema=src/infrastructure/database/orm/prisma/schema.prisma

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app_api", "--reload", "--host", "0.0.0.0", "--port", "8000", "-log-level", "debug"]
