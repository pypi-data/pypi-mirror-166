#!/usr/bin/env bash

# A script used to install NVIDIA HGX A100 Softwares

pre_install_checker() {
  # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions
  echo "========================================================="
  echo "Check if the system satisfy the pre-install requirements."
  echo "========================================================="
  # Verify your GPU is CUDA-capable
  res=`lspci | grep -i nvidia | wc -l`
  if [ $res -eq 0 ]; then
    echo "No CUDA-capable GPUs found. Please make sure you have NVIDIA GPUs installed." 
    echo "Or update the PCI hardware database that Linux maintains by entering update-pciids (generally found in /sbin) at the command line."
    exit 1
  fi

  # Verify You Have a Supported Version of Linux
  OS_NAME=`cat /etc/*release | grep "^NAME=" | sed s/NAME=//`
  if [ $OS_NAME != "\"Ubuntu\"" ]; then
    echo "We only support the Ubuntu OS."
    exit 1
  fi

  # Verify the System Has gcc Installed
  ver=`gcc --version`
  if [ $? -ne 0 ]; then
    echo "Your system has no gcc installed. We will install it for you."
    sudo apt-get install -y gcc
  fi

  echo "Install some frequently used packages"
  DEBIAN_FRONTEND=noninteractive apt-get -yq --ignore-missing install unzip \
  git wget axel net-tools vim htop libglib2.0-0 python3 python3-pip alsa-utils \
  intel-mkl numactl libnuma-dev

  echo "Install kernel headers"
  apt-get install linux-headers-$(uname -r)

  # Setup the GPG keys
  ## Remove outdated Signing Key
  apt-key del 7fa2af80
  ## Install the new one
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g') \
  && wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-keyring_1.0-1_all.deb \
  && dpkg -i cuda-keyring_1.0-1_all.deb && apt-get update
  ## Set up the CUDA network repository and the repository priority
  #distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g') \
  #&& wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-$distribution.pin \
  #&& sudo mv cuda-$distribution.pin /etc/apt/preferences.d/cuda-repository-pin-600

  echo "Pre-install check Passed."
  echo ""
  echo ""
}

install_cuda_toolkit() {
  echo "========================================================="
  echo "Install CUDA Toolkit."
  echo "========================================================="
  wget https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux.run
  sh ./cuda_11.6.2_510.47.03_linux.run --silent --driver --toolkit --samples
  echo "export LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" >> ~/.bashrc
  echo "export PATH=/usr/local/cuda-11.6/bin${PATH:+:${PATH}}" >> ~/.bashrc

  echo "CUDA Toolkit Installed."
  echo ""
  echo ""
}

install_cuda_drivers_fabricmanager() {
  # Install cuda-drivers-fabricmanager
  sudo apt-cache madison cuda-drivers-fabricmanager-510
  sudo apt-get install -y cuda-drivers-fabricmanager-510
  sudo systemctl status nvidia-fabricmanager.service
  sudo systemctl start nvidia-fabricmanager.service
  nvidia-smi topo -m
}

install_nvidia_nscq() {
  # Setup the library using the libnvidia-nscq package.
  sudo apt-get install -y libnvidia-nscq-510
  ls -ol /usr/lib/x86_64-linux-gnu/libnvidia-nscq*
}

uninstall_cuda_toolkit() {
  sudo apt-get --purge remove "*cuda*" "*cublas*" "*cufft*" "*cufile*" "*curand*" \
    "*cusolver*" "*cusparse*" "*gds-tools*" "*npp*" "*nvjpeg*" "nsight*"
  # Uninstall nvidia driver
  sudo apt-get --purge remove "*nvidia*"
  sudo apt-get autoremove
}

post_setup() {
  echo "export LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}" >> ~/.bashrc
  echo "export PATH=/usr/local/cuda-11.7/bin${PATH:+:${PATH}}" >> ~/.bashrc
}

pre_install_checker
install_cuda_toolkit
install_cuda_drivers_fabricmanager
install nvidia_nscq
