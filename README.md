# home-AI

## RUN


### Stop ollama if running
```bash
sudo systemctl stop ollama
```

### Install dependencies
```bash
npm i
```

### Run
```bash
npm run start
```

## Install GPU support

### Install NVIDIA repository
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
```

```bash
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

### Install NVIDIA Container Toolkit
```bash
sudo apt update && sudo apt install -y nvidia-container-toolkit
```

### Configure Docker to use it
```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

### Restart Docker
```bash
sudo systemctl restart docker
```

### Verify installation
```bash
docker info | grep -i runtime
docker run --rm --gpus all nvidia/cuda:12.3.1-base-ubuntu22.04 nvidia-smi
```

## Checks

### Check Model

```bash
docker exec -it homeai_ollama ollama run llama3.1:8b "Hello!"
```

### Check Redis

```bash
docker exec -it homeai_redis redis-cli ping
```

### Check Agents

```bash
docker logs homeai_agents
```

