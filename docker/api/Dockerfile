# DMIRSBACKEND

# ===================================
# ---- Executed at Image Build ----
# ===================================
FROM python:3.10.1-slim-bullseye

WORKDIR /app_code

# Install Dependencies
RUN apt-get update && apt-get install --yes --no-install-recommends \
    figlet boxes curl xmlsec1 postgresql-client-13 g++ libssl-dev gcc \
    pkg-config libcairo2-dev unixodbc unixodbc-dev freetds-dev freetds-bin \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    unixodbc unixodbc-dev gnupg2  # Install ODBC dependencies and GnuPG

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17  # Install ODBC driver

# Update pip
RUN pip install --upgrade pip

# Copy application code into a directory called 'app_code'
COPY . /app_code



# Create a 'logs' directory
RUN mkdir -p /app_code/logs

# Installing requirements
RUN python -m venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

# Change the path to the requirements.txt file
COPY docker/api/requirements.txt /app_code/requirements.txt

RUN pip install -Ur requirements.txt

# Generate a timestamp of when this image was created for display in the logs / as the container comes up. Used as a sanity check.
RUN touch /app_code/build_timestamp.txt
RUN date > /app_code/build_timestamp.txt && cat /app_code/build_timestamp.txt

RUN figlet BACKEND - DJANGO

# ========================================
# ---- Executed at Container Runtime ----
# ========================================
# Runtime commands
COPY docker/api/setup.sh /app_code/setup.sh
RUN chmod +x /app_code/setup.sh

# Run setup script for migrations and static files
#RUN /app_code/setup.sh

# Runtime commands
CMD echo "Running in \develop environment" \
    && python manage.py migrate \
    && echo "Running: python manage.py runserver 0.0.0.0:8000" \
    && exec python manage.py runserver 0.0.0.0:8000