# NDC API for Developer

日本十進分類法（NDC）の分類項目を JSON で返す、開発者向けの REST API です。
NDC8（10,340項目）と NDC9（12,388項目）の全体を配信しています。

- 動作サンプル: [https://api-4pccg7v5ma-an.a.run.app/](https://api-4pccg7v5ma-an.a.run.app/)
- フレームワーク: [FastAPI](https://fastapi.tiangolo.com/)
- プロジェクト全体: [ndc.dev](https://ndc.dev/) （[ndc-dev/web](https://github.com/ndc-dev/web)）

## エンドポイント

| パス | 内容 |
|---|---|
| [`/`](https://api-4pccg7v5ma-an.a.run.app/) | トップページ（HTML） |
| [`/ndc8.json`](https://api-4pccg7v5ma-an.a.run.app/ndc8.json) | NDC8 の全項目 |
| [`/ndc8/`](https://api-4pccg7v5ma-an.a.run.app/ndc8/) | NDC8 の階層のルート |
| [`/ndc8/{ndc}`](https://api-4pccg7v5ma-an.a.run.app/ndc8/123) | NDC8 の1項目（例: `/ndc8/123`） |
| [`/ndc9.json`](https://api-4pccg7v5ma-an.a.run.app/ndc9.json) | NDC9 の全項目 |
| [`/ndc9/`](https://api-4pccg7v5ma-an.a.run.app/ndc9/) | NDC9 の階層のルート |
| [`/ndc9/{ndc}`](https://api-4pccg7v5ma-an.a.run.app/ndc9/123) | NDC9 の1項目 |
| [`/schema`](https://api-4pccg7v5ma-an.a.run.app/schema) | 1項目の JSON Schema（`jsonschema.json`） |
| [`/docs`](https://api-4pccg7v5ma-an.a.run.app/docs) | FastAPI が生成する API ドキュメント |

いずれも CORS を許可しているので、ブラウザから直接呼び出せます。

`ndc8.json` / `ndc9.json` は分類記号をキーにしたオブジェクトを返します。数MBあるため、
1項目ずつ返すエンドポイントと違って `source`（元データの Turtle 断片）は含みません。

## データ

日本図書館協会が公開している
[NDC のオープンデータ](https://www.jla.or.jp/committees/bunrui/ndc-data/)（RDF/Turtle）を
`zips/ndc8.zip` / `zips/ndc9.zip` として同梱しています。
起動時に [ndc-parser](https://github.com/ndc-dev/python-parser) でパースしてメモリに展開するため、
データベースは使いません。元データは [ndc-dev/opendata](https://github.com/ndc-dev/opendata) にも置いてあります。

## 開発

Python 3.14（`.python-version`）と [uv](https://docs.astral.sh/uv/) が必要です。

```
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0
```

http://127.0.0.1:8000/ で開きます。

### JSON Schema の検証

`ndc9.json` の全項目が `jsonschema.json` に適合するかを確認します。
上の開発サーバーを起動したまま、別のシェルで実行してください。

```
uv run python validate.py
```

## Docker

本番と同じ構成（gunicorn + UvicornWorker、非rootユーザー）で起動します。

```
docker build . -t ndc-dev-api
docker run -it -p 8080:8080 ndc-dev-api
```

http://127.0.0.1:8080/ で開きます。

## デプロイ

インフラは [Terraform](terraform/) で管理しています（Cloud Runのメモリ・スケーリング・
サービスアカウント等）。デプロイはイメージの差し替えのみで、Cloud Build で
Artifact Registry へビルド・pushし、Cloud Run に反映します。

```
gcloud config set project ndc-dev-255301
gcloud builds submit --tag asia-northeast1-docker.pkg.dev/ndc-dev-255301/api/api:latest
gcloud run deploy api --image asia-northeast1-docker.pkg.dev/ndc-dev-255301/api/api:latest --region asia-northeast1
```

以前は `gcr.io`（Container Registry）にpushしていましたが、gcr.io はこのプロジェクトで
完全に廃止され読み取りもできなくなっていたため、Artifact Registry に移行しました。
