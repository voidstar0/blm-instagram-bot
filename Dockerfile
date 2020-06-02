FROM python:alpine
COPY . /usr/local/share
WORKDIR /usr/local/share
RUN pip install --no-cache-dir -r requirements_docker.txt
ENV CLOUD_FUNCTION_URL=https://us-central1-protect-blm.cloudfunctions.net/isSolidColor
CMD ["python", "bot.py"]