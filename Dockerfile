FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install production dependencies. Adjust if you have a requirements.txt.
RUN pip install --no-cache-dir flask flask-cors gunicorn

# Set environment variables for production.
ENV FLASK_DEBUG=False

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]