import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    指定されたPDFファイルから最初のページのテキストを抽出する
    """
    try:
        # PDFファイルを開く
        doc = fitz.open(pdf_path)
        
        # 最初のページ（インデックス0）を取得
        page = doc[0]
        
        # ページ内のテキストを抽出
        text = page.get_text()
        
        # PDFを閉じる
        doc.close()
        
        return text
        
    except FileNotFoundError:
        return f"エラー: 指定されたファイルが見つかりません - {pdf_path}"
    except Exception as e:
        return f"PDFの読み込み中にエラーが発生しました: {e}"

if __name__ == "__main__":
    # ここにテストしたいPDFファイルのパスを記述
    # 例：my_book.pdf がプログラムと同じフォルダにある場合
    pdf_file_path = r"C:\Users\oneof\OneDrive\デスクトップ\電大アクセス\2025\統計学\3記述統計量１ (1).pdf"
    
    # PDFからテキストを抽出して表示
    extracted_text = extract_text_from_pdf(pdf_file_path)
    print("--- 抽出されたテキスト ---")
    print(extracted_text)