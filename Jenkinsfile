pipeline {
    agent any

    environment {
        AWS_REGION   = 'ap-south-1'
        ECR_REPO     = '575589967956.dkr.ecr.ap-south-1.amazonaws.com/cloudpulse-app'
        IMAGE_TAG    = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rajeshdangi04/cloudpulse-app.git'
            }
        }

        stage('Lint & Test') {
            steps {
                dir('app') {
                    sh 'pip install flake8 -q'
                    sh 'flake8 main.py --max-line-length=120'
                    sh 'python -c "import main; print(main.app.name)"'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh """
                    aws eks update-kubeconfig --region ${AWS_REGION} --name cloudpulse-cluster
                    kubectl set image deployment/cloudpulse-app cloudpulse-app=${ECR_REPO}:${IMAGE_TAG} -n cloudpulse
                    kubectl rollout status deployment/cloudpulse-app -n cloudpulse --timeout=60s
                """
            }
        }
    }

    post {
        success {
            mail to: 'umeshdangi@gmail.com',
                 subject: "✅ Build #${BUILD_NUMBER} Success",
                 body: "Deployment successful! Image: ${ECR_REPO}:${IMAGE_TAG}"
        }
        failure {
            mail to: 'umeshdangi@gmail.com',
                 subject: "❌ Build #${BUILD_NUMBER} Failed",
                 body: "Pipeline failed. Check: ${BUILD_URL}"
        }
    }
}
