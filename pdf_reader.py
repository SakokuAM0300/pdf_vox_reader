import fitz

def get_pdf_page_count(pdf_path):
    """
    指定されたPDFファイルの総ページ数を取得する
    """
    try:
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        doc.close()
        return page_count
    except FileNotFoundError:
        print(f"エラー: 指定されたファイルが見つかりません - {pdf_path}")
        return None
    except Exception as e:
        print(f"PDFのページ数取得中にエラーが発生しました: {e}")
        return None

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

if __name__ == "__main__":
    # このファイル単体でのテスト用コード
    pdf_file_path = "sample.pdf"
    page_count = get_pdf_page_count(pdf_file_path)
    if page_count is not None:
        print(f"総ページ数: {page_count}")
        extracted_text = extract_text_from_pdf(pdf_file_path, 0)
        print("--- 抽出されたテキスト ---")
        print(extracted_text)