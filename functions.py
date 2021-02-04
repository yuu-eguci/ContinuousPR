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


def add_label(issue_number: int) -> dict:
    """api.github.com を使ってラベルを追加します。
    ラベルがもともとなくとも、自動で生成されます。

    Args:
        issue_number (int): Issue number

    Returns:
        dict: Returned value from api
    """

    url = f'https://api.github.com/repos/{consts.OWNER}/{consts.REPO}/issues/{issue_number}/labels'  # noqa: E501
    payload = {
        'labels': ['CONTINUOUS-PR'],
    }
    res = requests.post(url, headers=HEADERS_FOR_API, data=json.dumps(payload))

    # 200 系でなければ raise HTTPError します。
    res.raise_for_status()

    # 返却 json -> dict します。
    dic = res.json()
    return dic


if __name__ == '__main__':
    pass
