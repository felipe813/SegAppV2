#!groovy
node {

    try {
        stage 'Checkout'
            checkout scm

        stage 'Deploy'
            try{
                sh "docker image rm django"
                sh "docker build --tag django ."
            } catch (err) {  
                sh "docker build --tag django ."
            }
	    
        stage 'Test'
            sh "python3 manage.py test"

        stage 'Publish results'
            try{
                containerID = sh (
                    script: "docker container ls -aq", 
                    returnStdout: true
                ).trim()
                sh "docker container stop ${containerID}"
                sh "docker container rm ${containerID}"
                sh "docker run -d --name django -p 8013:8013 django"
            } catch (err) {  
                sh "docker run -d --name django -p 8013:8013 django"
            }           
            
    }

    catch (err) {  
        throw err
    }

}