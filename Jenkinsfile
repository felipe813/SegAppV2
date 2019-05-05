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
	    
        stage 'Publish results'
            try{
                sh "docker container stop \$ '(docker container ls -aq)'"
                sh "docker container rm \$ '(docker container ls -aq)'"
                sh "docker run -d --name django -p 8013:8013 django"
            } catch (err) {  
                sh "docker run -d --name django -p 8013:8013 django"
            }           
            
    }

    catch (err) {  
        throw err
    }

}