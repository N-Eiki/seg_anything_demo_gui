# FROM ubuntu:20.04
# FROM nvidia/cuda:12.1.1-devel-ubuntu20.04
FROM nvidia/cuda:11.7.0-devel-ubuntu20.04

# ENV
# ENV USE_OPENMP 1

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# apt-get
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        git \
        cmake\
        wget \
        vim \
        lsb-release \
        byobu\
        tmux\
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        libgl1-mesa-dev\
        x11-apps



#python install
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        python3.9 \
        python3.9-dev \
        python3-pip \
        python3.9-venv\
        python3-tk

### windows
RUN apt-get update -y\
 && apt-get install x11-apps -y
ENV DISPLAY host.docker.internal:0.0

RUN useradd -ms /bin/bash xuser


# コンテナにアクセスした際のデフォルトディレクトリ
WORKDIR workdir

# poetryのインストール先の指定
ENV POETRY_HOME=/opt/poetry
# poetry環境の作成
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry 

RUN poetry new poetry_seg_anything
WORKDIR /workdir/poetry_seg_anything
COPY requirements.txt .

RUN cat requirements.txt | xargs poetry add
# RUN poetry add $( cat requirements.txt )
RUN rm requirements.txt
RUN git clone https://github.com/facebookresearch/segment-anything.git

WORKDIR /workdir/poetry_seg_anything/segment-anything