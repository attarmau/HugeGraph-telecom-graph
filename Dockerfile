FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/telecom_ui.py ./telecom_ui.py
COPY assets/ ./assets

CMD ["streamlit", "run", "telecom_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
