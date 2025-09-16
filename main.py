from pdf_reader import get_pdf_page_count, extract_text_from_pdf
from voice_generator import generate_and_play_voice

def main():
    """
    PDFファイルを読み込み、全ページのテキストを抽出して音声化する
    """
    pdf_file_path = r"C:\Users\oneof\OneDrive\デスクトップ\研究室関連\参考レポート\大学出版119［神-人間_高橋］.pdf"
    
    # PDFの総ページ数を取得
    page_count = get_pdf_page_count(pdf_file_path)
    if page_count is None:
        return # エラーが発生した場合、プログラムを終了

    print(f"総ページ数: {page_count} のPDFを読み上げます。")
    
    # ページごとにループを回して処理
    for page_num in range(page_count):
        print(f"\n--- ページ {page_num + 1} の読み上げを開始します ---")
        extracted_text = extract_text_from_pdf(pdf_file_path, page_num)
        
        if extracted_text and not extracted_text.startswith("エラー:"):
            # 抽出されたテキストが空欄ではないかチェック
            if extracted_text.strip():
                print("テキストの抽出に成功しました。音声データを生成し、再生します。")
                generate_and_play_voice(extracted_text)
            else:
                print("このページには読み上げ可能なテキストが含まれていません。スキップします。")
        else:
            print(extracted_text) # エラーメッセージを表示

    print("\nすべてのページの読み上げが完了しました。")

if __name__ == "__main__":
    main()