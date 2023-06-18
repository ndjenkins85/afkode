# AFKode - Speak it, Save it, AFKode it!

AFKode allows users to interact with AI and file system using only voice, allowing you to work away from keyboard.
Works on iPhone with pythonista, or on MacOS.
Powered by Whisper and ChatGPT.

This project was inspired by long walks on the beach while ruminating and organizing ones thoughts.

Users of this program should be comfortable using pythonista/python.
You are required to BYO OpenAI secret key in variable `OPENAI_KEY` using environment variables or within `afkcode/secrets.py`.

Key features:

- Detection of start/stop dictation for transcription
- Uses ChatGPT create smart file naming for your notes

Interfaces:

* At home: Supports MacOS with base speakers/microphone or AirPods. May not work with other bluetooth headsets like Bose headphones.
* Out and about: Supports Pythonista iOS with base speakers/microphones, or plugged in lightning wired heaphones. Bluetooth headsets like AirPods and Bose headphones currently not working.

## Contents

* [Instructions for users](#instructions-for-users)
  * [Installation](#installation)
  * [Usage documentation](#usage-documentation)
  * [Bug reports](#bug-reports)
* [Instructions for developers](#instructions-for-developers)
  * [Poetry](#environment-1-poetry)
  * [Testing with Nox](#testing-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
* [Contributors](#contributors)

## Instructions for users

The following are the quick start instructions for using the project as an end-user.

Follow the [Instructions for developers](#instructions-for-developers) to set up the virtual environment and dependency management.

### Installation

MacOS requirements:

- Python 3.8
- ffmpeg for mp3 text-to-speech, `brew install ffmpeg`


Note: Instructions marked with %% are not functioning and are for demo purposes only.

Install the project using pip %%:

```bash
pip install afkode
```

To replicate the data transformations and model results, run the following commands from the project root.
These should be run from the `poetry shell`, or `conda` environment, or with the `poetry run` prefix.
```bash
python -m afkode.run
```

### Usage documentation

The user guides can be found on [github pages](https://ndjenkins85.github.io/afkode).
This includes overview of features, discussion of `afkode` framework, and API reference.

### Bug reports

Please raise an [issue](https://github.com/ndjenkins85/afkode/issues) with `bug` label and I will look into it!

## Instructions for developers

The following are the setup instructions for developers looking to improve this project.
For information on current contributors and guidelines see the [contributors](#contributors) section.
Follow each step here and ensure tests are working.

### Poetry

[Poetry](https://python-poetry.org/docs/) handles virtual environment management, dev and optional extra libraries, library development, builds and publishing.

Check the poetry website for the latest instructions on how to install poetry.
You can use the following command on OS/linux to install poetry 1.1.9 used in this project.

```bash
curl -sSL https://install.python-poetry.org | python - --version 1.1.9
```

It is recommended to set virtual environment creation to within project using the following command.
This adds a `.venv` directory to project to handle cache and virtual environment.
```bash
poetry config virtualenvs.in-project true
```

You can set up the virtual environment in the repo using the following command.
Make sure that any other virtual environments (i.e. `conda deactivate`) are deactivated before running.

```bash
poetry install
```

Troubleshooting: You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

When the environment is correctly installed, you can enter the virtual environment using `poetry shell`. Library can be built using `poetry build`.

### Testing with Nox

[Nox](https://nox.thea.codes/en/stable/index.html) is a command-line tool that automates testing in multiple Python environments, similar to tox, Makefiles or scripts. Unlike tox, Nox uses a standard Python file for configuration.

Here it is used for code quality, testing, and generating documentation.

The following command can be used to run mypy, lint, and tests.
It is recommended to run these before pushing code, as this is run with Github Actions.
Some checks such as black are run more frequently with [pre-commit](#code-formatting-with-pre-commit).

```bash
poetry run nox
```

Local Sphinx documentation can be generated with the following command.
Documentation publishing using Github Actions to Github pages is enabled by default.

```bash
poetry run nox -s docs
```

Other available commands include:

```bash
poetry run nox -rs coverage
```

### Code formatting with Pre-commit

[Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks.

It intercepts the `git commit` command to run checks of staged code before the commit is finalized.
The checks are specified in `.pre-commit-config.yaml`.
Checks in use are quick, pragmatic, and apply automatic formatting checks.
If checks fail, it is usually only a matter of re-staging the files (`git add`) and attempting to commit again.

The aim is to provide a lightweight way to keep some code standards automatically in line with standards.
This does not replace the need to run nox tests, although pre-commits will satisfy some of the nox test checks.

On first time use of the repository, pre-commit will need to be installed locally.
You will need to be in the `poetry shell` or `conda` environment.
Run the following command to perform a first time install.

```bash
pre-commit install
```

This will cache several code assets used in the checks.

When you have new code to commit, pre-commit will kick in and check the code.
Alternatively, you can run the following command to run for all files in repo.

``` bash
pre-commit run --all-files
```

## Contributors

* [Nick Jenkins](https://www.ndjenkins.com) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
