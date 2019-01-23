# slack-search
## setup

slackのログのzipをes-python/slack 以下に解凍しておきます

```bash
./init.sh
```

`curl 'localhost:9200/slack/_analyze?pretty' -d 'こんにちは世界'` を実行して，正しく形態素解析されていれば大丈夫

## 起動
.env.sampleを参考に.envを書いてください

```bash
docker-compose up
```