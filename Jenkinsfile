#!groovy

node {

    try {
        stage 'Checkout'
            checkout scm

        stage 'Deploy'
            sh "docker build --tag django ."
	    


        stage 'Publish results'
           sh "docker run -d --name django -p 80:80 django"
    }

    catch (err) {
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}