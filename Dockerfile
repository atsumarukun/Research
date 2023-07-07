FROM python:3.11

RUN apt update && apt -y install portaudio19-dev && \
    pip install numpy matplotlib pyaudio tensorflow keras
