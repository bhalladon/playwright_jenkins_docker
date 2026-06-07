FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre\
    openjdk-21-jdk-headless\
    wget \
    unzip && \
    wget -q https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.tgz && \
    tar -xzf allure-2.29.0.tgz -C /opt && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/local/bin/allure && \
    rm allure-2.29.0.tgz && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chrome

COPY . .

ENV WEB_BROWSER=chrome \
    HEADLESS=true \
    APP_URL=https://testautomationpractice.blogspot.com/

RUN mkdir -p screenshots allure-results allure-report

CMD ["sh", "-c", "pytest tests/ --tb=short -v --alluredir=allure-results && allure generate allure-results -o allure-report --clean"]
