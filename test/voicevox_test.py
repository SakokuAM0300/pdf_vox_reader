import requests
import json

# VOICEVOXが稼働しているAPIサーバーのURL
# デフォルトではlocalhostのポート50021を使用
VOICEVOX_API_URL = "http://localhost:50021"

def generate_voice(text, speaker_id=1):
    """
    VOICEVOX APIを使ってテキストを音声データに変換する
    """
    try:
        # 1. 音声合成のためのクエリを生成
        params = {
            "text": text,
            "speaker": speaker_id,
        }
        res = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
        if res.status_code != 200:
            print(f"Error generating audio query: {res.text}")
            return None
        
        audio_query_data = res.json()
        
        # 2. クエリを使って音声データを生成
        res = requests.post(f"{VOICEVOX_API_URL}/synthesis", params={"speaker": speaker_id}, data=json.dumps(audio_query_data))
        if res.status_code != 200:
            print(f"Error synthesizing audio: {res.text}")
            return None
            
        return res.content  # WAV形式のバイナリデータ
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to VOICEVOX API: {e}")
        return None

if __name__ == "__main__":
    text_to_speak = "こんにちは、VOICEVOXのテストです。"
    print(f"「{text_to_speak}」の音声データを生成中...")
    
    # VOICEVOXの四国めたん（ノーマル）のスピーカーIDは3
    audio_data = generate_voice(text_to_speak, speaker_id=3)
    
    if audio_data:
        print("音声データの生成に成功しました。")
        import io
        from pydub import AudioSegment
        import simpleaudio as sa

        # `audio_data`はVOICEVOXから取得したWAV形式のバイナリデータ
        try:
            # バイナリデータをメモリ上のファイルとして読み込む
            audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            
            # 再生
            play_obj = sa.play_buffer(
                audio_segment.raw_data,
                num_channels=audio_segment.channels,
                bytes_per_sample=audio_segment.sample_width,
                sample_rate=audio_segment.frame_rate
            )
            
            # 再生が終了するまで待機
            play_obj.wait_done()
            print("音声の再生が完了しました。")

        except Exception as e:
            print(f"音声の再生中にエラーが発生しました: {e}")
    else:
        print("音声データの生成に失敗しました。VOICEVOXが起動しているか、リモート接続が有効になっているか確認してください。")
        