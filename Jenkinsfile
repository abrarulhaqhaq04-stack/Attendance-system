pipeline {
    agent any
    environment {
        KUBECONFIG = 'C:/users/abrar ul haq/.kube/config'
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
               bat '"C:\\Users\\abrar ul haq\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t attendance:4 .'
            }
        }
     stage('Deploy to Kubernetes') {
    steps {
        bat '''
            set "PATH=C:\\Users\\abrar ul haq\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%"
            kubectl config use-context docker-desktop

            kubectl version --client
            kubectl apply -f k8s/postgres.yml
            kubectl set image deployment/attendance attendance=attendance:4
            kubectl rollout status deployment/attendance --timeout=120s
        '''
    }
}
    }
}
