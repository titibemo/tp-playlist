FROM python:latest

WORKDIR /home/thierry

COPY . .
RUN pip install psycopg[binary]
EXPOSE 5000

CMD ["python", "index.py"]
#CMD ["tail", "-f", "/dev/null"]