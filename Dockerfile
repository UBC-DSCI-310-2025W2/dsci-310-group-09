FROM python:3.13-slim

WORKDIR /home/work

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    make \
    git \
    libgl1 \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pandas \
    scikit-learn \
    matplotlib \
    shap==0.49.1 \
    click \
    requests \
    jupyter \
    pyyaml

ARG QUARTO_VERSION=1.9.37
ARG TARGETARCH

RUN if [ "$TARGETARCH" = "arm64" ]; then QUARTO_ARCH="linux-arm64"; \
    elif [ "$TARGETARCH" = "amd64" ]; then QUARTO_ARCH="linux-amd64"; \
    else echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi \
    && wget -q "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.tar.gz" \
    && tar -xzf "quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.tar.gz" \
    && mv "quarto-${QUARTO_VERSION}" /opt/quarto \
    && ln -s /opt/quarto/bin/quarto /usr/local/bin/quarto \
    && rm "quarto-${QUARTO_VERSION}-${QUARTO_ARCH}.tar.gz" \
    && quarto --version

COPY . /home/work

ENV PYTHONPATH=/home/work

CMD ["bash"]