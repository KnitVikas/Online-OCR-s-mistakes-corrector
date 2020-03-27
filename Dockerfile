FROM ubuntu:18.04

ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

WORKDIR /app

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y software-properties-common \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ /app

RUN chmod +x /tini && \
    pip3 install --no-cache-dir -r requirements.txt && \
    chmod +x health.sh && \
    touch demo_logs.log && \
    cd cython_utils && \
    python3 setup.py build_ext --inplace

ENTRYPOINT ["/tini", "--"]

CMD [ "python3", "main.py" ]
