FROM python:3.11

ARG USER=docker
ARG UID=1000
ARG USER_PASS=docker
ARG ROOT_PASS=root

RUN apt update && apt install -y alsa-utils pulseaudio sudo && \
    echo root:${ROOT_PASS} | chpasswd && \
    useradd -m -u ${UID} ${USER} && \
    echo ${USER}:${USER_PASS} | chpasswd && \
    echo "${USER} ALL=(ALL) ALL" >> /etc/sudoers

USER ${USER}