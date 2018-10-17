pipeline {
  agent any
  stages {
    stage('git') {
      steps {
        echo 'lets tart git integration'
      }
    }
    stage('gitman') {
      steps {
        git(url: 'https://github.com/karthikithr/rpmbuildicon.git', branch: 'rpmbuildicon', credentialsId: 'karthikithr')
      }
    }
  }
}