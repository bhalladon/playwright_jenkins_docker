pipeline {
    agent any

    environment {
        WEB_BROWSER = 'chrome'
        APP_URL     = 'https://testautomationpractice.blogspot.com/'
        HEADLESS    = 'true'
    }

    stages {
        stage('Run Tests') {
            steps {
                script {
                    docker.image('jenkins_test').inside('--ipc=host') {
                        sh 'mkdir -p screenshots allure-results'
                        sh 'pytest tests/ --tb=short -v --alluredir=allure-results'
                    }
                }
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
            ])
        }
    }
}
