FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (5001 to avoid macOS AirPlay conflict on 5000)
EXPOSE 5001

# Run the API with Gunicorn for production
CMD ["python", "api.py"]

# For production, use:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "api:app"]
