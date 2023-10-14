FROM python:slim-buster

WORKDIR /app/src

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

CMD ["python", "gather_data.py"]