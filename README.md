# slack-progress-checker-bot

指定したチャンネルにメッセージのリンクを送信するbotです. 進捗報告が一箇所にまとまるといいな, という思いでつくりました. 以下の機能があります.

* bot がメンションされると, 指定したチャンネルにメッセージのリンクを送信する
* `/post [送信したいメッセージのリンク]` とすると, 指定したチャンネルにメッセージのリンクを送信する
* メッセージのリンク送信時に, 元のメッセージに好きなリアクションをつける


## セットアップ方法

1. [Slack apiのページ](https://api.slack.com/apps)から, アプリを作成する.  
   `app-manifest.yml`を用いると便利.
1. ボットをワークスペースにインストールする.
1. `sample.env` を参考に, このディレクトリに `.env` ファイルを作成する.
1. Slack Apiのページを見ながら, 以下のように設定する.  
   チャンネルIDはSlack上で, 転送先のチャンネルの設定画面下部から確認できる.
    ```env
    SLACK_BOT_TOKEN=xoxbから始まる, "Bot User OAuth Token"
    SLACK_APP_TOKEN=xappから始まる, "App-level Token"
    POST_CHANNEL_ID=転送先のチャンネルID
    ```
1. リンク送信時に元のメッセージにつけたいreactionを, `./src/main.py` の `reactions` で指定する.  
   デフォルトでは, 🎉がつくようになっている.
1. requirements.txt を用いて, pythonパッケージをインストールする.
1. bot をすべてのチャンネルに追加したい場合は, `./src/add_bot.py` を実行する.
1. `./src/main.py` を実行する.
