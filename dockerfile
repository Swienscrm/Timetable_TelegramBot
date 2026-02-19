FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /bot

# сначала зависимости (для кеша сборки)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# потом весь проект
COPY . .

# запуск
CMD ["python", "main.py"]