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



@app.post("/add")
def add_knowledge(text: str):
    """ Add new content to the knowledge base dynamically"""
    
    try:
        #Generates a uuid for this document
        import uuid
        doc_id = str(uuid.uuid4())

        #Add the text to the Chroma Collection
        collection.add(documents= [text], ids=[doc_id])

        return {
            "status": "Success",
            "message": "Document added successfully",
            "id": doc_id
        }

    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }



"""
 How can you reduce hallucination?






Provide more detailed context in your knowledge base (the more specific information you give, the less the model needs to invent)



Use larger, more capable models (like Llama 3.3 70B) that are better at sticking to provided context



Improve your prompts to explicitly tell the model to only use information from the context



Add validation in your API to check if responses match your knowledge base

RAG significantly reduces hallucination by providing relevant context, but it doesn't eliminate it completely - especially with smaller models. This is an active area of research in AI!"""

