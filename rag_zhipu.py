# @author yangyunlong 

import chromadb
from zhipuai import ZhipuAI
import os


class ChromaDB():

    def __init__(self, path):
        self.path = path
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("search")

    def load(self, file_path):
        self.path = file_path
        self.client = chromadb.PersistentClient(path=file_path)
        self.collection = self.client.get_collection("search")

    def search(self, vector, n_results):
        results = self.collection.query(query_embeddings=[vector],
                                        n_results=n_results)
        return results['documents'][0]

    def from_texts(self, vectors, documents):
        ids = []
        for i, doc in enumerate(documents):
            ids.append(str(i) + "_" + doc)
        self.collection.add(embeddings=vectors, documents=documents, ids=ids)

    def add_texts(self, vectors, documents, ids):
        self.collection.upsert(embeddings=vectors, documents=documents, ids=ids)


class TextLoader():

    def __init__(self, file_path, encoding):
        self.file_path = file_path
        self.encoding = encoding

    def load(self):
        """Load from file path."""
        text = ""
        try:
            with open(self.file_path, encoding=self.encoding) as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError("Error loading {text}".format(text=self.file_path)) from e
        return [text]


def extract_file_dirs(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):

        for file in files:
            fp = os.path.join(root, file)
            file_paths.append(fp)
    return file_paths

def split_chunks(text, chunk_size):
    docs = []
    doc_size = 0
    tmp = []
    
    for line in text.split("\n"):
        line = line.strip()
        if len(line) + doc_size < chunk_size:
            tmp.append(line)
            doc_size += len(line)
        else:
            docs.append("\n".join(tmp))
            tmp = []
            doc_size = 0
    
    # 添加最后一个块（如果存在）
    if tmp:
        docs.append("\n".join(tmp))
    
    return docs


def generate_prompt(query, docs):
    PROMPT_TEMPLATE = """
    已知信息：
    {context} 

    根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 
    问题是：{question}"""
    context = []
    for index, doc in enumerate(docs):
        doc = doc.strip()
        f_prompt = "<{a}>: {b}".format(a=index + 1, b=doc)
        context.append(f_prompt)
    context = "\n".join(context)
    prompt = PROMPT_TEMPLATE.replace("{question}", query).replace("{context}",
                                                                  context)
    return prompt


def get_zhipu_client():
    api_key="填写您自己的APIKey"
    client = ZhipuAI(api_key=api_key) # 填写您自己的APIKey
    return client


def get_embeddings(embedding_input):
    client = get_zhipu_client()
    embeddings_result = []
    for emb_input in embedding_input:
        embeddings = client.embeddings.create(
        model="embedding-2",
        input=emb_input)

        embeddings_result.append(embeddings.data[0].embedding)  

    return embeddings_result


def run():
    FILE_PATH = "./zsxq"
    files = extract_file_dirs(FILE_PATH)    
    loaders = [TextLoader(f, encoding='utf-8') for f in files]

    docs = []
    for l in loaders:
        docs.extend(l.load())
    chunks = []
    for doc in docs:
        chunk = split_chunks(doc, 150)
        chunks.extend(chunk)
    
    path = "./zhipu_data"
    vectordb = ChromaDB(path) 
    num = vectordb.collection.count()    
    if len(chunks)>num:
        print("load embedding ...")
        emb = get_embeddings(chunks)        
        vectordb.from_texts(emb, chunks)

    query = "运营知识星球有什么好处"
    embedding = get_embeddings([query])[0]
    result = vectordb.search(embedding, 4)
    prompt = generate_prompt(query, result)

    generate_for_llm = True
    # 调用 OpenAI 的 API 生成回答
    if generate_for_llm:
        client = get_zhipu_client()
        response = client.chat.completions.create(
            model="glm-4",
            messages=[{"role": "user", "content": prompt}])
        print(response.choices[0].message.content)


if __name__ == "__main__":
    run()

