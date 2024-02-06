FROM python:3.9.3

COPY requirements.txt /code/
WORKDIR /code/
RUN pip install -r requirements.txt

ADD ./backend /code/

ENV TZ Asia/Seoul

EXPOSE 8000

CMD ["gunicorn", "conf.wsgi:application", "--workers", "3", "--threads", "3", "-t", "300", "--bind", "0.0.0.0:8000"]
