# 開発環境
- aws-cli/1.18.179
- aws sam cli/1.12.0
- python/3.8.0

# 開発環境へのデプロイ
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
$ sam deploy --config-env dev
```

## スタックの削除

```
$ aws cloudformation delete-stack --stack-name dev-launch-update-stack 
```

# 本番環境へのデプロイ
## ワークフローの説明
- パス
   - github/workflows/deploy.yml
- ワークフロー
   1. checkoutの実行
   2. cliのセットアップ
   3. credentialsのセットアップ
   4. sam build
   5. sam deploy
- ワークフローが実行されるトリガーとなるファイル
   - sam-app/handlers/
   - sam-app/tamplate.yaml
   - sam-app/samconfig.toml
- Secrets
   - ```AWS_ACCESS_KEY_ID```：デプロイ用IAMユーザーのアクセスキー
   - ```AWS_SECRET_ACCESS_KEY```：デプロイ用IAMユーザーのシークレットキー
## 使用例
```
$ git clone https://github.com/niftycorporation/launch-update-uranai.git
$ cd sam-app/
$ aws s3 mb s3://prod-launch-update-bucket
$ git add samconfig.toml
$ git commit -m "commitmessage"
$ git push origin master
```

## ワークフローの実行結果
<img width="467" alt="スクリーンショット 2021-01-21 144147" src="https://user-images.githubusercontent.com/68361524/105285081-0098dd80-5bf7-11eb-9012-eba10da4f981.png">
