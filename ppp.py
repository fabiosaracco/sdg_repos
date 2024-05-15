# pdf pre-processing
from pypdf import PdfReader

def ppp(file, page=None):
    reader = PdfReader(file)
    
    if reader.is_encrypted:
        reader.decrypt(password='')
        
    n_pages=reader.get_num_pages()
    # all pages
    pages=reader.flattened_pages
    
    if page is not None:
        assert type(page)==int and page<n_pages
        text=pages[page].extract_text()
    else:
        # make all text in the same page
        pages=[p.extract_text() for p in pages]
        text=' '.join(pages)
    # delete new line
    text=' '.join(text.split('\n'))
    return text
    
