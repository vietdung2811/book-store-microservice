FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     gcc     python3-dev     build-essential libmariadb-dev pkg-config netcat-traditional     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

EXPOSE 8000

CMD ["/wait-for-db.sh", "mariadb", "python", "manage.py", "runserver", "0.0.0.0:8000"]
