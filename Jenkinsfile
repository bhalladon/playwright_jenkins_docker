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
                sh 'playwright install chromium firefox'
            }
        }

        stage('Windows Tasks') {
            when {
                expression { !isUnix() }
            }
            steps {
                echo "Running on a Windows agent"
                script {
                    def rawOutput = bat(script: 'where python', returnStdout: true).trim()
                    env.PYTHON_PATH = rawOutput.tokenize('\n').last().trim()
                    echo "Python found at: ${env.PYTHON_PATH}"
                }
                echo "${PYTHON_PATH}"
                bat  "${env.PYTHON_PATH} -m pip install -r requirements.txt"
                bat  "${env.PYTHON_PATH} -m playwright install chromium firefox"
            }
        }

        stage('Run Tests') {
            steps {
                bat "${PYTHON_PATH} -m pytest tests/ --tb=short -v --alluredir=allure-results"
                   echo "Run tests"
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
