FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN apt-get update \
    && apt-get install -y git curl python3 python3-dev python3-pip python3-venv \
    && echo "export PATH=$PATH:/root/.local/bin" >> /root/.bashrc \
    && echo "export PATH=$PATH:/home/${USERNAME}/.local/bin" >> /home/${USERNAME}/.bashrc

ENV SHELL=/bin/bash

WORKDIR /workspaces

USER ${USERNAME}
