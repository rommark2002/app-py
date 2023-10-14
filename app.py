import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

# #Jenkins file
# pipeline {
#     environment {
#     registry = 'cmuriukin/python-application-docker-image-sample'
#     registryCredentials = 'DOCKER-HUB-CREDENTIALS'
#     }
#     agent any
#     triggers {
#         pollSCM('* * * * *')
#     }
#     stages {
#         stage('Cloning our github repository') {
#             steps {
#                 git credentialsId: 'GIT-ACCESS-TOKEN', url: 'https://github.com/cmuriukin/app-py.git', branch: 'main'
#             }
#         }
#         stage('Build docker image') {
#             steps {
#                 sh 'docker build -t app-py-image .'
#             }
#         }
#         stage('Tag Image') {
#             steps {
#                 sh 'docker tag app.py:latest cmuriukin/python-application-docker-image-sample:$BUILD_NUMBER'
#                 sh 'docker tag app.py:latest cmuriukin/python-application-docker-image-sample:latest'
#             }
#         }
#         stage('Push image to Docker Repository') {
#             steps {
#                 withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USERNAME')]) {
#                     sh "echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin"
#                     sh 'docker push $registry:$BUILD_NUMBER'
#                     sh 'docker push $registry:latest'

#                 }
#             }

#         }
#     }

# }
