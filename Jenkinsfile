pipeline {
    agent any
    environment {
        dockerId = 'anhassan94'
        dockerImageName = 'dockeretl'
        dockerImageSnapshot = 'lt1'
        dockerImage = ''
        registry = "${dockerId}/${dockerImageName}:${dockerImageSnapshot}"
        registryCredential = 'dockerHubCredentials'
    }
    stages {
        stage('Git Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']],
                 extensions: [], userRemoteConfigs:
                  [[url: 'https://github.com/anhassan/ETL-CiCd-Jenkins-Pipeline-With-Docker.git']]])
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build registry
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
