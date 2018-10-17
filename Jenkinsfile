pipeline {
  agent none
  stages {
    stage('git') {
      steps {
        git(url: 'https://github.com/karthikithr/rpmbuildicon.git', branch: 'rpmbuildicon', credentialsId: 'githubcred')
      }
    }
  }
}