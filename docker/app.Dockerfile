FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install poppler-utils -y
RUN apt-get install tesseract-ocr -y
RUN apt-get -y install cmake

## install conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda init

# activate base env
RUN echo ". /root/minicondsa3/etc/profile.d/conda.sh" >> ~/.bashrc
RUN . /root/miniconda3/etc/profile.d/conda.sh && conda activate base

# install torch
RUN conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y

# install MERI for parameter extraction
RUN pip install git+https://github.com/Novia-RDI-Seafaring/MERI@main

RUN conda install -c conda-forge pyfmi -y

# install fmu-gen-hex for fmu generation
RUN git clone https://github.com/Novia-RDI-Seafaring/fmu-gen-hex.git

RUN pip install /fmu-gen-hex

# Set the working directory
WORKDIR /fmu-gen-hex/demo

RUN pip install /fmu_gen_hex

ENV GRADIO_SERVER_NAME="0.0.0.0"

EXPOSE 7860

CMD ["bash", "-c", "source activate base && python demo.py"]