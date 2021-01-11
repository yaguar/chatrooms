FROM python:3.6.9

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
#RUN alembic upgrade head
CMD gunicorn app:init_app --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker

