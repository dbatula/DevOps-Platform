pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'ngcicd'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        AWS_CREDENTIALS_ID = 'aws-credentials'
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                script {
                    def services = ['auth-service', 'user-service', 'order-service']
                    for (svc in services) {
                        sh "docker build -t ${DOCKERHUB_REPO}/${svc}:${IMAGE_TAG} services/${svc}"
                    }
                }
            }
        }

        stage('Push Images') {
            when {
                expression {
                    // The stage is executed only if the DOCKERHUB_CREDENTIALS_ID variable is not empty.
                    return env.DOCKERHUB_CREDENTIALS_ID?.trim()
                }
            }
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKERHUB_CREDENTIALS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                        def services = ['auth-service', 'user-service', 'order-service']
                        for (svc in services) {
                            sh "docker push ${DOCKERHUB_REPO}/${svc}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Terraform Init/Apply') {
            when {
                expression {
                    // The stage is executed only if the AWS_CREDENTIALS_ID variable is not empty.
                    return env.AWS_CREDENTIALS_ID?.trim()
                }
            }
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: env.AWS_CREDENTIALS_ID,
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )]) {
                        
                        // A directory for AWS config is created.
                        sh 'mkdir -p ~/.aws'
                        
                        // The ~/.aws/credentials file containing AWS access credentials is written.
                        sh 'cat > ~/.aws/credentials <<EOF\n[default]\naws_access_key_id = $AWS_ACCESS_KEY_ID\naws_secret_access_key = $AWS_SECRET_ACCESS_KEY\nEOF'
                        
                        // Switching to the terraform directory
                        dir('terraform') {
                            // 
                            sh 'terraform init -input=false'
                            
                            // Applying Terraform without a confirmation prompt.
                            sh 'terraform apply -auto-approve'
                        }
                    }
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: env.AWS_CREDENTIALS_ID,
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )]) {
                        sh 'mkdir -p ~/.aws'
                        sh 'cat > ~/.aws/credentials <<EOF\n[default]\naws_access_key_id = $AWS_ACCESS_KEY_ID\naws_secret_access_key = $AWS_SECRET_ACCESS_KEY\nEOF'

                        sh 'aws configure set region ${AWS_REGION}'

                        dir('terraform') {
                            // The EKS cluster name is taken from the Terraform output.
                            sh 'terraform output -raw cluster_name > /tmp/eks_cluster_name'
                        }
                        
                        // The cluster name is read into a Groovy variable.
                        def clusterName = readFile('/tmp/eks_cluster_name').trim()
                        
                        // Updating kubeconfig for EKS access
                        sh 'aws eks update-kubeconfig --name ${clusterName} --region ${AWS_REGION}'
                        
                        // Helm deployment is in progress.
                        sh 'helm upgrade --install devops-platform helm/devops-platform --namespace devops-platform --create-namespace --set services.auth.image=${DOCKERHUB_REPO}/auth-service:${IMAGE_TAG} --set services.user.image=${DOCKERHUB_REPO}/user-service:${IMAGE_TAG} --set services.order.image=${DOCKERHUB_REPO}/order-service:${IMAGE_TAG} --set services.postgres.image=postgres:17'
                    }
                }
            }
        }
    }
}