# Start with a base Python image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /aims

# Install dependencies
COPY requirements.txt /aims/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /aims/
