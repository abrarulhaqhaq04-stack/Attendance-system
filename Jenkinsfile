pipeline {
    agent any
    environment {
        KUBECONFIG = 'C:\\jenkins-kube\\config'
    }
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
     stage('Deploy to Kubernetes') {
    steps {
        bat '''
            set "PATH=C:\\Users\\abrar ul haq\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%"

            kubectl version --client
            kubectl apply -f k8s/postgres.yml
            kubectl apply -f k8s/deployment.yml
            kubectl set image deployment/attendance attendance=attendance:latest
            kubectl rollout status deployment/attendance --timeout=120s
        '''
    }
}
    }
}
