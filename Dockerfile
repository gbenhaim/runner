FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y \
	strace \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .

ENTRYPOINT [ "python3", "./runner.py" ]
