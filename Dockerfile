FROM python:3.12.2-slim-bullseye as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base as python-deps

ENV PYTHONUNBUFFERED 1

# Install pipenv and compilation dependencies
RUN pip install pipenv
#RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install -y apache2 apache2-dev python3-dev libpq-dev build-essential

COPY Pipfile .
COPY Pipfile.lock .
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
COPY . .

EXPOSE 80

LABEL authors="chojo"

ENTRYPOINT ["python", "main.py"]
