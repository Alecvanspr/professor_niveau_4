from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi import HTTPException


def _decode_text(data: bytes) -> str:
    return data.decode('utf-8', errors='ignore')


def _extract_pdf_text(data: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                'PDF-upload is geconfigureerd, maar de server mist pypdf. '
                'Installeer backend dependencies met: pip install -r backend/requirements.txt '
                'of minimaal: pip install pypdf'
            ),
        ) from exc

    reader = PdfReader(io.BytesIO(data))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or '')

    return '\n'.join(parts).strip()


def _extract_zip_text(data: bytes) -> str:
    sections: list[str] = []

    with zipfile.ZipFile(io.BytesIO(data), 'r') as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue

            suffix = Path(info.filename).suffix.lower()
            with archive.open(info, 'r') as file_handle:
                file_data = file_handle.read()

            if suffix in {'.txt', '.md'}:
                content = _decode_text(file_data)
            elif suffix == '.pdf':
                content = _extract_pdf_text(file_data)
            else:
                continue

            if content.strip():
                sections.append(f"### Bestand: {info.filename}\n{content.strip()}")

    if not sections:
        raise HTTPException(
            status_code=400,
            detail='ZIP bevat geen ondersteunde documenten (.txt, .md, .pdf) met leesbare inhoud.',
        )

    return '\n\n'.join(sections)


def extract_document_content(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()

    if suffix in {'.txt', '.md'}:
        content = _decode_text(data)
    elif suffix == '.pdf':
        content = _extract_pdf_text(data)
    elif suffix == '.zip':
        content = _extract_zip_text(data)
    else:
        raise HTTPException(status_code=400, detail='Niet ondersteund bestandstype. Gebruik .txt, .md, .pdf of .zip')

    if not content.strip():
        raise HTTPException(status_code=400, detail='Geen leesbare tekst gevonden in het aangeleverde document.')

    return content.strip()
