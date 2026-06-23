#「①準備（インポート） ➔ ②受け取り（API） ➔ ③解析（Rekognition） ➔ ④翻訳 ➔ ⑤返却（API）」
#という一連の流れを忘れずに

import json
import base64
import boto3
# ↑AWSの各種サービス（RekognitionやDynamoDBなど）をPythonから操作するための
#「AWS公式の万能リモコン（SDK）」がboto3。アマゾンカワイルカ（別名ボト）から。
# from translate import Translator
# r'''
# AWS lambdaは実行される前に一度だけdef lambda_handler関数の外側を読んで初期化する。
# '''

# Amazon Rekognition（画像解析サービス）へアクセスする
#クライアントオブジェクトを取得
rekognition = boto3.client("rekognition")
#↑'【コードを入力】'
# '''Boto3の「Clientインターフェース（低レベルな直訳窓口）」を使って、
# Amazon Rekognition専用のリモコンを作成し、rekognitionという変数に代入。
# これを使って後でAIに解析を依頼する。
# '''
# translator = Translator(to_lang="ja",from_lang="en")
# 英語から日本語へ翻訳するTranslatorオブジェクトを取得
#↑'【コードを入力】'
#翻訳機を「英語(en)から日本語(ja)へ翻訳する」という設定でインスタンス(オブジェクト)化

def lambda_handler(event, context):
    #API Gatewayからリクエストが来た時に実行される「メインの受付窓口。
    #送られてきたデータはすべて eventという仮引数に代入される。
    #●eventというのは宣言していないのに、送られてきたデータがここに入る仕組みがピンとこない。
    #●ブラウザでJSを動かす時の環境変数のようなものか？ 
    try:
        # リクエスト本文のJSONを読み込み
        body = json.loads(event['body'])
            #APIGatewayからﾘｸｴｽﾄが来た時に実行される。
    #送られて来たHTTPﾘｸｴｽﾄ本文は全てevent['body']という辞書型に
    #格納されている。
    #●↑これはJavaScriptを記述する時にブラウザ上のイベント情報が、
    #宣言しなくても環境変数としてeventに格納されているのと同じ。
        print('event:', event) #←受取ったeventそのものを表示してみる。
        # '''↑API GatewayからPOSTメソッドで見えない形で送られてきたJSON文字列（event['body']）を、
        # Pythonで操作しやすい辞書型に変換（loads）して、変数 body に入れています。
        # ●loadに変換という意味もあるの？
        # ●jsonモジュールの各関数の処理の仕方が、json⇔文字列⇒バイナリそれぞれのどれに当たるかが
        #  な曖昧理解になっているのを感じる。'''
                 # JSON形式の画像データ（Base64エンコード済文字列）を
        #Pythonで扱える辞書型の文字列として変換してbodyを貼る。
        # JSON内の画像データ（Base64エンコード済）をバイナリに変換
        base64_string = base64.b64decode(body['imageData'])

         # 📸【観測用カメラ】受け取ったデータの「長さ」と「最初・最後の文字」をログに出す
        print(f"★Base64 Length: {len(base64_string)}")
        print(f"★Base64 Preview: {base64_string[:50]} ... {base64_string[-50:]}")
        # '''ログに「文字列の長さ」と「最初と最後の50文字だけ」を出力。Base64は数万文字になるため、
        # 全部 print するとログがパンクする。長さを測って一部だけ切り取るのは、よく使うデバッグの手法
        # '''
        
        # バイナリに変換
        image_bytes = base64.b64decode(base64_string)
        #↑文字の羅列であるBase64文字列を解読（デコード）し、Rekognitionが理解できる純粋な
        #「画像データ（バイナリ）」に戻して、image_bytes の札を貼る。
        print(f"★Image Bytes Length: {len(image_bytes)}")


        # Amazon Rekognitionで画像を解析して物体を検知
        #（上位10件、信頼度70%以上）
        res_rekog = rekognition.detect_labels(
            # '''lambda_handlerの外で実体化させたrekognition操作用インスタンスのメソッド、
            # detect_labelsメソッド(ラベル検出)を実行。
            # '''
            Image={'Bytes': image_bytes},
            #↑解析するターゲットを指定。今回は直上で復元した画像データimage_bytes
            MaxLabels=10, MinConfidence=70,
            #↑AIの自信（信頼度）が70%以上のものだけを」「最大10件まで」返せと、
            #デフォルトのキーワード引数に値を入れて.detect_labelsに渡す。
            # Uncomment to use image properties and filtration settings
            Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"]
            #「一般的な物体の名前」と「画像の色合いなどのプロパティ」の両方を分析機能をONにする
            #キーワード引数。
        )
        # for label_confidence in res_rekog["label"]["Confidence"]:
        #     if label_confidence >= 70.0:
        #         lbls_conf70 = labels_confidence
        # lbls_conf70_top = lbls_conf70.sort(key='confidence')
        # lbls_conf70_top10 = lbls_conf70_top[0:11]
        #↑'【コードを入力】'

        #↓ 解析結果（res_rekog）内の全てのラベル名を英語から日本語へ
        #翻訳 ↓【コードを入力】
        # for label in res_rekog['Labels']:
        #     english_name = label['Name']
        #     japanese_name = translator.translate(english_name)
        #     label['NameJa'] = japanese_name
            #↑元のラベル情報（辞書）に、新しく NameJa（日本語名）というキーを自分で作り、
            #そこに翻訳した日本語を書き込む。

        # レスポンス返却
        return {
        #↑API Gatewayを通じて、ユーザー（ブラウザ）に結果を返すための辞書の作成
            'statusCode': 200,
            #HTTPステータスコード「200」は、通信が正常に完了したことをブラウザに伝える。
            'body': json.dumps(res_rekog['Labels'],ensure_ascii=False), #←【コードを入力】
            # 解析結果内の全てのラベルをJSONに変換
            # '''↑日本語訳が追加されたラベルのリストを、ブラウザが通信で受け取れるように再びJSONの
            # 「文字列」に変換（dumps）して、body に入れます。
            # (※json.dumps(res_rekog['Labels'], ensure_ascii=False) としないと日本語が
            #  "\u30cd\u30b3" のようにUnicode文字化けする。
            #  ●ensure_asciiは英語的にはどんな意味になる？
            # '''
            'headers': {
            #ブラウザへの「お手紙の封筒（ヘッダー）」。
            #「中身はJSONデータだよ」と伝えている。
                'Content-Type': 'application/json',
                '【コードを入力】': '【コードを入力】' 
                # 全てのオリジンにCORSを許可
            },
            'isBase64Encoded': False
        }

    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
