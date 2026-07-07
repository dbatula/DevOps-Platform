pipeline{

    agent any

    environment{
        DOCKERHUB_REPO = "ngcicd"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages{
        stage("Checkout SCM"){
            steps{
                checkout scm
            }

        }

        stage("Build Images"){
            steps{
                echo "Building Auth service"
                dir('services/auth-service') { 
                    sh "docker build -t ${DOCKERHUB_REPO}/auth-service:${IMAGE_TAG} ."
                }
            }

        }

        stage("Push Images"){
            steps{
                echo "Push Auth service to DockerHub"
                echo "Push User service to DockerHub"
                echo "Push Order service to DockerHub"
            }

        }
    }
}