FROM python:3.12-alpine

ENV PYTHONBUFFERED=1

WORKDIR /SmartHomeBackend
# 3. Skopiuj plik requirements.txt do obrazu
COPY requirements.txt .

# 4. Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# 5. Skopiuj cały projekt do obrazu
COPY . .

# 6. Zmienna środowiskowa, aby uniknąć interakcji terminala
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 7. Uruchomienie serwera Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]