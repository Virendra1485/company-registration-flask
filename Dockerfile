FROM python:3.8
WORKDIR /company_record
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
