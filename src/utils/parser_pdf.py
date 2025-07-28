import requests
import fitz 
import io

def get_text_from_pdf_url(url: str) -> str:
    """
    Baixa um arquivo PDF de uma URL, extrai e retorna todo o seu conteúdo de texto.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  

        pdf_file = io.BytesIO(response.content)
        
        full_text = ""
        with fitz.open(stream=pdf_file, filetype="pdf") as doc:
            for page in doc:
                full_text += page.get_text()
        
        return full_text

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF da URL {url}: {e}")
        raise  
    except Exception as e:
        print(f"Erro ao processar o arquivo PDF: {e}")
        raise