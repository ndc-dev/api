FROM python:3.14-slim

WORKDIR /app

# uv を公式イメージから取り込む（再現性のためバージョンを固定する）
COPY --from=ghcr.io/astral-sh/uv:0.12.0 /uv /uvx /bin/

# Python依存関係のインストール
# uv.lock をそのまま使うので requirements.txt は要らない。
# --frozen: uv.lock を書き換えず、ロックどおりに入れる（ずれていれば失敗する）
# --no-dev: autopep8 など開発用の依存は入れない
# --no-install-project: このプロジェクト自体はパッケージとして入れない
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# uv が作る仮想環境に PATH を通し、gunicorn などをそのまま呼べるようにする
ENV PATH="/app/.venv/bin:$PATH"

# アプリケーションファイルのコピー
COPY main.py jsonschema.json ./
COPY templates/ templates/
COPY zips/ zips/

# Cloud Run用の環境変数
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# 非rootユーザーで実行
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# main.py がモジュール読み込み時にNDCデータ（1万数千件×2）をメモリに展開するため、
# ワーカーを増やすとその分メモリに複製される。512Miの小規模インスタンスなので1ワーカーに絞り、
# 同時実行数はCloud Run側のインスタンス数（自動スケール）に任せる。
# --threads は sync/gthread worker専用のオプションで UvicornWorker（asyncio）には効かないため付けない。
CMD exec gunicorn --bind :$PORT --workers 1 -k uvicorn_worker.UvicornWorker main:app
