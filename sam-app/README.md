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
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides IamUserName={IAMユーザー名}
```

## デプロイ用のIAMユーザーのアクセスキーとシークレットキーを取得

```
$ aws iam create-access-key --user-name {IAMユーザー名}
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

dev環境へデプロイする場合は以下を修正
```
[dev.deploy.parameters]
stack_name = {スタック名}
s3_bucket = {バケット名}
s3_prefix = {プレフィックス名}
region = "ap-northeast-1"
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
parameter_overrides = {テンプレート名}
```

prod環境へデプロイする場合は以下を修正
```
[prod.deploy.parameters]
stack_name = {スタック名}
s3_bucket = {バケット名}
s3_prefix = {プレフィックス名}
region = "ap-northeast-1"
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
parameter_overrides = {テンプレート名}
```

## sam build

```
$ sam build --profile {プロファイル名}
```

## sam deploy

```
$ sam deploy --config-env {dev|prod} --profile {プロファイル名}
```

## スタックの削除

```
$ aws cloudformation delete-stack --stack-name {スタック名} --profile {プロファイル名}
```

# 開発環境へのデプロイ手順
## GitHubのSecretsを登録する
1. githubのprojectのsetting > secretsから登録する
2. *DEV_AWS_ACCESS_KEY_ID*にデプロイ用IAMユーザーのアクセスキーを登録
3. *DEV_AWS_SECRET_ACCESS_KEY*にデプロイ用IAMユーザーのシークレットキーを登録

## samconfig.tomlの修正
samconfig.tomlの```[dev.deploy.parameters]```を修正

```
[dev.deploy.parameters]
stack_name = {スタック名}
s3_bucket = {バケット名}
s3_prefix = {プレフィックス名}
region = "ap-northeast-1"
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
parameter_overrides = {テンプレート名}
```

## samconfig.tomlをPush

```
$ git add samconfig.toml
$ git commit -m "{commit message}"
$ git push origin develop
```

# 本番環境へのデプロイ手順
## GitHubのSecretsを登録する
1. githubのprojectのsetting > secretsから登録する
2. *PROD_AWS_ACCESS_KEY_ID*にデプロイ用IAMユーザーのアクセスキーを登録
3. *PROD_AWS_SECRET_ACCESS_KEY*にデプロイ用IAMユーザーのシークレットキーを登録

## samconfig.tomlの修正
samconfig.tomlの```[prod.deploy.parameters]```を修正

```
[prod.deploy.parameters]
stack_name = {スタック名}
s3_bucket = {バケット名}
s3_prefix = {プレフィックス名}
region = "ap-northeast-1"
confirm_changeset = false
capabilities = "CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND"
parameter_overrides = {テンプレート名}
```

## samconfig.tomlをPush

```
$ git add samconfig.toml
$ git commit -m "{commit message}"
$ git push origin master
```
