# AM-Flow Programming Test

This repository contains the AM-Flow programming test.

## Requirements

- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)

## Installation

- Add Poetry to your PATH (see Poetry documentation).
- Install the dependencies with `poetry install`.
- Copy `.env.template` to `.env` and set the variables.

## Usage

Run the project with the following command.

```
poetry run python main.py
```

## Linter

This repository uses [Black](https://github.com/psf/black) as linter.

```
poetry run black .
```