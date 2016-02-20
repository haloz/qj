from jenkinsapi.jenkins import Jenkins


def connectToJenkins(server_url):
    jenkins_instance = Jenkins(server_url)
    return jenkins_instance
