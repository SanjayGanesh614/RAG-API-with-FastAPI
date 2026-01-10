from fastapi import FastAPI
import chromadb
import ollama


app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection(name="docs")

@app.post("/query")
def query(q: str):
    results = collection.query(
        query_texts=[q], #gives a list of query text to chromadb to search for similar texts
        n_results=1 # get the top 1 most similar document
    )
    context = results['documents'][0][0] if results["documents"] else" No context found"  #[0][0] gets the first list of document and the next [0] gets the first document from that list

    answer = ollama.generate(
        model = "tinyllama",
        prompt =f"Context: \n{context} \n\nQuestion: {q}\n\nAnswer clearly and consisely:"
    )
    return {"answer": answer["response"]}
