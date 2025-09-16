import requests
import json
import fitz
import io
from pydub import AudioSegment
import simpleaudio as sa

# VOICEVOXが稼働しているAPIサーバーのURL
VOICEVOX_API_URL = "http://localhost:50021"

def extract_text_from_pdf(pdf_path, page_num=0):
    """
    指定されたPDFファイルの指定ページからテキストを抽出する
    """
    try:
        doc = fitz.open(pdf_path)
        if page_num >= doc.page_count:
            return f"エラー: 指定されたページ番号 {page_num} は存在しません。"
        page = doc[page_num]
        text = page.get_text()
        doc.close()
        return text
    except FileNotFoundError:
        return f"エラー: 指定されたファイルが見つかりません - {pdf_path}"
    except Exception as e:
        return f"PDFの読み込み中にエラーが発生しました: {e}"

def generate_voice(text, speaker_id=3):
    """
    VOICEVOX APIを使ってテキストを音声データに変換する
    """
    try:
        params = {"text": text, "speaker": speaker_id}
        res = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
        if res.status_code != 200:
            print(f"音声クエリ生成エラー: {res.text}")
            return None
        audio_query_data = res.json()
        
        res = requests.post(f"{VOICEVOX_API_URL}/synthesis", params={"speaker": speaker_id}, data=json.dumps(audio_query_data))
        if res.status_code != 200:
            print(f"音声合成エラー: {res.text}")
            return None
            
        return res.content
    except requests.exceptions.RequestException as e:
        print(f"VOICEVOX API接続エラー: {e}")
        return None

def play_audio(audio_data):
    """
    音声データを再生する
    """
    try:
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
        play_obj = sa.play_buffer(
            audio_segment.raw_data,
            num_channels=audio_segment.channels,
            bytes_per_sample=audio_segment.sample_width,
            sample_rate=audio_segment.frame_rate
        )
        play_obj.wait_done()
    except Exception as e:
        print(f"音声再生エラー: {e}")

if __name__ == "__main__":
    pdf_file_path = r"C:\Users\oneof\OneDrive\デスクトップ\研究室関連\ipadpro11-2020_標準 ベイズ統計学 入江 薫 288p_4254122675.pdf"
    page_to_read = 0

    print(f"PDFファイル '{pdf_file_path}' のページ {page_to_read} からテキストを抽出中...")
    extracted_text = extract_text_from_pdf(pdf_file_path, page_to_read)
    
    # 抽出されたテキストが空文字列でないか、かつエラーメッセージでないかを確認
    if extracted_text and not extracted_text.startswith("エラー:"):
        # 空白文字だけの可能性もあるため、strip()で前後の空白を削除してチェック
        if extracted_text.strip():
            print("テキストの抽出に成功しました。")
            print("--- 抽出されたテキスト ---")
            print(extracted_text[:100] + "..." if len(extracted_text) > 100 else extracted_text)
            print("\n音声データを生成中...")
            audio_data = generate_voice(extracted_text)
            
            if audio_data:
                print("音声データの生成に成功しました。再生を開始します。")
                play_audio(audio_data)
                print("再生が完了しました。")
            else:
                print("音声データの生成に失敗しました。")
        else:
            print("このページには読み上げ可能なテキストが含まれていません。")
    else:
        print(extracted_text)