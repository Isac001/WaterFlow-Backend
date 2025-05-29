
# **WaterFlow - Backend**

# How to install docker on your machine 

### Install git:

```bash
sudo apt-get install git
```

### Clone the repository and run the following command:

```bash
git clone https://github.com/Isac001/WaterFlow-Backend.git &&
cd water_flow_backend 
```


```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Start the docker service:
```bash
sudo service docker start
```

### Run the following command to start the docker containers:

```bash
docker-compose up -d
```



# Installation of the Database Solution on PostgreSQL (Required)

_For Ubuntu_ OR _WSL_:

Dependency Installation

```bash
sudo apt update &&
sudo locale-gen pt_BR.UTF-8 &&
sudo apt install git python3-pip postgresql postgresql-client
```


### Install the following libraries for the solution:

```bash
python3 -m pip install -r requirements.txt
```


To update the server and install the main dependencies related to the project, use the following commands:


```bash
sudo service postgresql start &&
sudo -u postgres psql
```

Then:

```bash
CREATE DATABASE waterflow;
CREATE USER waterflow WITH PASSWORD 'root';
GRANT ALL PRIVILEGES ON DATABASE waterflow TO waterflow;
```

After configuring this part, use the following command to exit the terminal:

```bash
\q
```

To finalizate the database configuration, execute:

```bash
sudo -u postgres psql -d waterflow

# IN DATABASE RUNNIGN:
GRANT ALL PRIVILEGES ON SCHEMA public TO waterflow;
```

### Now enter the directory where the project root is located by using:

```bash
cd ~/water_flow_backend
```

Install the requirements of the project using the following command:

```bash
pip install -r requirements.txt
```

### Now, this part is to test de API, firstone build the containers

```bash
docker compose up
docker exec -it water_flow_backend sh
```

Afert, use someone the commands to create mock data and run tasks:

Commands to generate mock data and running tasks:
```bash
python3 manage.py create_alert
python3 manage.py create_daily
python3 manage.py create_weekly
python3 manage.py create_monthly
python3 manage.py create_bimonthly
python3 manage.py loadfixtures
```

Once the installation process is completed, you can access the backend of the solution from a web browser in two ways:

Locally, using the address _http://localhost:8000_.

Remotely, using the server's IP address _http://999.999.999.999:8000_.
