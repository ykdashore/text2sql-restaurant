FROM python:3.11-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/src

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]