# r'''
# {
#   "statusCode": 200,
#   "body": "[{\"Name\": \"Gray\", \"Confidence\": 99.95271301269531, \"Instances\": [], \"Parents\": [], \"Aliases\": [], \"Categories\": [{\"Name\": \"Colors and Visual Composition\"}], \"NameJa\": \"\\u30b0\\u30ec\\u30fc\"}]",
#   "headers": {
#     "Content-Type": "application/json",
#     "【コードを入力】": "【コードを入力】"
#   },
#   "isBase64Encoded": false
#   ◆補足：
#   疑問①：event 引数にはなぜ自動でデータが入るのか？環境変数みたいなもの？
# ●eventというのは宣言していないのに、送られてきたデータがここに入る仕組みがピンとこない。 ●ブラウザでJSを動かす時の環境変数のようなものか？
# 回答：環境変数ではなく、JavaScriptの「クリックイベント（onClick(e)）」などに近いです。AWSの裏側のシステムが「関数を呼び出す時」に、荷物（データ）を渡してくれています。
# Pythonの def lambda_handler(event, context): というのは、あくまで「関数の設計図」です。昌敏さんがこの関数を直接実行しているわけではありません。
# API GatewayにURL経由でアクセスが来た時、AWSの裏側で動いているシステム（Lambdaの実行環境）が、昌敏さんの代わりにこの関数を実行（Invoke）します。 その際、AWSのシステムがAPI Gatewayから受け取ったHTTPリクエスト（ヘッダーやボディ、IPアドレスなどすべて）を、自動的にPythonの辞書型に変換し、event という引数に入れて lambda_handler(event, context) と呼び出してくれる仕様になっています
# 。
# つまり、「宣言していないのに入る」のではなく、**「AWSのシステムがこの関数を呼び出す時のルールとして、最初の引数に必ずリクエストデータを入れて渡す」**と決まっているからです。
# 疑問②：json.loads の「load」の意味と、データ変換の整理
# ●loadに変換という意味もあるの？ ●jsonモジュールの各関数の処理の仕方が、json⇔文字列⇒バイナリそれぞれのどれに当たるかがな曖昧理解になっているのを感じる。
# 回答：「load」の本来の意味は「荷物を積む」「読み込む」です。文字列をPythonの世界に「読み込む」から load です。
# JSONの変換処理は、英語の略称を理解すると一発で覚えられます。ポイントは最後に付いている s です。この s は string（文字列） を意味します。
# json.loads(文字列) ＝ Load String（文字列から読み込む） 通信で送られてきた単なる「文字の羅列（JSON形式の文字列）」を読み込んで、Pythonで操作できる「辞書型（ディクショナリ）」に**変換（デシリアライズ）**します
# 。
# json.dumps(辞書) ＝ Dump String（文字列として吐き出す） Pythonの世界で作った「辞書型」を、外の世界（ブラウザなど）に通信で送るために、「ただの文字列」に**変換（シリアライズ）**して吐き出します
# 。
# ※ちなみに、「バイナリ（0と1のデータ）」⇔「文字列」の変換はJSONモジュールの仕事ではなく、今回使っている base64.b64decode() （Base64文字列からバイナリへ）が担当しています。
# 疑問③：ensure_ascii=False の英語的な意味
# ●ensure_asciiは英語的にはどんな意味になる？
# 回答：「ensure（保証する・確実にする）」＋「ASCII（半角英数字）」＝「絶対に半角英数字だけで出力する」という意味です。
# Pythonの json.dumps() は、初期設定（デフォルト）で ensure_ascii=True になっています。 これは、「通信エラーが起きないように、どんな文字が来ても絶対にASCII（半角英数字）だけで出力することを保証するよ」というPythonのお節介機能です。
# そのため、日本語（ASCII以外の文字）が来ると、無理やりASCIIで表現しようとして \u30cd\u30b3 のようなエスケープシーケンス（Unicode文字化け）に変換してしまいます。
# これを ensure_ascii=False（ASCIIを保証しなくていいよ、そのまま出していいよ）と設定することで、日本語がそのまま綺麗にブラウザに返るようになります。
# '''