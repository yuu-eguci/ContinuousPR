# NOTE: ざくざく実装するためひとつのファイルにすべてまとめています。のちに整理します。

# Built-in modules.
import json

# Third-party modules.
import requests

# User modules.
import consts
import utils


# ロガーを取得します。
logger = utils.get_my_logger(__name__)

# api.github.com へのアクセスに使う http headers です。
HEADERS_FOR_API = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {consts.TOKEN_REPO_SCOPE}',
}


def create_pull(head_branch: str, base_branch: str) -> dict:
    """api.github.com を使って PR を作成します。

    Args:
        head_branch (str): Head branch
        base_branch (str): Base branch

    Returns:
        dict: Returned value from api
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/pulls'
    payload = {
        'title': f'🚀 [Scheduled] {head_branch} to {base_branch}',
        'head': head_branch,
        'base': base_branch,
        'body': consts.PR_BODY,
    }
    res = requests.post(url, headers=HEADERS_FOR_API, data=json.dumps(payload))

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> dict します。
    dic = res.json()
    return dic


def add_label(issue_number: int) -> list:
    """api.github.com を使ってラベルを追加します。
    ラベルがもともとなくとも、自動で生成されます。

    Args:
        issue_number (int): Issue number

    Returns:
        list: Returned value from api
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/issues/{issue_number}/labels'  # noqa: E501
    payload = {
        'labels': ['CONTINUOUS-PR'],
    }
    res = requests.post(url, headers=HEADERS_FOR_API, data=json.dumps(payload))

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> list します。
    lis = res.json()
    return lis


def list_commits_on_pull(issue_number: int) -> list:
    """api.github.com を使って PR に含まれる commits 一覧を取得します。

    Args:
        issue_number (int): Issue number

    Returns:
        list: Returned value from api
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/pulls/{issue_number}/commits'  # noqa: E501
    res = requests.get(url, headers=HEADERS_FOR_API)

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> list します。
    lis = res.json()
    return lis


def create_comment_body(list_commits_on_pull_result: list) -> str:
    """コメントの body を作成するビジネスロジックです。
    内容に注文が入ったら、ばんばん書き換えてよし。

    Args:
        list_commits_on_pull_result (list): list_commits_on_pull の返却値

    Returns:
        str: コメントの body に使われる想定の文字列
    """

    body = '## Release note'
    for commit in list_commits_on_pull_result:
        message = commit['commit']['message']
        author_name = commit['commit']['author']['name']
        author_date = commit['commit']['author']['date']
        body += (
            '\n'
            f'- {message} ({author_name} at {author_date})'
        )
    body += '\n'

    return body


def create_comment(issue_number: int, body: str) -> dict:
    """api.github.com を使って PR にコメントを投稿します。

    Args:
        issue_number (int): Issue number
        body (str): 投稿コメント

    Returns:
        dict: Returned value from api
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/issues/{issue_number}/comments'  # noqa: E501
    payload = {
        'body': body,
    }
    res = requests.post(url, headers=HEADERS_FOR_API, data=json.dumps(payload))

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> dict します。
    dic = res.json()
    return dic


if __name__ == '__main__':
    pass
