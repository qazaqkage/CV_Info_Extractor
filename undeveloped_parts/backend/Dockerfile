# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it.sh script
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Copy application code
COPY . .

# Expose the Flask application port
EXPOSE 5000

# Use wait-for-it.sh to wait for the database
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "job_matching_auth.py"]
