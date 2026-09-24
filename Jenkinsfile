pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-2'
        AWS_ACCOUNT_ID = '280710007209'

        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        BACKEND_REPO  = 'employee-task-backend'
        FRONTEND_REPO = 'employee-task-frontend'

        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout DevOps Branch') {
            steps {
                git branch: 'devops',
                    url: 'https://github.com/Naveencodespeaks/employee-task-devops.git'
            }
        }

        stage('Verify Branch') {
            steps {
                sh '''
                    echo "Current Git branch:"
                    git branch --show-current

                    echo "Latest commit:"
                    git log --oneline -1
                '''
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate

                        pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v
                    '''
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                        npm ci
                        npm run build
                    '''
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh '''
                    aws ecr get-login-password \
                        --region ${AWS_REGION} \
                    | docker login \
                        --username AWS \
                        --password-stdin \
                        ${ECR_REGISTRY}
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                    docker build \
                        -t ${BACKEND_REPO}:${IMAGE_TAG} \
                        ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    docker build \
                        -t ${FRONTEND_REPO}:${IMAGE_TAG} \
                        ./frontend
                '''
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                    docker tag \
                        ${BACKEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}

                    docker tag \
                        ${BACKEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:latest


                    docker tag \
                        ${FRONTEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}

                    docker tag \
                        ${FRONTEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:latest
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                    docker push \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:latest


                    docker push \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:latest
                '''
            }
        }

        stage('Verify Images') {
            steps {
                sh '''
                    echo "Backend image:"
                    echo "${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}"

                    echo "Frontend image:"
                    echo "${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}"
                '''
            }
        }
    }

    post {

        success {
            echo "========================================="
            echo "BUILD SUCCESSFUL"
            echo "Branch: devops"
            echo "Backend: ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}"
            echo "Frontend: ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}"
            echo "========================================="
        }

        failure {
            echo "Pipeline failed. Check the failed stage."
        }

        always {
            echo "Pipeline completed."
        }
    }
}
