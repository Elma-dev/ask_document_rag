from llama_index.core import DocumentSummaryIndex, Document


def summarize_document(documents:[Document]):
    DocumentSummaryIndex.from_documents(documents=documents)