# ローカルPCの開発環境
・windows 
・aws cli aws-cli/1.18.179
・aws sam cli/1.12.0
・python/3.8

# 本番環境へのデプロイ方法

## git clone
```
$ git clone https://github.com/niftycorporation/launch-update-uranai.git
$ cd sam-app/
```

## IAMユーザー/ロールの作成
デプロイ用のIAMユーザーとCloudformation用のロールを作成する

```
$ aws cloudformation deploy \
  --template-file iam.yaml \
  --stack-name Deploy-Iam-Sample-SAM-App \ 
  --capabilities CAPABILITY_NAMED_IAM \ 
  --profile {プロファイル名}
```

##git 

## AWS SAM CLIのインストール

```

```

## S3 bucketの作成

```
$ aws s3 mb s3://{バケット名} --profile {プロファイル名}
```

## samconfig.tomlを変更

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

## samconfig.tomlをpushする

```
$ git add .
$ git commit -m "{コメント}"
$ git git push origin {ブランチ名}
```