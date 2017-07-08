pipeline {
  agent {
    docker 'python:2.7-slim'
  }

  environment {
  BUDDY = 'GOODBOY'
  }
  stages {
    stage('Build') {
      steps {
        echo 'building!'
        which python
      }
    }
    stage('Test') {
      steps {
        echo 'testing!'
      }
    }
    stage('Deploy') {
      steps {
        echo 'deploying!'
      }
    }
  }
  post {
    always {
      deleteDir()
    }
    success {
      mail(from: "heyo@test.com",
           to: "leosayger@gmail.com",
           subject: "passed",
           body: "something something")
    }
  }

  options {
    buildDiscarder(logRotator(numToKeepStr:'10'))
    timeout(time: 10, unit: 'MINUTES')
  }
}
