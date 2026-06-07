pipeline {
    agent any

    environment {
        WEB_BROWSER = 'chrome'
        APP_URL     = 'https://testautomationpractice.blogspot.com/'
        HEADLESS    = 'true'
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
                sh 'playwright install --with-deps chromium'
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
                bat 'C:\\Users\\bhall\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe -m pip install -r requirements.txt'
                bat 'C:\\Users\\bhall\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe -m playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'mkdir -p screenshots'
                bat 'C:\\Users\\bhall\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe -m pytest tests/ --tb=short -v'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        }
    }
}
