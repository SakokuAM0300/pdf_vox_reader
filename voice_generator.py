import requests
import json
import io
import time
from pydub import AudioSegment
import simpleaudio as sa
import threading

VOICEVOX_API_URL = "http://localhost:50021"

class AudioPlayer:
    def __init__(self):
        self.play_obj = None
        self.playback_thread = None
        self.is_playing = False
        self.is_paused = False
        self.audio_segment = None
        self.current_position = 0
        self.start_time = 0
        self.lock = threading.Lock()
        self.volume = 0 # デフォルトは0dB、つまり元の音量

    def _run_playback(self):
        try:
            with self.lock:
                if not self.audio_segment:
                    return

            # 音量調整を適用
            adjusted_segment = self.audio_segment[self.current_position:].apply_gain(self.volume)

            self.play_obj = sa.play_buffer(
                adjusted_segment.raw_data,
                num_channels=adjusted_segment.channels,
                bytes_per_sample=adjusted_segment.sample_width,
                sample_rate=adjusted_segment.frame_rate
            )
            
            with self.lock:
                self.start_time = time.time()
                self.is_playing = True
                self.is_paused = False

            self.play_obj.wait_done()
            
            with self.lock:
                self.is_playing = False
                self.is_paused = False
                self.current_position = 0
                
        except Exception as e:
            print(f"音声再生中にエラーが発生しました: {e}")
            with self.lock:
                self.is_playing = False
                self.is_paused = False
    
    def set_volume(self, volume_percent):
        """
        音量を設定する（0-100%）
        """
        # pydubの音量調整はデシベル(dB)で行う
        # dB = 20 * log10(volume_percent / 100)
        # 100% -> 0dB (元の音量)
        # 50% -> -6dB
        # 0% -> 負の無限大
        if volume_percent == 0:
            self.volume = -100 # ほぼ無音
        else:
            self.volume = 20 * (volume_percent / 100)**2 - 20 # 簡易的なカーブ
        print(f"Volume set to: {self.volume} dB")


    def play(self, audio_data):
        with self.lock:
            if self.is_playing:
                return
            
            self.audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            self.current_position = 0
            
            self.playback_thread = threading.Thread(target=self._run_playback, daemon=True)
            self.playback_thread.start()

    def pause(self):
        with self.lock:
            if self.is_playing and not self.is_paused:
                self.is_paused = True
                self.is_playing = False
                self.play_obj.stop()
                elapsed_time = time.time() - self.start_time
                self.current_position += elapsed_time * 1000
                
    def resume(self):
        with self.lock:
            if not self.is_playing and self.is_paused:
                self.playback_thread = threading.Thread(target=self._run_playback, daemon=True)
                self.playback_thread.start()

def generate_voice(text, speaker_id=3):
    """
    VOICEVOX APIを使ってテキストを音声データに変換する
    """
    try:
        params = {"text": text, "speaker": speaker_id}
        res = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
        res.raise_for_status()
        audio_query_data = res.json()
        
        res = requests.post(f"{VOICEVOX_API_URL}/synthesis", params={"speaker": speaker_id}, data=json.dumps(audio_query_data))
        res.raise_for_status()
        return res.content
    except requests.exceptions.RequestException as e:
        print(f"VOICEVOX API接続エラー: {e}")
        return None