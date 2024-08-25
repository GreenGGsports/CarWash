FROM python:3.11

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set work directory and copy only requirements first
ENV APP_HOME /back-end
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a separate layer
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install mysqlclient pymysql cryptography

# Copy the rest of the application files
COPY . .

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
