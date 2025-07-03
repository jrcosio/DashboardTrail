# Dashboard Trail Sierra de Peñasagra - Corremos por Adriana


# Flet en Linux
sudo apt update
sudo apt install libmpv-dev libmpv2   # en Debian viejas es libmpv1

sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1


# Instalación de CUDA

sudo apt install build-essential

Instalación CUDA
https://developer.nvidia.com/cuda-toolkit

wget https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux.run
sudo sh cuda_12.8.0_570.86.10_linux.run

nano .bashrc
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH
source .bashrc

sudo nano /etc/ld.so.conf.d/cuda.conf
añadir: /usr/local/cuda-12.6/lib64
sudo ldconfig

------------------------------------------
Instalación CUDNN
https://developer.nvidia.com/cudnn-downloads

wget https://developer.download.nvidia.com/compute/cudnn/9.10.2/local_installers/cudnn-local-repo-ubuntu2404-9.10.2_1.0-1_amd64.deb
sudo dpkg -i cudnn-local-repo-ubuntu2404-9.10.2_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2404-9.10.2/cudnn-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cudnn
