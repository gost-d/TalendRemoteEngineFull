node {

    stage('Checkout') {
        checkout scm 
    }
    
    stage('Copy Talend Remote Engine files') {
        sh('curl -u "admin:admin123" -o "./Talend-RemoteEngine-V2.11.7.zip" "http://172.22.6.131:8081/repository/DEVOPS/talend_remote_engine/v/2.11.7/v-2.11.7.zip" ')
    }
    
    stage('Create infrastructure') {
        withCredentials([azureServicePrincipal('AzureJenkins')]) {
            
            sh('docker pull ghostd/talend:firsttry')
            
            if (params.ostype == 'windows') {
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook /root/windows/createVM.yaml')
            } else {
                sh('ssh-keygen -q -t rsa -N "" -f ./id_rsa <<<y >/dev/null 2>&1')
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend-Remote-Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook /root/ubuntu/createVM.yaml')

            }

        }   
    }

    stage('Install Talend Remote Engine') {
        withCredentials([azureServicePrincipal('AzureJenkins')]) {
            if (params.ostype == 'windows') {
                 sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --env ANSIBLE_HOST_KEY_CHECKING=False --rm ghostd/talend:firsttry ansible-playbook -i /root/windows/azure_rm.yaml --extra-vars "tre_version=$tre_version" /root/windows/installRemoteWindows.yaml')
            } else {
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend-Remote-Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook -i /root/ubuntu/azure_rm.yaml -u azureuser --private-key /root/id_rsa --extra-vars "tre_version=$tre_version" /root/ubuntu/installRemoteUbuntu.yaml')
            }
        }   
    }
} 
