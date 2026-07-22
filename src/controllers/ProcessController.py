from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import PyMuPDFLoader , TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessEnums

class ProcessController(BaseController):
    def __init__(self,project_id:str):
        self.projectpath = ProjectController().get_file_path(project_id=project_id)

    def get_file_extension(self,filename:str):
        return os.path.splitext(filename)[-1]
    
    def get_file_loader(self, filename:str):
        file_extension = self.get_file_extension(filename)
        file_path = os.path.join(
            self.projectpath,
            filename
        )

        if os.path.exists(file_path) is False:
            return None
        
        if file_extension == ProcessEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_extension == ProcessEnums.TXT.value:
            return TextLoader(
                        file_path,
                        encoding="utf-8"
                    )
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
    def get_file_content(self , project_id:str , filename:str):
        loader = self.get_file_loader(filename)
        if loader:
            return loader.load()
        else:
            return None

    def process_file_content(self, file_content: list, file_id:str,
                            chunk_size: int = 100, chunk_overlap: int = 20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len)
        
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]
        file_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_metadata)
        

        return chunks