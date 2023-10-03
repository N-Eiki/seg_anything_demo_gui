#!/bin/bash
# export DISPLAY="$(grep nameserver /etc/resolv.conf | sed 's/nameserver //'):0.0"
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
xhost +
docker run --gpus all -it --rm --privileged\
    --env="DISPLAY=host.docker.internal:0" \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /home/eiki/seg_anything_demo/mnt_workdir:/mnt\
    --name seg_anything poetry_docker_py39 bash 

#   poetry run python scripts/amg.py --checkpoint /mnt/ckpt/sam_vit_h_4b8939.pth --model-type default --input /mnt/imgs/ノビル.jpg --output /mnt/output/

# import matplotlib.pyplot as plt;plt.plot([0, 1, 2]);plt.show()