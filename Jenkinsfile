#!groovy

node {

    try {
        stage 'Checkout'
            checkout scm

        stage 'Deploy'
            sh "sudo docker build --tag "django" ."
	    


        stage 'Publish results'
           sh "sudo docker run -d --name "django" -p 8080:8080 "django""
    }

    catch (err) {
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}