#### RAG with Knowledge Graph


#### Overview
Retrieval Augmented Generation(RAG) is a way of generating reliable answers from LLM using an external knowledge base. This project shows how to use RAG with a knowledge graph using Weaviate as the vector database and the exllamav2 implementation of the mistral orca model.

The following is the pipeline -

1. Extract text from a PDF
2. Chunk the data into k size with w overlap.
3. Extract (source, relation, target) from the chunks and create a knowledge graph
4. Extract embeddings for the nodes and relationships.
5. Store the text and vectors in weaviate vector database.
6. Apply a keyword search on the nodes and retrieve the top k chunks.
7. Generate the answer from the top k retrieved chunks.
8. You can also visualize the sub-graph of the nodes used to generate the answer.