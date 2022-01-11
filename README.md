<p align="center">
        <img width=200px height=200px src="https://raw.githubusercontent.com/AndresMWeber/form-checker/main/docs/logo.png" alt="Form Checker Logo" />
</p>

<div align="center">
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
    A tool that creates a skeletal overlay for slow motion pose form critiques via cloud based python infrastructure.
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
    - [Deploy](#deploy)
- [⛏️ Tech Stack <a name = "tech"></a>](#️-tech-stack-)
- [✍️ Authors <a name = "authors"></a>](#️-authors-)
- [🎉 Acknowledgements <a name = "acknowledgement"></a>](#-acknowledgements-)


## 🧐 About <a name = "about"></a>

A CLI tool that creates a kaleidescope-esque gradient image of your favorite movie.

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
1. `aws profile` - Creates an AWS profile named `aw` or change `serverless.yml.provider.profile` to your own profile name (or delete the line for default)
1. `sls login` - Logs in to serverless
1. `create .env` - Configure as needed, defaults will be set otherwise.
```shell
DEBUG=form-checker:*
UPLOAD_BUCKET=form-checker-storage
```

#### Deploy

1. Create the domain for the AWS Api Gateway
    ```console
    foo@bar:~$ sls create_domain
    ```
1. Deploys the serverless cloud infrastructure.
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

## ✍️ Authors <a name = "authors"></a>

<a href="https://github.com/andresmweber/">
    <img title="Andres Weber" src="https://github.com/andresmweber.png" height="50px">
</a>

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@FFMPEG](https://www.ffmpeg.org/) for providing amazing open source video solutions.
