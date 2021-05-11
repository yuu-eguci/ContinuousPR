# NOTE: ざくざく実装するためひとつのファイルにすべてまとめています。のちに整理します。

# Built-in modules.
import json
import datetime

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
    dic = res.json()

    # 200 系でなければ raise HTTPError します。
    # NOTE: いちいち返却値を if でチェックする手間をはぶくために raise_for_status を使っているはずです。
    #       ただ raise_for_status では api から返ってくるエラーメッセージを表示できません。
    #       エラーメッセージ表示のために if しています。
    #       errors 例: [{'resource': 'PullRequest', 'code': 'custom',
    #                   'message': 'A pull request already exists for yuu-eguci:dev.'}]
    if 'errors' in dic and dic['errors'] and 'message' in dic['errors'][0]:
        logger.error(dic['errors'][0]['message'])
    res.raise_for_status()

    return dic


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


def create_comment_body(list_commits_on_pull_result: list, base_branch: str) -> str:
    """コメントの body を作成するビジネスロジックです。
    内容に注文が入ったら、ばんばん書き換えてよし。

    Args:
        list_commits_on_pull_result (list): list_commits_on_pull の返却値
        base_branch (str): base branch 名

    Returns:
        str: コメントの body に使われる想定の文字列
    """

    body = (
        '<!channel>\n'
        f'*## {datetime.datetime.now().strftime("%Y-%m-%d")} Release Note*\n'
        '```'
    )
    for commit in list_commits_on_pull_result:

        # メッセージの1行目のみをリリースノートへ記述します。
        # NOTE: git のメッセージは複数行になります。改行が入るとリリースノートがぐっちゃになるので絞っています。
        messages = commit['commit']['message']
        message = messages.split('\n')[0]

        author_name = commit['commit']['author']['name']
        author_date = commit['commit']['author']['date']
        body += (
            '\n'
            f'- {message} ({author_name} at {author_date})'
        )
    body += (
        '```\n'
        f'数日中に、 {base_branch} 環境へのリリース作業を行います。\n'
        '内容は↑の Release Note を確認してください。\n'
        '\n'
        '【お知らせ】編集担当者の方は、 Release Note を確認して頂き、\n'
        'お知らせが必要な項目について本 channel に文面を投稿してください。\n'
        '\n'
        '[本メッセージは自動送信メッセージです]'
    )
    return body


if __name__ == '__main__':
    pass
