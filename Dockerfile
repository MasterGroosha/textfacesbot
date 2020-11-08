FROM python:3.8-slim-buster
WORKDIR /app
COPY data /app/data
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt
COPY *.py /app/
CMD ["python", "textfacesbot.py"]
