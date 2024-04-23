from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.node_parser import NodeParser
from llama_index.core import Document
def sentence_window_retrieval(documents:[Document]):
    NodeParser()
    node_parser=SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="key",
        original_text_metadata_key="text"
    )
    return node_parser.get_nodes_from_documents(documents=documents)

