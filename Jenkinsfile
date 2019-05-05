#!groovy
node {

    try {
        stage 'Checkout'
            checkout scm

        stage 'Deploy'
            sh "docker build --tag django ."
	    
        stage 'Publish results'
            try{
                sh "docker container stop \$5 '(docker container ls -aq)'"
                sh "docker container rm \$5 '(docker container ls -aq)'"
            } catch (err) {  
                slackSend color: "good", message: "No hay contenedores que borrar "
            }           
            sh "docker run -d --name django -p 8013:8013 django"
    }

    catch (err) {  
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
        throw err
    }

}