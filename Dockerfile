FROM python:3.10.2

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app

CMD [ "fastapi", "run", "src/controller.py", "--port", "80" ]