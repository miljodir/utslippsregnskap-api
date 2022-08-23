FROM node:16-alpine

WORKDIR /app
ADD client .
RUN npm ci
RUN npm run build

FROM python:3.10-slim-bullseye

WORKDIR /app
ADD utslippsregnskap-api .

RUN pip3 install -U pip wheel --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir

COPY --from=0 /app/static static

CMD gunicorn -t 60 -w 2 --bind 0.0.0.0:8000 app:app