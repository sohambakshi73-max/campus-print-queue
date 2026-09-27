pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint & Static Analysis') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                '''
            }
        }

        stage('Execute Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -v
                '''
            }
        }

        stage('Deploy Notification') {
            steps {
                echo 'Build, lint, and test validation passed. Ready for deployment.'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}