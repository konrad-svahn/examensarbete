from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All

embeddings = GPT4AllEmbeddings()
db = FAISS.load_local("./customKnowlegeBase/knowlegebase", embeddings, allow_dangerous_deserialization = True)

question = input("Enter your question: ")
docs = db.similarity_search(question)
context = docs[0].page_content + " " + docs[1].page_content

print(context)

template = """
Please use the following context to answer questions.
Context: {context}
---
Question: {question}
Answer: """

prompt = PromptTemplate(template=template, input_variables=["context", "question"]).partial(context=context)

callbacks = [StreamingStdOutCallbackHandler()]
local_path = './models/mistral-7b-openorca.Q4_0.gguf'
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)
llm_chain.run(question)#"""
