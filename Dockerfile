FROM python:3.12-slim

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /parser/src
WORKDIR /parser/src

RUN mv requirements.txt /parser
RUN pip install --upgrade pip
RUN pip install -r /parser/requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python", "main.py" ]