import tkinter as tk
from tkinter import ttk
import threading
from voice_generator import generate_voice, AudioPlayer
from pdf_reader import get_pdf_page_count, extract_text_from_pdf

# グローバルな再生オブジェクトとPDF情報を保持
player = AudioPlayer()
pdf_info = {
    "path": "sample.pdf",
    "total_pages": 0,
    "current_page": 0
}
text_buffer = ""

# GUIアプリケーションのクラス
class PdfVoxReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Voice Reader")
        self.geometry("400x200")
        
        self.is_playing = False
        self.is_paused = False

        self.create_widgets()
        
    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # 再生コントロールボタンを配置するフレーム
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)

        # 再生/一時停止ボタン
        self.play_pause_button = ttk.Button(
            control_frame, 
            text="再生 / 一時停止", 
            command=self.toggle_play_pause
        )
        self.play_pause_button.pack(side="left", padx=5)

        # 前へボタン
        self.prev_button = ttk.Button(
            control_frame, 
            text="前へ", 
            command=self.prev_page
        )
        self.prev_button.pack(side="left", padx=5)

        # 次へボタン
        self.next_button = ttk.Button(
            control_frame, 
            text="次へ", 
            command=self.next_page
        )
        self.next_button.pack(side="left", padx=5)

        # 音量調整スライダー
        volume_label = ttk.Label(main_frame, text="音量:")
        volume_label.pack(pady=(10, 0))
        
        self.volume_slider = ttk.Scale(
            main_frame,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.set_volume
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(pady=5, fill="x")

    def toggle_play_pause(self):
        # 現在再生中かつ一時停止中でない場合
        if player.is_playing and not player.is_paused:
            player.pause()
        # 一時停止中の場合
        elif not player.is_playing and player.is_paused:
            player.resume()
        # 初回再生または再生終了後の場合
        elif not player.is_playing and not player.is_paused:
            self.start_playback()

    def start_playback(self):
        # メインスレッドをブロックしないよう、別スレッドで処理を開始
        threading.Thread(target=self._run_playback_thread, daemon=True).start()

    def _run_playback_thread(self):
        print("音声データの生成を開始します...")
        extracted_text = extract_text_from_pdf(pdf_info["path"], pdf_info["current_page"])
        
        if extracted_text and extracted_text.strip() and not extracted_text.startswith("エラー:"):
            print("テキストの抽出に成功しました。音声データを生成中...")
            audio_data = generate_voice(extracted_text)
            if audio_data:
                print("音声データの生成に成功しました。再生を開始します。")
                player.play(audio_data)
                print("再生が完了しました。")
            else:
                print("音声データの生成に失敗しました。")
        else:
            print("このページには読み上げ可能なテキストがありません。")

    # 現時点では何もしない
    def prev_page(self):
        print("前へボタンが押されました")

    # 現時点では何もしない
    def next_page(self):
        print("次へボタンが押されました")

    # 音量スライダーの機能は今後のステップで実装
    def set_volume(self, value):
        volume_percent = int(float(value))
        player.set_volume(volume_percent)

if __name__ == "__main__":
    app = PdfVoxReaderApp()
    app.mainloop()