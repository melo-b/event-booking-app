# 1. Use the official, lightweight Python image
FROM python:3.11-slim

# 2. Safety/Best Practice Environment Variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1 
# Ensures Python output is sent straight to the terminal without buffering (great for logs)
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy just the requirements first (to leverage Docker cache)
COPY requirements.txt /app/

# 5. Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. Copy the rest of your application code
COPY . /app/

# 7. The default command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]