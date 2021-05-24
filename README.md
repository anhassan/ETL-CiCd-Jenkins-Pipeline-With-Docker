# Continuous Integration/Continuous Deployment(CI/CD) ETL Pipeline in Jenkins with Docker
This project automates the building and deployment of python based ETL using Jenkins as the continuous integration server and Docker for containerization with Docker Hub acting as the deployment sink. Git is used as the source code management (SCM) system and polling is enabled in the Jenkins server to ensure that when ever a new commit is made, a new docker image corresponding to the commit is deployed on Docker Hub.

# Jenkins Installation and Docker Integration inside Jenkins Docker Container
Installing Jenkins and instantiating docker container is a walk in the park. It can be done easily using the following command:
```docker
docker run -p 8080:8080 -p 50000:50000 -v 
<host_os_dir_path>:/var/jenkins_home jenkins/jenkins:lts-jdk11
```
However, things become really tricky when we want to spin up docker client within a Jenkins container so that the docker client present within the Jenkins container can communicate with the docker daemon on the host machine . In summary, we would have to follow the steps below:

1. Install Docker CLI in Jenkins Container
2. Communicate with the docker daemon running on the host machine
3. Establish a way to grant appropriate permission to the container so that it can talk to the docker daemon

In order to perform the above steps we would require to:

1. Install a custom docker image of Jenkins using the Dockerfile below:
```docker
FROM jenkins/jenkins:lts
USER root
RUN curl -sSL https://get.docker.com/|sh
USER jenkins
```
The command `curl -sSL https://get.docker.com/|sh` is used to download docker CLI within the new custom Jenkins image.

2. Build the custom Jenkins image using the above Dockerfile by navigating to the directory where the Dockerfile is placed and by using the following command:
```docker
 docker build --tag <custom_image_name> .
```
3. Grant appropriate permissions to the container using the following command
```docker
sudo chown -R 1000:1000 /var/jenkins_home
sudo chmod 666 /var/run/docker.sock
```
4. Spin up the Jenkins container with embedded docker CLI using the following docker run command:
```docker
docker run --name jenkins -d -p 8080:8080 -p 50000:50000
 --group-add 0 -v /var/jenkins_home:/var/jenkins_home
  -v /var/run/docker.sock:/var/run/docker.sock 
  <custom_image_name>
```
`docker.sock` is a unix file, the docker daemon listens to this file and responds to all the commands that are sent through CLI. This the way the Jenkins container would be able to communicate with docker daemon on the host machine.

# CI/CD Pipeline Design
The pipeline design is fairly simple. The Jenkins CI server will keep on listening to the repository it is bind to. Whenever a new commit is made to the Jenkins bind repository, a job would be triggered. This job would result in building of a new docker image corresponding to the current commit. The latest image built will finally be pushed to Docker Hub. All this automation is done using a Jenkinsfile which contains the information about the bind SCM repository as well as the Docker Hub credentials and docker image details. The below diagram clarifies the workflow:

<p align="center">
  <img src="/assets/cicd_etl_diagram.png" />
</p>


# Jenkins Pipeline
In order to build a pipeline in Jenkins we would chose the pipeline option among all the options including Freestyle project, Muti-branch pipeline etc. Now, in order to make sure that Jenkins Server keeps on listening to the desired repository for changes, we would choose Poll SCM option in the Build Triggers section of the pipeline with `* * * * *` as the cron pattern in order to check for a change every single minute. In the Pipeline options, we would choose Pipeline script from SCM as the Definition, SCM as Git, add the repository URL, keep the branch specifier as empty and uncheck the Lightweight checkout option.  Finally we would add the DockerHub credentials using the Jenkins Credential Manager having an id of `dockerHubCredentials` which are red in the Jenkinsfile. The following screenshots below will explain the required options chosen:

<p align="center">
  <img src="/assets/build_triggers.png" />
</p>

<p align="center">
  <img src="/assets/pipeline_options.png" />
</p>



# Validating Pipeline & Extracting ETL Results
The following steps would be used to verify the working of the pipeline and to fetch the results of the ETL.
1. Pull the docker image created via the Jenkins pipeline using the following command:
```docker
docker pull <etl_image_name>
```
2. Run the image and bind a volume to the run command to get the ETL output data using the following command:
```docker
docker run --rm 
-v $(pwd)/<host_directory>:<container_directory> <image_name>
```
The `<container_directory>` in the above command is the directory created in the Dockerfile of the ETL using the command `RUN  mkdir  -p  /etl/data` specifically for storing ETL output.

3. Explore the contents of the ETL output using the following commands:
```bash
cd <host_directory>
cat <etl_output_file_name>
```
