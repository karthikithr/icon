pipeline {
  agent none
  stages {
    stage('git') {
      steps {
        git(url: 'https://github.com/karthikithr/icon.git', branch: 'icon', credentialsId: 'githubcredentials')
      }
    }
  }
}