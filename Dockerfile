FROM python3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY /src/url_shorter .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]