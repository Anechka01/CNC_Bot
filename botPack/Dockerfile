# Get the Fast API image with Python version 3.7
FROM python:3.9
# Create the directory for the container
WORKDIR /botPack
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./botPack ./

ENV BOT_TOKEN=file_env
EXPOSE 8001
# Run by specifying the host and port
CMD ["python", "bot.py"]