<p align="center">
        <img width=200px height=200px src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/docs/logo.png" alt="Cinegraph Logo" />
</p>

<div align="center">
    <a href="https://badge.fury.io/py/cinegraph">
        <img alt="PyPi Repo" src="https://badge.fury.io/py/cinegraph.svg" />
    </a>
    <br />
    <a href="https://github.com/AndresMWeber/cinegraph/actions/workflows/py-cicd.yml">
        <img alt="GitHub CICD Action Status" src="https://github.com/AndresMWeber/Cinegraph/actions/workflows/py-cicd.yml/badge.svg" />
    </a>
    <a href="https://github.com/AndresMWeber/cinegraph/actions/workflows/pypi-upload.yml">
        <img alt="GitHub PyPi Deploy Action Status" src="https://github.com/AndresMWeber/cinegraph/actions/workflows/pypi-upload.yml/badge.svg" />
    </a>
    <br/>
    <a href="https://github.com/AndresMWeber/Cinegraph">
        <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg" />
    </a>
    <a href="https://github.com/AndresMWeber/Cinegraph/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/andresmweber/Cinegraph.svg" />
    </a>
    <a href="https://www.gnu.org/licenses/gpl-3.0">
        <img alt="License" src="https://img.shields.io/badge/License-GPLv3-blue.svg" />
    </a>
    <br />
    <a href="https://pypi.python.org/pypi/cinegraph">
        <img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/cinegraph.svg" />
    </a>
    <a href="https://codecov.io/gh/AndresMWeber/cinegraph">
        <img src="https://codecov.io/gh/AndresMWeber/cinegraph/branch/main/graph/badge.svg?token=rQNFZEvfMu"/>
    </a>
    <a>
        <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/andresmweber/Cinegraph" />
    </a>
    <br />
</div>
<br>

<p align="center"> A CLI tool that creates a kaleidescope-esque gradient image of your favorite movie.
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
  - [Flags](#flags)
- [💾 Installation](#-installation)
  - [From PyPi](#from-pypi)
    - [Install steps](#install-steps)
  - [From GitHub Repo Clone](#from-github-repo-clone)
    - [Prerequsites](#prerequsites)
    - [Install steps](#install-steps-1)
- [⛏️ Tech Stack <a name = "tech"></a>](#️-tech-stack-)
- [✍️ Authors <a name = "authors"></a>](#️-authors-)
- [🎉 Acknowledgements <a name = "acknowledgement"></a>](#-acknowledgements-)


## 🧐 About <a name = "about"></a>

A CLI tool that creates a kaleidescope-esque gradient image of your favorite movie.

## 🖥️ Screenshots <a name = "screenshots"></a>

<div align=center>
<h2>Total Recall</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/(2012)%20Total%20Recall_c600_b5_r1920x1080_f1_fm50.jpg" />

<h2>Elysium</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/(2013)%20Elysium_c600_b5_r1920x1080_f1_fm50.jpg" />

<h2>Pacific Rim</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/(2013)%20Pacific%20Rim_c600_b5_r1920x1080_f1_fm50.jpg" />

<h2>Star Trek Into Darkness</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/(2013)%20Star%20Trek%20Into%20Darkness_c600_b5_r1920x1080_f1_fm50.jpg" />

<h2>Edge of Tomorrow</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Edge_of_Tomorrow_c600_b5_r1920x1080_f1_fm50.jpg" />

<h2>Example Write Frames</h2>
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_1052.jpg" />
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_2367.jpg" />
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_108619.jpg" />
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_122821.jpg" />
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_150699.jpg" />
<img src="https://raw.githubusercontent.com/AndresMWeber/cinegraph/main/examples/Elysium/f_157274.jpg" />
</div>

## 💨 Quickstart <a name = "quickstart"></a>
If you are running from the repository Cinegraph can be invoked using:
``` bash
$ poetry run cinegraph 
```
or if you are running from a pip installation you should have the CLI command available:
``` bash
$ cinegraph
```

If you do not provide any positional arguments to specify input files it will automatically open a [Tkinter](https://docs.python.org/3/library/tkinter.html) file picker, you need to have a capable display window provider (if using WSL [Xserver](https://www.x.org/releases/X11R7.7/doc/man/man1/Xserver.1.xhtml) is a great option.)

Additionally you can run it with the following flags:
### Flags
```
NAME
    poetry run cinegraph
    cinegraph

SYNOPSIS
    poetry run cinegraph <flags> [FILES]...
    cinegraph <flags> [FILES]...
POSITIONAL ARGUMENTS
    FILES
        The files that you want to be processed.

FLAGS
    -c,--colors=COLORS
        Number of colors in the Cinegraph
        Example Input:
            100
    -b,--blur=BLUR
        Blur amount for the Cinegraph
        Example Input:
            5
    -r,--resolution=RESOLUTION
        Resolution for the Cinegraph
        Example Input:
            1000,1200
    -t,--template=TEMPLATE
        International Standard Paper Format Name
        Available Options:
            A0 - 	    33-1/8 x 46-13/16 in	    841 x 1188 mm
            A1 - 	    23-3/8 x 33-1/8 in	        594 x 841 mm
            A2 - 	    16-1/2 x 23-3/8 in	        420 x 594 mm
            A3 - 	    11-3/4 x 16-1/2 in	        297 x 420 mm
            A4 - 	    8-1/4 x 11-3/4 in	        210 x 297 mm
            A5 - 	    5-7/8 x 8-1/4 in	        148 x 210 mm
            A6 - 	    4-1/8 x 5-7/8 in	        105 x 148 mm
            A7 - 	    2-15/16 x 4-1/8 in	        74 x 105 mm
            A8 - 	    2-1/16 x 2-15/16 in	        52 x 74 mm
            LETTER  -   8.5 x 11 in                 215.9 x 279.4 mm
            SMALL	-   11 x 17 in                  279.4 x 431.8 mm
            MEDIUM	-   18 x 24 in                  457.2 x 609.6 mm
            LARGE	-   24 x 36 in                  609.6 x 914.4 mm
    -d,--dpi=DPI
        The desired print resolution, must be specified as a whole number
        e.g. 72
    -f,--frame=FRAME
        Add a white border + frame for the Cinegraph
    -m,--margin=MARGIN
        Set the margin (in pixels) for the border around the Cinegraph
        e.g. 25
    -w,--write_frames=WRITE_FRAMES
        Output the frames with a center square that denotes the dominant color.
```

## 💾 Installation

### From PyPi
#### Install steps
1. Install using pip: `pip install cinegraph`
2. You will then have the CLI command available to you:
``` bash
$ cinegraph
```

### From GitHub Repo Clone
#### Prerequsites

1. [Python](https://www.python.org/) and [Python Poetry](https://python-poetry.org/) is installed

#### Install steps
1. `poetry install` (To install in the top level directory always: `poetry config virtualenvs.in-project true`)


## ⛏️ Tech Stack <a name = "tech"></a>

- [Python](https://www.python.org/) - Software Development
- [Poetry](https://python-poetry.org/) - Package Management
- [OpenCV](https://opencv.org/) - Image Processing
- [Fire](https://github.com/google/python-fire) - CLI Framework

## ✍️ Authors <a name = "authors"></a>

<a href="https://github.com/andresmweber/">
    <img title="Andres Weber" src="https://github.com/andresmweber.png" height="50px">
</a>

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@FFMPEG](https://www.ffmpeg.org/) for providing amazing open source video solutions.
- [The Colors of Motion](https://thecolorsofmotion.com/) for being the inspiriation and the idea that I tried my best to mimic. 
