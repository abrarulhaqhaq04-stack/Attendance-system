pipeline {
    agent any
    stages {
       stage('Test') {
    steps {
        bat '"C:\\Program Files\\Python313\\python.exe" -m venv venv'
        bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
        bat 'venv\\Scripts\\python.exe -m pytest'
    }
}
        stage('Build Docker Image') {
            steps {
               bat '"C:\\Users\\abrar ul haq\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t attendance-app:4 .'
            }
        }
    }
}
