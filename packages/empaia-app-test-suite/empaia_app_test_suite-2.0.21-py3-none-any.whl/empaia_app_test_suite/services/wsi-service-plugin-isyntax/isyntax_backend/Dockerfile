FROM registry.gitlab.com/empaia/integration/ci-docker-images/test-runner:0.1.38@sha256:d46c48a00a11c32f5a615a19a4d92e5ab25f8a1a61bebb642031e483c24b4f5c AS build0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY isyntax_backend /isyntax/isyntax_backend
COPY pyproject.toml /isyntax/pyproject.toml

WORKDIR /isyntax

RUN python3 -m venv .venv
RUN poetry build

FROM ubuntu:18.04@sha256:eb1392bbdde63147bc2b4ff1a4053dcfe6d15e4dfd3cce29e9b9f52a4f88bc74

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-pip python3-wheel unzip

COPY philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip

WORKDIR /isyntax

RUN unzip philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip \
    && cd philips-pathologysdk-2.0-ubuntu18_04_py36_research \
    && chmod 777 InstallPathologySDK.sh \
    && ./InstallPathologySDK.sh py3 -y \
    && cd .. \
    && rm -r philips-pathologysdk-2.0-ubuntu18_04_py36_research

COPY --from=build0 /isyntax/dist/*.whl /tmp
RUN pip3 install /tmp/*.whl

RUN mkdir /data

CMD ["python3", "-m", "isyntax_backend"]
