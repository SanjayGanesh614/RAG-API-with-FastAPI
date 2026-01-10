import chromadb

client = chromadb.PersistentClient(path = "./db")  # creates a path for chromadb to permanently store everything at this path and then saves to disk
collection = client.get_or_create_collection(name = "docs") #this created or get the collection docs

with open("k8s.txt", "r") as f:
    text = f.read()

collection.add(documents = [text], ids=["k8s"])

print("Embedding stored in Chroma")
