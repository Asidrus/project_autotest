FROM python:3.10
ARG path=/app
ARG PROJECT='autotest'
WORKDIR $path/$PROJECT

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
CMD ["pytest", "--alluredir=./allure-results", "tests/test_api.py"]