pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        AWS_REGION     = 'ap-south-2'
        AWS_ACCOUNT_ID = '280710007209'

        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        BACKEND_REPO  = 'employee-task-backend'
        FRONTEND_REPO = 'employee-task-frontend'

        IMAGE_TAG = "v${BUILD_NUMBER}"

        DEPLOY_DIR = '/opt/employee-task'

        COMPOSE_PROJECT_NAME = 'employee-task-devops'
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
                    set -e

                    echo "========================================"
                    echo "Current Git branch:"
                    git branch --show-current

                    echo
                    echo "Latest commit:"
                    git log --oneline -1

                    echo "========================================"
                '''
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    sh '''
                        set -e

                        echo "Creating Python virtual environment..."

                        python3 -m venv .venv

                        . .venv/bin/activate

                        echo "Upgrading pip..."
                        pip install --upgrade pip

                        echo "Installing backend dependencies..."
                        pip install -r requirements.txt

                        echo "Running backend tests..."
                        pytest -v
                    '''
                }
            }
        }

        stage('Frontend Build') {
            steps {
                dir('frontend') {
                    sh '''
                        set -e

                        echo "Installing frontend dependencies..."
                        npm ci

                        echo "Building frontend..."
                        npm run build
                    '''
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh '''
                    set -e

                    echo "Logging in to AWS ECR..."

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
                    set -e

                    echo "Building backend image..."

                    docker build \
                        -t ${BACKEND_REPO}:${IMAGE_TAG} \
                        ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                    set -e

                    echo "Building frontend image..."

                    docker build \
                        -t ${FRONTEND_REPO}:${IMAGE_TAG} \
                        ./frontend
                '''
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                    set -e

                    echo "Tagging backend image..."

                    docker tag \
                        ${BACKEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}

                    docker tag \
                        ${BACKEND_REPO}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:latest


                    echo "Tagging frontend image..."

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
                    set -e

                    echo "Pushing backend image..."

                    docker push \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${BACKEND_REPO}:latest


                    echo "Pushing frontend image..."

                    docker push \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${FRONTEND_REPO}:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Deploying application"
                    echo "Image tag: ${IMAGE_TAG}"
                    echo "Compose project: ${COMPOSE_PROJECT_NAME}"
                    echo "========================================"

                    cd ${DEPLOY_DIR}

                    export BACKEND_IMAGE=${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}
                    export FRONTEND_IMAGE=${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}

                    echo
                    echo "Backend image:"
                    echo "${BACKEND_IMAGE}"

                    echo
                    echo "Frontend image:"
                    echo "${FRONTEND_IMAGE}"

                    echo
                    echo "Pulling deployment images..."

                    docker compose \
                        -p ${COMPOSE_PROJECT_NAME} \
                        pull

                    echo
                    echo "Starting containers..."

                    docker compose \
                        -p ${COMPOSE_PROJECT_NAME} \
                        up -d --force-recreate

                    echo
                    echo "Container status:"

                    docker compose \
                        -p ${COMPOSE_PROJECT_NAME} \
                        ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Backend health check"
                    echo "========================================"

                    HEALTH_OK=false

                    for i in $(seq 1 12); do

                        echo "Health check attempt $i/12"

                        if curl -fsS http://localhost:8000/health; then

                            echo
                            echo "Backend health check passed"

                            HEALTH_OK=true

                            break
                        fi

                        echo "Backend not ready yet..."

                        sleep 5
                    done


                    if [ "$HEALTH_OK" != "true" ]; then

                        echo "Backend failed health check"

                        cd ${DEPLOY_DIR}

                        echo
                        echo "Container status:"

                        docker compose \
                            -p ${COMPOSE_PROJECT_NAME} \
                            ps

                        echo
                        echo "Backend logs:"

                        docker compose \
                            -p ${COMPOSE_PROJECT_NAME} \
                            logs \
                            --tail=100 \
                            backend

                        exit 1
                    fi


                    echo
                    echo "========================================"
                    echo "Backend readiness check"
                    echo "========================================"

                    READY_OK=false

                    for i in $(seq 1 12); do

                        echo "Readiness check attempt $i/12"

                        if curl -fsS http://localhost:8000/ready; then

                            echo
                            echo "Backend readiness check passed"

                            READY_OK=true

                            break
                        fi

                        echo "Backend not ready yet..."

                        sleep 5
                    done


                    if [ "$READY_OK" != "true" ]; then

                        echo "Backend failed readiness check"

                        cd ${DEPLOY_DIR}

                        echo
                        echo "Container status:"

                        docker compose \
                            -p ${COMPOSE_PROJECT_NAME} \
                            ps

                        echo
                        echo "Backend logs:"

                        docker compose \
                            -p ${COMPOSE_PROJECT_NAME} \
                            logs \
                            --tail=100 \
                            backend

                        exit 1
                    fi
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Deployment verification"
                    echo "========================================"

                    cd ${DEPLOY_DIR}

                    docker compose \
                        -p ${COMPOSE_PROJECT_NAME} \
                        ps

                    echo
                    echo "Backend deployed image:"

                    docker inspect \
                        employee-backend \
                        --format='{{.Config.Image}}'

                    echo
                    echo "Frontend deployed image:"

                    docker inspect \
                        employee-frontend \
                        --format='{{.Config.Image}}'

                    echo
                    echo "PostgreSQL container:"

                    docker inspect \
                        employee-postgres \
                        --format='{{.State.Status}}'
                '''
            }
        }

        stage('Verify ECR Images') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "Images pushed to ECR"
                    echo "========================================"

                    echo
                    echo "Backend:"
                    echo "${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}"

                    echo
                    echo "Frontend:"
                    echo "${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}"

                    echo
                    echo "Checking backend image in ECR..."

                    aws ecr describe-images \
                        --repository-name ${BACKEND_REPO} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION} \
                        --query 'imageDetails[0].imageTags' \
                        --output text

                    echo
                    echo "Checking frontend image in ECR..."

                    aws ecr describe-images \
                        --repository-name ${FRONTEND_REPO} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION} \
                        --query 'imageDetails[0].imageTags' \
                        --output text

                    echo
                    echo "========================================"
                '''
            }
        }
    }

    post {

        success {
            echo "========================================="
            echo "PIPELINE SUCCESSFUL"
            echo "========================================="

            echo "Branch: devops"

            echo "Backend:"
            echo "${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}"

            echo "Frontend:"
            echo "${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}"

            echo "Deployment directory:"
            echo "${DEPLOY_DIR}"

            echo "Compose project:"
            echo "${COMPOSE_PROJECT_NAME}"

            echo "========================================="
        }

        failure {
            echo "========================================="
            echo "PIPELINE FAILED"
            echo "Check the failed Jenkins stage and logs."
            echo "========================================="
        }

        always {
            echo "Pipeline completed."
        }
    }
}
