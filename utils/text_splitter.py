"""
Text splitting utilities for handling long texts.
"""
import re


def split_text_by_sentences(text, max_chars=500):
    """
    Split text into chunks by sentences, respecting max character limit.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    # Split by sentence endings
    sentences = re.split(r'([.!?]\s+)', text)

    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        separator = sentences[i + 1] if i + 1 < len(sentences) else ""

        full_sentence = sentence + separator

        # If adding this sentence exceeds max_chars, start new chunk
        if len(current_chunk) + len(full_sentence) > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = full_sentence
        else:
            current_chunk += full_sentence

    # Add remaining text
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def split_text_by_paragraphs(text, max_chars=500):
    """
    Split text into chunks by paragraphs, respecting max character limit.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    # Split by paragraphs (double newline or single newline)
    paragraphs = text.split('\n')

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # If adding this paragraph exceeds max_chars, start new chunk
        if len(current_chunk) + len(paragraph) + 1 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph

    # Add remaining text
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def split_text_smart(text, max_chars=500, method='sentences'):
    """
    Smart text splitting with multiple methods.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk
        method: 'sentences' or 'paragraphs'

    Returns:
        List of text chunks
    """
    if method == 'paragraphs':
        chunks = split_text_by_paragraphs(text, max_chars)
    else:
        chunks = split_text_by_sentences(text, max_chars)

    # If any chunk is still too long, split it further
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            final_chunks.append(chunk)
        else:
            # Force split by words if still too long
            words = chunk.split()
            current = ""
            for word in words:
                if len(current) + len(word) + 1 > max_chars:
                    if current:
                        final_chunks.append(current.strip())
                    current = word
                else:
                    current += " " + word if current else word
            if current:
                final_chunks.append(current.strip())

    return final_chunks
