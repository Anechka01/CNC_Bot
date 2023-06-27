# Get the Fast API image with Python version 3.7
FROM python:3.9
# Create the directory for the container
WORKDIR /app
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ ./
EXPOSE 8000
# Run by specifying the host and port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]