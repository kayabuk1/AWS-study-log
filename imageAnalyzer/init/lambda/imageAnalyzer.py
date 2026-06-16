import json
import base64
import boto3
from translate import Translator

# Amazon Rekognition（画像解析サービス）へアクセスする
#クライアントオブジェクトを取得
rekognition = boto3.client("rekognition")
#↑'【コードを入力】'
# 英語から日本語へ翻訳するTranslatorオブジェクトを取得
translator = Translator(to_lang="ja",from_lang="en")
#↑'【コードを入力】'

def lambda_handler(event, context):
    try:
        # リクエスト本文のJSONを読み込み
        body = json.loads(event['body'])
        # JSON内の画像データ（Base64エンコード済）をバイナリに変換
        image_bytes = base64.b64decode(body['imageData'])

        # リクエスト本文のJSONを読み込み
        body = json.loads(event['body'])
        base64_string = body['imageData']
         # 📸【観測用カメラ】受け取ったデータの「長さ」と「最初・最後の文字」をログに出す
        print(f"★Base64 Length: {len(base64_string)}")
        print(f"★Base64 Preview: {base64_string[:50]} ... {base64_string[-50:]}")
        
        # バイナリに変換
        image_bytes = base64.b64decode(base64_string)
        print(f"★Image Bytes Length: {len(image_bytes)}")


        # Amazon Rekognitionで画像を解析して物体を検知
        #（上位10件、信頼度70%以上）
        res_rekog = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10, MinConfidence=70,
            # Uncomment to use image properties and filtration settings
            Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"]
        )
        # for label_confidence in res_rekog["label"]["Confidence"]:
        #     if label_confidence >= 70.0:
        #         lbls_conf70 = labels_confidence
        # lbls_conf70_top = lbls_conf70.sort(key='confidence')
        # lbls_conf70_top10 = lbls_conf70_top[0:11]
        #↑'【コードを入力】'

        #↓ 解析結果（res_rekog）内の全てのラベル名を英語から日本語へ
        #翻訳 ↓【コードを入力】
        for label in res_rekog['Labels']:
            english_name = label['Name']
            japanese_name = translator.translate(english_name)
            label['NameJa'] = japanese_name
        # レスポンス返却
        return {
            'statusCode': 200,
            'body': json.dumps(res_rekog['Labels']), #←【コードを入力】
            # 解析結果内の全てのラベルをJSONに変換
            'headers': {
                'Content-Type': 'application/json',
                '【コードを入力】': '【コードを入力】' 
                # 全てのオリジンにCORSを許可
            },
            'isBase64Encoded': False
        }

    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
r'''
{
  "statusCode": 200,
  "body": "[{\"Name\": \"Gray\", \"Confidence\": 99.95271301269531, \"Instances\": [], \"Parents\": [], \"Aliases\": [], \"Categories\": [{\"Name\": \"Colors and Visual Composition\"}], \"NameJa\": \"\\u30b0\\u30ec\\u30fc\"}]",
  "headers": {
    "Content-Type": "application/json",
    "【コードを入力】": "【コードを入力】"
  },
  "isBase64Encoded": false
'''