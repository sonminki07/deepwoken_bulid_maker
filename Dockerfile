FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg and Git
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run 24/7 Discord bot
CMD ["python", "discord_bot.py"]
