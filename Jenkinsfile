pipeline {
    agent any

    environment {
        WEB_BROWSER = 'chrome'
        APP_URL     = 'https://testautomationpractice.blogspot.com/'
        HEADLESS    = 'true'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install --with-deps chromium'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'mkdir -p screenshots'
                sh 'pytest tests/ --tb=short -v'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        }
    }
}
