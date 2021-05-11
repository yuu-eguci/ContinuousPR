# Built-in modules.
import datetime
import argparse
import sys

# Third-party modules.
import pytz

# User modules.
import utils
import functions


# ロガーを取得します。
logger = utils.get_my_logger(__name__)
current_utc = datetime.datetime.now(tz=pytz.utc)
logger.info(f'Started at {current_utc.isoformat()}')
current_jst = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
logger.info(f'Started at {current_jst.isoformat()}')

# コマンドライン引数を取得します。
# head -> base の PR となります。
# NOTE: TOKEN 等は環境変数で良いですが、ブランチは実行ごとに可変にしたい。
# NOTE: release への PR は通知したいが、 early-access への PR は必要ない。
#       slack_notification 引数はその分岐を行うために追加しました。
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--head', type=str, help='head -> base',
                    default='dev')
parser.add_argument('-B', '--base', type=str, help='head -> base',
                    default='master')
parser.add_argument('-S', '--slack-notification', type=bool,
                    help='Send release note message to Slack', default=False)
parser.add_argument('-D', '--date', type=int,
                    help='Run this program only on this date',
                    # default=0 のときは日付に構わず実行します。
                    # NOTE: Heroku 上で毎日発火する場合は日付指定が良い仕事をします。
                    #       しかしテストで実行したいときは、毎回その日の日付をコマンドライン引数に含めるのは面倒です。
                    #       その手間を省くために用意したデフォルト値です。
                    default=0)
args = parser.parse_args()
logger.info(f'PR [{args.head} -> {args.base}] will be made.'
            f' Slack notification is {"on" if args.slack_notification else "off"}.')

# 実行日チェックです。
# NOTE: 本スクリプトは毎日の定期発火を想定しています。
#       ただし、 PR が欲しいのは月イチなので、毎日実行されると不都合です。
#       そのため、コマンドライン引数で日付を受け取り、その日にのみ続きの処理を行います。
if args.date == 0:
    # 上述したとおり、 0 のときは構わず実行します。
    pass
else:
    # 「* 日にだけ実行してほしい」、と指定がある場合です。チェックしてやります。
    today = utils.get_today_jst('%d')
    if str(args.date) != today:
        logger.info(
            'This is not the date to create PR.'
            f' Specified date: {args.date} Today: {today}'
        )
        sys.exit()

# api を使って PR を作ります。
create_pull_result = functions.create_pull(args.head, args.base)
logger.info(f'Successfully created PR: {create_pull_result["html_url"]}')

# 「Slack 通知不要」ならばここで終了です。
if not args.slack_notification:
    sys.exit()

# NOTE: ここ以降の処理は、
#       「PR の commits 一覧をリリースノートとして Slack へ通知したい」
#       というニーズのためにある処理です。
#       もともとは、「PR コメントにリリースノートを投稿し、それを Slack へ通知する」と
#       わざわざ「PR コメント」を経由していたため、ラベルをつけたりなんだりと非常に苦労しましたが
#       「いや直接 Slack にメッセージしたらいいじゃん」ということで簡略化できました。
# NOTE: ラベル指定での Slack notification は知見として残しておきます。
#       下記コマンドで通知可能です。
#       /github subscribe OWNER/REPO pulls,comments,+label:"CONTINUOUS-PR"

# api を使って PR の commits 一覧を取得します。
# NOTE: 「リリースノート」となる一覧を取得するための処理です。
list_commits_on_pull_result = functions.list_commits_on_pull(
    create_pull_result['number'])
logger.info(f'Successfully listed commits, count: {len(list_commits_on_pull_result)}')  # noqa: E501
comment_body = functions.create_comment_body(
    list_commits_on_pull_result,
    args.base,
)

# comment_body として取得した内容は、リリースノートとして扱い Slack へ送ります。
utils.send_slack_message(comment_body)
logger.info('Successfully sent message to Slack')
