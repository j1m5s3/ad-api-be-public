FROM python:3.7.16-slim
RUN apt-get update && apt-get install -y wget

#FROM python:3.7.16
#RUN apt-get update && apt-get install -y wget
#RUN apt-get update && apt-get install -y software-properties-common && \
#    add-apt-repository ppa:ethereum/ethereum && apt-get install solc

ARG SOLC_VERSION=v0.8.17
RUN wget --output-document /usr/local/bin/solc https://github.com/ethereum/solidity/releases/download/${SOLC_VERSION}/solc-static-linux \
    && chmod a+x /usr/local/bin/solc

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh"]
CMD ["run_api_server.sh"]