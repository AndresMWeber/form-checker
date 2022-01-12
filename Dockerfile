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

# Build OpenCV from Source
RUN yum install cmake gcc-c++ gtk3-devel -y
RUN wget opencv.zip https://github.com/opencv/opencv/archive/4.5.5.zip
RUN unzip opencv.zip
RUN rm opencv.zip

RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.5.zip
RUN unzip opencv_contrib.zip
RUN rm opencv_contrib.zip
RUN cd opencv-*

RUN mkdir build
RUN cd build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=~/local \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.2/modules \
    -D BUILD_SHARED_LIBS=NO \
    -D WITH_FFMPEG=ON \
    -D BUILD_opencv_python2=ON \ 
    -D BUILD_EXAMPLES=OFF ..

RUN cd /
COPY form_checker ./form_checker
COPY poetry.lock pyproject.toml ./
RUN pip3.9 install --upgrade pip
RUN pip3.9 install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

CMD ["form_checker.handlers.upload.handler"]

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
