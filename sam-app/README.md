# SAMの環境構築手順

## git clone
```
$ git clone https://github.com/niftycorporation/launch-update-uranai.git
$ cd sam-app/
```

## IAMユーザー/ロールの作成

デプロイ用のIAMユーザーの作成と以下のリソースへアクセスできるようにポリシーを設定する
* S3
* CloudFormation
* powertools用のポリシー (参考:https://awslabs.github.io/aws-lambda-powertools-python/)


Cloudformationにアタッチするロールの作成と以下のリソースへアクセスできるようにポリシーを設定する
* Lambda
* CloufFormation
* IAM
* powertools用のポリシー 

## aws configureの設定
※aws cliは事前にインストール済みと想定

```
$ aws configure --profile {プロファイル名}
AWS Access Key ID [None]: {アクセスキー}
AWS Secret Access Key [None]: {シークレットアクセスキー}
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

## AWS SAM CLIのインストール

macOS
```
$ brew tap aws/tap
$ brew install aws-sam-cli
$ sam --version
SAM CLI, version 1.0.0
```

Windows
```
https://github.com/awslabs/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi

> sam --version
SAM CLI, version 1.0.0
```

その他の環境
```
$ pip install -U aws-sam-cli
$ sam --version
SAM CLI, version 1.0.0
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

## SAM Build

```
$ sam build --profile {プロファイル名}
```

## SAM Deploy

```
$ sam deploy --role-arn {CloufFormation用のロールのARN} --profile {プロファイル名}
```

## スタックの削除

```
$ aws cloudformation delete-stack --stack-name {スタック名} --profile {プロファイル名}
```