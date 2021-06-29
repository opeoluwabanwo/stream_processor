
FROM openjdk:8u292-slim
COPY --from=python:3.8-slim / /

RUN apt-get update -qqy && apt-get install -qqy curl git gnupg wget

# Install Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

# Install Poetry
RUN pip install -U pip && \
    pip --no-cache-dir install poetry poetry-setup

# Install Terraform
RUN cd $HOME
RUN apt-get install unzip
RUN rm -rf terraform*
RUN wget https://releases.hashicorp.com/terraform/0.14.2/terraform_0.14.2_linux_amd64.zip
RUN unzip terraform_0.14.2_linux_amd64.zip
RUN rm terraform_0.14.2_linux_amd64.zip
RUN mv terraform /usr/local/bin/
RUN terraform --version

# Install the stream-processor app as a package
COPY . /app
WORKDIR /app
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# set timezone
RUN cd $HOME
RUN echo "UTC" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

VOLUME ["/root/.config"]
