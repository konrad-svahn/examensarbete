from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All

embeddings = GPT4AllEmbeddings()
db = FAISS.load_local("./knowlegebaseSv", embeddings, allow_dangerous_deserialization = True)

question = input("Ställ en fråga: ")
docs = db.similarity_search(question)
context = docs[0].page_content + " " + docs[1].page_content
print(context)

template = """
svara på frågan med följande kontext: {context}
---
Fråga: {question}
Svar: """

prompt = PromptTemplate(template=template, input_variables=["context", "question"]).partial(context=context)

callbacks = [StreamingStdOutCallbackHandler()]
local_path = '../models/GPT-Sw3-356M-Instruct-f32-GGUF'
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)
llm_chain.run(question)