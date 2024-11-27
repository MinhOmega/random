FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD ["python", "src/main.py"]
