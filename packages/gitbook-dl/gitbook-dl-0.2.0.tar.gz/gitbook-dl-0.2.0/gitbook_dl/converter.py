from typing import Tuple

import pypandoc


def download(url: str) -> Tuple[str, str]:
    doc = pypandoc.convert_file(
        url, "md", extra_args=["--extract-media=tmp", "--atx-headers"]
    )
    header, body = doc.split("::: {.book-body}")
    body, _ = body.split("::: {.search-results}")
    body = "::: {.book}\n::: {.book-body}" + body + "\n:::" * 6
    return (header, body)


def to_docx(body: str) -> str:
    return pypandoc.convert_text(body, "docx", format="md", outputfile="tmp.docx")
