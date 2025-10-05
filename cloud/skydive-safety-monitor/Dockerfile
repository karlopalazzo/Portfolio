# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]