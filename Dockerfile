FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY chatbot.py .
EXPOSE 8080
# Make sure this says chatbot:app (NOT chatbot.py:app)
CMD ["uvicorn", "chatbot:app", "--host", "0.0.0.0", "--port", "8080"]
