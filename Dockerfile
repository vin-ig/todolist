FROM python:3.10-slim

WORKDIR /code
#RUN pip install poetry
#COPY pyproject.toml .
#RUN poetry install
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD python manage.py runserver 0.0.0.0:8000