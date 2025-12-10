FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000
CMD ["gunicorn","-w","4","-k","gthread","--threads","4","app:app","-b","0.0.0.0:5000"]
