# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /foodgram

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && \
     apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x /foodgram/entrypoint.sh
ENTRYPOINT ["/foodgram/entrypoint.sh"]