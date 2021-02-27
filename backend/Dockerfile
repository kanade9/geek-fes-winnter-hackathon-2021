FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python","FLASK_APP=main.py"]