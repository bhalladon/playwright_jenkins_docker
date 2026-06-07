pipeline {
    agent any

    environment {
        WEB_BROWSER = 'chrome'
        APP_URL     = 'https://testautomationpractice.blogspot.com/'
        HEADLESS    = 'true'
    }

    parameters {
    choice(
            name: 'WEB_BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Select a web browser where you want to execute the tests'
        )
}

    stages {

        stage('Linux Tasks') {
            when {
                expression { isUnix() }
            }
            steps {
                echo "Running on a Linux / Unix agent"
                sh 'echo "Hello from Linux!"'
                sh 'pip install -r requirements.txt'
                sh 'playwright install chrome firefox'
            }
        }

        stage('Windows Tasks') {
            when {
                expression { !isUnix() }
            }
            steps {
                echo "Running on a Windows agent"
                bat 'echo Hello from Windows!'
                bat 'cd'
                bat 'dir'
                bat 'C:\\Users\\bhall\\AppData\\Local\\Programs\\Python\\Python314\\python.exe -m pip install -r requirements.txt'
                bat 'C:\\Users\\bhall\\AppData\\Local\\Programs\\Python\\Python314\\python.exe -m playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'C:\\Users\\bhall\\AppData\\Local\\Programs\\Python\\Python314\\python.exe -m pytest tests/ --tb=short -v --alluredir=allure-results'
            }
        }
    }

    post {
    always {
        archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        allure([
            includeProperties: false,
            reportBuildPolicy: 'ALWAYS',
            commandline: 'allure',
            results: [[path: 'allure-results']]
        ])}
    }
}
