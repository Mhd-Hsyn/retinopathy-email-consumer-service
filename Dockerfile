FROM python:3.10-slim

# Set working directory
WORKDIR /ai_call_assistant_saas_email_service

# Copy requirements into the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9007", "--reload"]

