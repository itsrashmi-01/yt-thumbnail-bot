# Use slim Python base
FROM python:3.11-slim

# Keep Python output unbuffered (helps logging)
ENV PYTHONUNBUFFERED=1

# Install ntpdate (and other small utilities) so we can sync time in the container.
# Remove package lists afterwards to reduce image size.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     ntpdate \
     iputils-ping \
     ca-certificates \
     tzdata \
  && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
# (create requirements.txt in your project root)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Copy entrypoint and make sure it is executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# If your bot listens on a port (webhook), expose it. Otherwise omit.
# EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
# Optional: if you prefer CMD instead of exec in the entrypoint:
# CMD ["python", "/app/run.py"]