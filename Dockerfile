# 1. Use Python base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY app.py .
COPY .env .

# 6. Expose port
EXPOSE 8000

# 7. Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
