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
RUN yum install -y wget
RUN wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && yum install -y epel-release-latest-7.noarch.rpm
# RUN yum -y --enablerepo=extras install epel-release

# Build OpenCV from Source
RUN yum install -y tar xz make unzip gcc gcc-c++ cmake3 gtk3-devel
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.5.zip
RUN unzip opencv.zip && rm opencv.zip
RUN mv opencv-* opencv

RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.5.zip
RUN unzip opencv_contrib.zip && rm opencv_contrib.zip
RUN mv opencv_contrib-* opencv_contrib
RUN mkdir /opencv/build

ENV PATH="/sbin:${PATH}"

WORKDIR /opencv/build
RUN cmake3 -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D BUILD_SHARED_LIBS=NO \
    -D WITH_FFMPEG=ON \
    -D BUILD_opencv_python3=ON \ 
    -D BUILD_EXAMPLES=OFF ..
RUN make -j`nproc` && make install
RUN ln -s /usr/local/lib/python3.7/site-packages/cv2  /usr/lib/python3.7/site-packages/
RUN ln -s /usr/local/lib/python3.7/site-packages/cv2 /var/lang/lib/python3.9/site-packages
ENV PKG_CONFIG_PATH $PKG_CONFIG_PATH:/usr/local/lib/pkgconfig/
RUN echo '/usr/local/lib/' >> /etc/ld.so.conf.d/opencv.conf && ldconfig

# Build FFMPEG 
# WORKDIR /
# RUN yum install -y --enablerepo=epel git yasm-devel yasm autoconf automake bzip2 bzip2-devel freetype-devel gcc gcc-c++ libtool pkgconfig zlib-devel
# RUN git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg
# WORKDIR /ffmpeg
# RUN ./configure --enable-nonfree --enable-pic --enable-shared
# RUN make && make install

# http://glidingphenomena.blogspot.com/2020/02/how-to-fix-error-requires.html
RUN yum install -y libwayland-client
RUN wget http://mirror.centos.org/centos/7/os/x86_64/Packages/libva-1.8.3-1.el7.x86_64.rpm 
RUN rpm -i libva-1.8.3-1.el7.x86_64.rpm
# https://serverfault.com/questions/862461/why-i-cant-install-ffmpeg-on-centos-7
RUN rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
RUN rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
RUN yum install -y --enablerepo=epel,nux-dextop  ffmpeg ffmpeg-devel

# Copy + Install project 
WORKDIR /
COPY form_checker ./form_checker
COPY poetry.lock pyproject.toml ./
RUN pip3.9 install --upgrade pip && pip3.9 install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Verify installations
RUN ffmpeg -version && poetry shell && python -c "import cv2; print(cv2.__version__)"

CMD ["form_checker.handlers.upload.handler"]

# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
