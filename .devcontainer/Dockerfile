FROM quay.io/jupyter/minimal-notebook

USER root
RUN apt-get update && apt-get install -y build-essential

USER jovyan
RUN mkdir /home/jovyan/temp
WORKDIR /opt


COPY ./requirements.txt ./requirements.txt
RUN pip install --cache-dir=/home/jovyan/temp -r requirements.txt
# RUN pip install --force-reinstall "chromadb==0.5.0"

