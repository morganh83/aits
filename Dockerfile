# Start with a base Python image
FROM python:3.9

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /astra

# # Copy project
COPY . /astra
# COPY ./scripts/wait_for_db.py /astra/wait_for_db.py

# Install dependencies
COPY requirements.txt /astra/

WORKDIR /astra
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["./wait_for_db.py && python", "manage.py", "runserver", "0.0.0.0:8000"]