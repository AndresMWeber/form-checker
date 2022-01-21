<p align="center">
        <img width=200px height=200px src="https://raw.githubusercontent.com/AndresMWeber/form-checker/main/docs/logo.png" alt="Form Checker Logo" />
</p>

<div align="center">
    <a href="https://github.com/AndresMWeber/form-checker/actions/workflows/pipeline.yml">
        <img alt="GitHub CICD Action Status" src="https://github.com/AndresMWeber/form-checker/actions/workflows/pipeline.yml/badge.svg" />
    </a>
    <br />
    <a href="https://github.com/AndresMWeber/form-checker">
        <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg" />
    </a>
    <a href="https://github.com/AndresMWeber/form-checker/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/andresmweber/Cinegraph.svg" />
    </a>
    <a href="https://www.gnu.org/licenses/gpl-3.0">
        <img alt="License" src="https://img.shields.io/badge/License-GPLv3-blue.svg" />
    </a>
    <br />
    <a href="https://codecov.io/gh/AndresMWeber/form-checker">
        <img src="https://codecov.io/gh/AndresMWeber/form-checker/branch/main/graph/badge.svg?token=rQNFZEvfMu"/>
    </a>
    <a>
        <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/andresmweber/form-checker" />
    </a>
    <br />
</div>
<br>

<p align="center"> 
    Automatically generate a skeletal overlay for slow motion pose form critiques over videos.
    <br> 
</p>

<h3 align="center">
    <code>
    ·
    <a href="#installation">Installation</a>
    ·
    </code>
</h3>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About <a name = "about"></a>](#-about-)
- [🖥️ Screenshots <a name = "screenshots"></a>](#️-screenshots-)
- [💨 Quickstart <a name = "quickstart"></a>](#-quickstart-)
- [💾 Installation](#-installation)
  - [From GitHub Repo Clone](#from-github-repo-clone)
    - [Prerequsites](#prerequsites)
    - [Install](#install)
    - [Configure](#configure)
    - [Local](#local)
    - [Deploy](#deploy)
- [⛏️ Tech Stack <a name = "tech"></a>](#️-tech-stack-)
- [✍️ Authors <a name = "authors"></a>](#️-authors-)
- [🎉 Acknowledgements <a name = "acknowledgement"></a>](#-acknowledgements-)


## 🧐 About <a name = "about"></a>

A tool that creates a skeletal overlay for slow motion pose form critiques via cloud based python infrastructure.

## 🖥️ Screenshots <a name = "screenshots"></a>

<h2>Example</h2>

https://user-images.githubusercontent.com/1587270/149015534-822a8618-9037-4f9f-91ea-ffff29665856.mp4

## 💨 Quickstart <a name = "quickstart"></a>


## 💾 Installation
### From GitHub Repo Clone
#### Prerequsites

1. [Python](https://www.python.org/) and [Python Poetry](https://python-poetry.org/)
2. [Docker](https://www.docker.com/) To containerize the form checking function.
3. [Serverless](https://www.serverless.com/) For infrastructure deployment
4. [ffmpeg](https://www.serverless.com/) For local invocation
5. [AWS](https://console.aws.amazon.com/) For infrastructure hosting


#### Install
1. `poetry install` (To install in the top level directory always: `poetry config virtualenvs.in-project true`)
1. `npm install` - Installs Serverless framework

#### Configure
1. `aws profile` - Create an AWS profile or change `serverless.yml.provider.profile` to your own profile name (or delete the line for `[default]`)
2. `sls login` - Log in to serverless
3. [`add github secrets`](https://docs.github.com/en/actions/security-guides/encrypted-secrets) - Add the following repo secrets (to allow cloud deployment):
```shell
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
CODECOV_TOKEN
```
1. `create .env` - Optional configuration as needed. [Example .env file](.env.example)

2. `add github secrets` - If deploying using the GitHub Action workflow CI/CD you must [specify these secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) (ignore codecov token if you did not set up code coverage.):
```shell
AWS_ACCESS_KEY_ID
AWS_DEFAULT_REGION
AWS_SECRET_ACCESS_KEY
CODECOV_TOKEN
FC_EMAIL_DESTINATION # (in case you want your email address obscured from SCM.)
```
#### Local
1. Start a poetry virtual environment shell
```console
foo@bar:~$ poetry shell
```

2. Run the script on the local file:
```console
foo@bar:~$ form_check /path/to/your/file.mp4
```

3. You can also run the following to open a file browser using Tkinter:
```console
foo@bar:~$ form_check_ui
```

4. Finally you can find the outputted processed/compressed version in `~./tmp/*.mp4`

#### Deploy

Please note that deployment will be automatic if you set up the configuration properly and push to your own fork via GitHub Actions.

1. Create the domain for the AWS Api Gateway
```console
foo@bar:~$ sls create_domain
```

2. Deploys the serverless cloud infrastructure.
```console
foo@bar:~$ sls deploy -v
```

3. Now you will be able to upload a file using `${DOMAIN}/presigned`
```console
foo@bar:~$ curl -L -X POST 'subdomain.domain.com/presigned' \
-H 'Content-Type: application/json' \
--data-raw '{
    "filename": "test"
}'
```
Now you may upload a file using the response url and the upload lambda will trigger which will create a new video file in the s3 bucket.

## ⛏️ Tech Stack <a name = "tech"></a>

- [Python](https://www.python.org/) - Software Development
- [Poetry](https://python-poetry.org/) - Package Management
- [OpenCV](https://opencv.org/) - Image Processing
- [MediaPipe](https://google.github.io/mediapipe/) - Machine Learning Model/Solution
- [Serverless](https://www.serverless.com/) - Web Framework
- [AWS](https://aws.amazon.com/) - Cloud Infrastructure
- [pytest](https://docs.pytest.org/en/6.2.x/) - Testing Framework
- [CodeCov](https://about.codecov.io/) - Test Coverage Metrics

## ✍️ Authors <a name = "authors"></a>

<a href="https://github.com/andresmweber/">
    <img title="Andres Weber" src="https://github.com/andresmweber.png" height="50px">
</a>

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@FFMPEG](https://www.ffmpeg.org/) for providing amazing open source video solutions.
