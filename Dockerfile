FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    net-tools \
    iputils-ping \
    tcpdump \
    nmap \
    hping3 \
    tor \
    proxychains \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

RUN chmod +x src/core/killer.py

CMD ["python3", "src/core/killer.py", "--mode", "ultimate", "--threads", "10000000"]
