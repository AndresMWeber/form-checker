FROM public.ecr.aws/lambda/python:3.9	


ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

WORKDIR /
RUN yum update -y
RUN yum install -y tar xz

# Install ffmpeg from local vendor distribution
COPY ffmpeg.tar.xz .
RUN ls
RUN tar -xf ffmpeg.tar.xz
RUN mv ffmpeg-*-amd64-static/ffmpeg /usr/bin

COPY form_checker ./form_checker
COPY poetry.lock pyproject.toml ./
RUN pip3.9 install --upgrade pip
RUN pip3.9 install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

CMD ["form_checker.handlers.upload.handler"]

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
