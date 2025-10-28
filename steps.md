## Crear AWS EC2 Server



# https://docs.docker.com/engine/install/ubuntu/
# PASO 1
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# PASO 2
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# PASO 3
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# PASO 4
sudo systemctl status docker

# PASO 5
sudo chmod 666 /var/run/docker.sock
systemctl status docker

# PASO 6
docker login

# PASO 7
docker run -d --name sonarqubetest -p 9000:9000 sonarqube:community
docker ps


## CREAR EL REPO EN GITHUB
# Crea y publica las ramas stage y dev
git switch -c stage
git push -u origin stage

git switch -c dev
git push -u origin dev


# Añadir secretos en GitHub

En tu repo: Settings → Secrets and variables → Actions → New repository secret:

SONAR_TOKEN = el token generado en SonarQube.
SONAR_HOST_URL = URL de tu SonarQube.

Settings → Branches → Add rule
Require status checks to pass

http://54.172.125.224:9000/sessions/new?return_to=%2F
