# Start with a base Python image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /astra

# Install dependencies
COPY requirements.txt /astra/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /astra/
