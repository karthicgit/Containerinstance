This is used to decompress files in OCI object storage using container instance

Build the docker image using the below command in OCI Cloudshell:
  docker login <region>.ocir.io and enter the username and authtoken as password
  
  `docker build -t cigzip:latest .`
  `docker tag cigzip:latest <target-tag>`
  `docker push <targettag>`

Create Container Instance using OCI Console,cli ,terraform etc 

You need to pass these two environment variables **BUCKET_NAME** and **PREFIX**
