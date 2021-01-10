FROM python:3.6.9

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
RUN alembic upgrade head