FROM python:3.8-slim-buster
WORKDIR /app
COPY faces_original.txt /app/
COPY start.sh /app/
RUN chmod +x /app/start.sh
COPY data /app/data
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
COPY *.py /app/
CMD ["/app/start.sh"]
