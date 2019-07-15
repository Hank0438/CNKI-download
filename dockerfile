FROM python:3

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8989
CMD ["python", "crawlerManager.py"]
