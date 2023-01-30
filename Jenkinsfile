pipeline {
    environment {
    registry = 'enowclaire/python-application-docker-image-sample'
    registryCredentials = 'DOCKERHUB-ACCESS-TOKEN'
    }
    agent any
    triggers {
        pollSCM('* * * * *')
    }
    stages {
        stage('Cloning our github repository') {
            steps {
                git credentialsId: 'GIT-ACCESS-TOKEN', url: 'https://github.com/enowclaire/app-py.git', branch: 'main' 
            }
        }
        stage('Build docker image') {
            steps {
                sh 'docker build -t app-py-image .'
            }
        }
        stage('Tag Image') {
            steps {
                sh 'docker tag app-py-image:latest enowclaire/python-application-docker-image-sample:$BUILD_NUMBER'
                sh 'docker tag app-py-image:latest enowclaire/python-application-docker-image-sample:latest'
            }
        }
        stage('Push image to Docker Repository') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DOCKERHUB-ACCESS-TOKEN', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
                    sh "echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin"
                    sh 'docker push $registry:$BUILD_NUMBER'
                    sh 'docker push $registry:latest'
                    
                }
            }
            
        }
    } 
    
}
