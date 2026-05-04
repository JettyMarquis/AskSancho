"""
indexer.py — Project file vectorizer

Indexes project files (CLAUDE.md, HANDOFF.md, recent code) and
collector.py output into ChromaDB for RAG retrieval by refiner.py.

Status: TODO (High Version Phase A)
Dependencies: chromadb, sentence-transformers (or ollama embeddings)
"""

# TODO: implement ChromaDB indexing
# Key design decisions to make:
#   - Embedding model: ollama nomic-embed-text (local) vs sentence-transformers
#   - Chunking strategy: by section (##) for markdown, by function for code
#   - Update strategy: re-index on file mtime change

raise NotImplementedError("indexer.py is not yet implemented — High Version Phase A")
