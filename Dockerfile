FROM python:3.12-slim

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /parser/src

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /parser/

RUN pip install --upgrade pip
RUN pip install -r /parser/requirements.txt

RUN curl -sL https://raw.githubusercontent.com/kevincobain2000/email_extractor/master/install.sh | sh \
    && mv email_extractor /usr/local/bin/

COPY . /parser/src

EXPOSE 8000

# ENTRYPOINT [ "python", "main.py" ]
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]