node {

    stage('Checkout') {
        checkout scm 
    }
    
    stage('Copy Talend Remote Engine files') {
        
        withCredentials([usernamePassword(credentialsId: 'nexus_user', usernameVariable: 'nexus_username', passwordVariable: 'nexus_password')]) {
            sh('curl -u "$nexus_username:$nexus_password" -o "./Talend-RemoteEngine-V${tre_version}.zip" "http://172.22.6.131:8081/repository/devops/talend_remote_engine/v/${tre_version}/v-${tre_version}.zip" ')
        }
    }

    stage('Create Talend Remote Engine') {
        sh('docker pull ghostd/python:1.0')
        sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --rm ghostd/python:1.0 python3 /root/createEng.py')
    }

    
    
    stage('Create infrastructure') {
        withCredentials([azureServicePrincipal('AzureJenkins')]) {
            
            sh('docker pull ghostd/talend:firsttry')
            
            if (params.ostype == 'windows') {
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook /root/${ostype}/createVM.yaml')
            } else {
                sh('echo "yes" | ssh-keygen -q -t rsa -N "" -f ./id_rsa')
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook /root/${ostype}/createVM.yaml')

            }

        }   
    }

    stage('Install Talend Remote Engine') {
        withCredentials([azureServicePrincipal('AzureJenkins')]) {
            if (params.ostype == 'windows') {
                 sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --env ANSIBLE_HOST_KEY_CHECKING=False --rm ghostd/talend:firsttry ansible-playbook -vvv -i /root/${ostype}/azure_rm.yaml --extra-vars "tre_version=$tre_version" /root/${ostype}/installRemoteWindows.yaml')
            } else {
                sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Remote_Engine_Create_Install:/root --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm ghostd/talend:firsttry ansible-playbook -vvv -i /root/${ostype}/azure_rm.yaml -u azureuser --private-key /root/id_rsa --extra-vars "tre_version=$tre_version ansible_host_key_checking=false" /root/${ostype}/installRemoteUbuntu.yaml')
            }
        }   
    }
} 
