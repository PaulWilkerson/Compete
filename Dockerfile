FROM python:3.10

# This creates the /app directory inside the container
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of your code
COPY . .

# Set the Python Path so it can see your nested 'Compete' modules
ENV PYTHONPATH=/app/Compete/Compete/Compete
ENV DJANGO_SETTINGS_MODULE=Compete.Compete.settings
