# Use the official Python image for testing
FROM python:3.10.1-slim-bullseye

WORKDIR /app_code

# Install dependencies
RUN apt-get update && apt-get install --yes --no-install-recommends figlet boxes curl xmlsec1 postgresql-client-13 g++ libssl-dev gcc pkg-config libcairo2-dev && rm -rf /var/lib/apt/lists/*

# Copy application code into a directory called 'app_code'
COPY ./src /app_code

# Create directory for coverage reports
# RUN mkdir /app_code/htmlcov && chown -R $USER:$USER /app_code/htmlcov

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pytest coverage

# Set the command to run tests
CMD ["sh", "-c", "pytest"]
