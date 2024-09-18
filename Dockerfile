FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["pytest", "--serial-config=common/config_file.txt", "--tb=short", "--log-cli-level=DEBUG", "--log-cli-date-format=", "--log-file=pytest_output_1.log"]
