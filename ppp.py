# pdf pre-processing
from pypdf import PdfReader

def ppp(file, page=None):
    reader = PdfReader(file)
    
    if reader.is_encrypted:
        reader.decrypt(password='')
        
    n_pages=len(reader.pages)
    
    if page is not None:
        assert type(page)==int and page<n_pages
        text=reader.pages[page].extract_text()
    else:
        # make all text in the same page
        pages=[reader.pages[p].extract_text() for p in range(n_pages)]
        text=' '.join(pages)
    # delete new line
    text=' '.join(text.split('\n'))
    return text
    
