# 開発環境
- aws-cli/1.18.179
- aws sam cli/1.12.0
- python/3.8.0

# ローカルPCからのデプロイ手順

## git clone

```
$ git clone https://github.com/niftycorporation/launch-update-uranai.git
$ cd sam-app/
```

## デプロイ用のIAMユーザーを作成

```
$ aws cloudformation deploy \
  --template-file iam.yaml \
  --stack-name {スタック名} \ 
  --capabilities CAPABILITY_NAMED_IAM 
```

## デプロイ用のIAMユーザーのアクセスキーとシークレットキーを取得

```
$ aws iam create-access-key --user-name deploy-iam-user
```

## aws configureの設定

```
$ aws configure --profile {プロファイル名}
AWS Access Key ID [None]: {アクセスキー}
AWS Secret Access Key [None]: {シークレットアクセスキー}
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

## AWS SAM CLIのインストール
- 以下のリンクを参考にインストールする
  - https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

## S3 bucketの作成

```
$ aws s3 mb s3://{バケット名} --profile {プロファイル名}
```

## samconfig.tomlを修正

```
version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = {スタック名}
s3_bucket = {バケット名}
s3_prefix = {プレフィックス名}
region = {リージョン名}
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
parameter_overrides = {起動テンプレート名}
```

## sam build

```
$ sam build --profile {プロファイル名}
```

## sam deploy

```
$ sam deploy --profile {プロファイル名}
```

## スタックの削除

```
$ aws cloudformation delete-stack --stack-name {スタック名} --profile {プロファイル名}
```