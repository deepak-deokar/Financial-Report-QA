FROM python:3.10-slim

# Set workdir
WORKDIR /app
COPY . /app

# Copy backend code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

# Expose FastAPI on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]