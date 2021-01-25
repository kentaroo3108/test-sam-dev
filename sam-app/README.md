# 開発環境
- aws-cli/1.18.179
- aws sam cli/1.12.0
- python/3.8.0

# 開発環境へのデプロイ手順
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
$ aws s3 mb s3://dev-launch-update-bucket
```

## sam build

```
$ sam build 
```

## sam deploy

```
$ sam deploy --config-env dev --parameter_overrides SlackIncomingUrl={slackのWebhookURL}
```

## スタックの削除

```
$ aws cloudformation delete-stack --stack-name dev-launch-update-stack 
```

# 本番環境へのデプロイ手順
## 使用例
 - ワークフローが実行されて本番環境にデプロイされる例を示す
```
$ git add app.py
$ git commit -m "commitmessage"
$ git push origin master
```

# 環境構築備忘録
## ワークフローの説明
- パス
   - github/workflows/deploy.yml
- トリガーとなるブランチ
   - master
- ワークフローのjob内容
   1. checkoutの実行
   2. cliのセットアップ
   3. credentialsのセットアップ
   4. sam build
   5. sam deploy
- ワークフローが実行されるトリガーファイル
   - sam-app/handlers/
   - sam-app/tamplate.yaml
   - sam-app/samconfig.toml
- Secrets
   - ```AWS_ACCESS_KEY_ID```：デプロイ用IAMユーザーのアクセスキー
   - ```AWS_SECRET_ACCESS_KEY```：デプロイ用IAMユーザーのシークレットキー

## デプロイ用IAMユーザーのSecrets登録方法
1. cloudformation/iam.yamlをデプロイしてアクセスキーとシークレットキーを取得
```
$ aws cloudformation deploy \
  --template-file iam.yaml \
  --stack-name {スタック名} \ 
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides IamUserName={IAMユーザー名}        
$ aws iam create-access-key --user-name {IAMユーザー名}
    {
        "AccessKey": {
        "UserName": "{ユーザー名}",
        "AccessKeyId": "{アクセスキー}",
        "Status": "Active",
        "SecretAccessKey": "{シークレットキー}",
        "CreateDate": "2018-12-14T17:34:16Z"
    }  
```
2. Githubの```Settins > Secrets```からアクセスキー・シークレットキーを登録
<img width="686" alt="スクリーンショット 2021-01-21 151242" src="https://user-images.githubusercontent.com/68361524/105288147-258f4f80-5bfb-11eb-9599-8c89fc427f68.png">


 - ワークフローの実行結果
<img width="467" alt="スクリーンショット 2021-01-21 144147" src="https://user-images.githubusercontent.com/68361524/105285081-0098dd80-5bf7-11eb-9012-eba10da4f981.png">

## 本番環境へのデプロイ準備
初回のデプロイ時のみS3バケットを作成
```
$ aws s3 mb s3://prod-launch-update-bucket 
```