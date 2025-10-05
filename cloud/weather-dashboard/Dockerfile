# slim Python image
FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set the working directory
WORKDIR /app

# copy configuration files and requirements
COPY requirements.txt /app/

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the app
COPY . /app/

# default port for Flask (compatible with Cloud Run)
ENV PORT 8080

# run Flask
CMD ["python", "app.py"]
