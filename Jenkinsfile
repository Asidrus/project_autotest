properties([disableConcurrentBuilds()])

pipeline {
    agent {
        label 'jenkins_host'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
    }
    environment {
        IP="37.140.198.248"
        WEBSITE_PORT_HTTPS=8091
        WEBSITE_PORT_HTTP=8090
        TELEGRAMBOT_PORT=8092
    }
    stages {
        stage('website') {
            steps {
                dir ("project_website"){
                    git branch: "dev", url: 'git@github.com:Asidrus/project_website.git', credentialsId: 'Github_ssh'
                    withCredentials([string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY')]) {
                        sh """
                        echo SECRET_KEY=$SECRET_KEY > .env
                        echo TELEGRAMBOT_IP=$IP >> .env
                        echo TELEGRAMBOT_PORT=$TELEGRAMBOT_PORT >> .env
                        """
                    }
                    sh "sudo rm -rf data"
                    sh "cp -r ~/data ./"
                    sh "docker-compose up -d --build"
                }
            }
        }
        stage('telegrambot') {
            steps {
                dir ("project_telegrambot"){
                    git branch: "dev", url: 'git@github.com:Asidrus/project_telegrambot.git', credentialsId: 'Github_ssh'
                    withCredentials([string(credentialsId: 'API_TOKEN', variable: 'API_TOKEN')]) {
                        sh """
                        echo "API_TOKEN=$API_TOKEN" > .env
                        echo "WEBSITE_IP=$IP" >> .env
                        echo "WEBSITE_PORT=$WEBSITE_PORT_http" >> .env
                        """
                    }
                    sh "docker-compose up -d --build"
                }
            }
        }
        stage('run autotests') {
            steps {
                dir ('project_autotest')
                {
                    git branch: "main", url: 'git@github.com:Asidrus/project_autotest.git', credentialsId: 'Github_ssh'
                    sh """
                    echo "WEBSITE_IP=$IP" > .env
                    echo "WEBSITE_PORT=$WEBSITE_PORT_HTTP" >> .env
                    echo "REMOTE=true" >> .env
                    echo "INTERACTIVE_MODE=false" >> .env
                    echo "WEBDRIVER_IP=$IP" >> .env
                    echo "WEBDRIVER_PORT=4444" >> .env
                    """
                    sh "docker-compose up -d --build"
                    sh "sudo chmod -R 777 allure-results"
                }
            }
        }
        stage('stop containers'){
            steps {
                sh """
                docker stop project_telegrambot_telegram_1
                docker stop project_website_web_1
                docker stop project_website_nginx_1
                docker stop project_website_db_1
                docker container prune -f
                """
            }
        }
        stage('reports') {
            steps {
                dir ('project_autotest') {
                    script {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: 'allure-results']]
                        ])
                    }
                }
            }
        }
    }
}
