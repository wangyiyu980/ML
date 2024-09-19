import pymupdf4llm
import pathlib
md_text = pymupdf4llm.to_markdown(r'C:\Users\wangy\Desktop\test_table.pdf')
pathlib.Path(r'C:\Users\wangy\Desktop\output.md').write_bytes(md_text.encode())