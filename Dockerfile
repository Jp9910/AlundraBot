FROM python:3.10-alpine

# Install necessary alpine packages
RUN apk add --no-cache bash vim git

# Set working directory
WORKDIR /app/

# Install required python extensions
COPY requirements.txt env.py ./
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

COPY ./src/ ./

# CMD [ "python", "./your-daemon-or-script.py" ]