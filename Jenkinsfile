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
            }           
            sh "docker run -d --name django -p 8013:8013 django"
    }

    catch (err) {  
        throw err
    }

}