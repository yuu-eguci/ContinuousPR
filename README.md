ContinuousPR
===

This program posts Pull Request using api.github.com.
You can do this only by hitting one api with curl. And also by using hub command or gh command.
But if you want the feature below, this program helps.

- Send notification only about the PRs posted by this program,to Slack channel

It is worth using when you want to notify **only** about the PRs about project release.

![readme](https://user-images.githubusercontent.com/28250432/117780660-cc672c80-b27a-11eb-9e95-2e8ff8d7856c.png)

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

## .env

```
# 実際にプログラムが動く環境で必要な env(Heroku を想定)
OWNER = ''
REPO = ''
TOKEN_REPO_SCOPE = ''
SLACK_BOT_TOKEN = ''
SLACK_MESSAGE_CHANNEL = ''
PR_BODY = ""

# CI/CD 環境で必要な env(GitHub Actions を想定)
HEROKU_API_KEY = ''
HEROKU_APP_NAME = ''
HEROKU_EMAIL = ''
```
