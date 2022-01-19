FROM 789539923770.dkr.ecr.us-east-1.amazonaws.com/fc-cv2-ffmpeg:latest

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
