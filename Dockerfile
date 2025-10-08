FROM python:3.10-slim

WORKDIR /ai_call_assistant_saas__email_service
COPY requirements.txt /law_firm_email_service/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /law_firm_email_service

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9007", "--reload"]

