ContinuousPR
===

This program posts Pull Request using api.github.com.
You can do this only by hitting one api with curl. And also by using hub command or gh command.
But if you want the feature below, this program helps.

- Send notification only about the PRs posted by this program,to Slack channel

It is worth using when you want to notify **only** about the PRs about project release.

![readme](https://user-images.githubusercontent.com/28250432/106868735-7e3e0c80-6712-11eb-89d6-f7d492a3978e.png)

## Installation

```bash
pipenv install
pipenv shell
python main.py --head dev --base master
```

## Usage

```plaintext
# python main.py -h
usage: main.py [-h] [-H HEAD] [-B BASE]

optional arguments:
  -h, --help            show this help message and exit
  -H HEAD, --head HEAD  head -> base
  -B BASE, --base BASE  head -> base
```
