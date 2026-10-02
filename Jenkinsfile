pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
                bat 'venv\\Scripts\\pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t attendance-app:%BUILD_NUMBER% .'
            }
        }
    }
}