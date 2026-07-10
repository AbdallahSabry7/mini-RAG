from string import Template

system_prompt = Template("/n".join([
    "you are a helpful assistant that generate answers based on documents provided",
    "you are given a question and a set of documents, your task is to find the most relevant information from the documents and use it to answer the question",
    "if the answer is not contained within the documents, say 'I could not find an answer in the provided documents.'",
    "answer the question in query language, do not translate the answer into another language",
    "be precise and concise, do not add any additional information that is not present in the documents",
]))

document_template = Template("/n".join([
    "##Document $index:\n",
    "###Content: $content\n",
    "###Score: $score\n"
]))

footer_template = Template("/n".join([
    "Please provide a concise and accurate answer to the question based on the information from the documents above. ",
    "If the answer is not contained within the documents, say 'I could not find an answer in the provided documents.'",
    "##Answer:"
]))