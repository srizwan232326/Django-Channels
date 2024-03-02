# Dockerfile

FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Download wait-for-it.sh using curl
RUN curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh

# Provide execute permissions
RUN chmod +x wait-for-it.sh

EXPOSE 8000

RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

# Wait for the database
CMD ["./wait-for-it.sh", "db:5432", "--", "celery", "-A", "realtime", "worker", "-l", "info"]
