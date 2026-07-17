from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import pgvectorTableSchema , pgvectorDistanceMethodEnums , pgvectorIndexTypeEnums
import logging
from typing import List
from models.db_schemas import retrievedchunk
from sqlalchemy.sql import text as sql_text

class pgvectorDB(VectorDBInterface):
    def __init__(self, db_client : str , distance_metric : str , default_vector_size : int = 786):
        self.client = db_client
        self.distance_metric = distance_metric
        self.default_vector_size = default_vector_size

        self.table_prefix = pgvectorTableSchema._PREFIX.value
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        async with self.client() as session:
            async with session.begin():
                await session.execute(sql_text("CREATE EXTENSION IF NOT EXISTS vector"))

            await session.commit()

    async def disconnect(self):
        pass

    async def is_collection_exists(self, collection_name:str) -> bool:
        async with self.client() as session:
            async with session.begin():
                list_tbl = sql_text('SELECT * FROM pg_tables WHERE tablename = :collection_name')
                session_result = await session.execute(list_tbl, {'collection_name': f"{collection_name}"})
                record = session_result.scalar_one_or_none()
            
        return record 

    async def list_all_collections(self) -> List:
        async with self.client() as session:
            async with session.begin():
                list_tbl = sql_text('SELECT tablename FROM pg_tables WHERE tablename LIKE :prefix')
                session_result = await session.execute(list_tbl, {'prefix': f"{self.table_prefix}"})
                records = session_result.scalars().all()
        return records
    
    async def get_collection_info(self, collection_name:str):
        async with self.client() as session:
            async with session.begin():
                table_info_sql = sql_text('''SELECT schemaname, tablename, tableowner, tablespace, hasindexes 
                                        FROM pg_tables WHERE tablename = :collection_name
                ''')
                count_sql = sql_text('''SELECT COUNT(*) FROM :collection_name''')

                table_info = await session.execute(table_info_sql, {'collection_name': f"{collection_name}"})
                table_count = await session.execute(count_sql, {'collection_name': f"{collection_name}"})

                table_data = table_info.fetchone()
                if not table_data:
                    return None
                
                return {
                    "table_info" : dict(table_data),
                    "table_count" : table_count.scalar_one()
                }
            
    
    async def delete_collection(self, collection_name:str):
        async with self.client() as session:
            async with session.begin():
                self.logger.info(f"Dropping collection {collection_name}...")
                drop_table_sql = sql_text('DROP TABLE IF EXISTS :collection_name')
                await session.execute(drop_table_sql, {'collection_name': f"{collection_name}"})
                await session.commit()

            
            return True
        
    async def create_collection(self, collection_name:str, embedding_size:int, do_reset:bool = False):
        if do_reset:
            await self.delete_collection(collection_name)

        if await self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} already exists. Skipping creation.")
            return False
        
        async with self.client() as session:
            async with session.begin():
                self.logger.info(f"Creating collection {collection_name} with embedding size {embedding_size}...")
                create_table_sql = sql_text('CREATE TABLE :collection_name ('
                                            f'{pgvectorTableSchema.ID.value} bigserial PRIMARY KEY, '
                                            f'{pgvectorTableSchema.TEXT.value} text, '
                                            f'{pgvectorTableSchema.VECTOR.value} vector({embedding_size}), '
                                            f'{pgvectorTableSchema.METADATA.value} jsonb DEFAULT \'{{}}\', '
                                            f'{pgvectorTableSchema.CHUNK_ID.value} integer,'
                                            f'FOREIGN KEY ({pgvectorTableSchema.CHUNK_ID.value}) REFERENCES chunks(chunk_id) ON DELETE CASCADE'
                                            ')')
                await session.execute(create_table_sql, {'collection_name': f"{collection_name}"})
                await session.commit()

                return True
            
    async def insert_collection(self, collection_name:str, text:str, vector:list, metadata:dict = None, record_id:str = None):
        
        is_collection_exists = await self.is_collection_exists(collection_name)
        if not is_collection_exists:
            self.logger.warning(f"Collection {collection_name} does not exist. Skipping insertion.")
            return False

        if not record_id:
            self.logger.warning(f"Record ID is required for insertion. Skipping insertion.")
            return False
        
        async with self.client() as session:
            async with session.begin():
                self.logger.info(f"Inserting record into collection {collection_name}...")
                insert_sql = sql_text(f'INSERT INTO :collection_name ({pgvectorTableSchema.TEXT.value}, {pgvectorTableSchema.VECTOR.value}, {pgvectorTableSchema.METADATA.value}, {pgvectorTableSchema.CHUNK_ID.value}) VALUES (:text, :vector, :metadata, :chunk_id)')
                await session.execute(insert_sql, {'collection_name': f"{collection_name}",
                                                    'text': text,
                                                    'vector': "[" + ", ".join(str(x) for x in vector) + "]",
                                                    'metadata': metadata or {},
                                                    'chunk_id': record_id})
                await session.commit()

                return True
        


    async def insert_collection_batch(self, collection_name:str, texts:list, vectors:list, metadatas:list = None, record_ids:list = None, batch_size:int = 100): 

        if not await self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} does not exist. Skipping batch insertion.")
            return False

        if len(vectors) != len(record_ids) or len(vectors) != len(texts):
            self.logger.warning(f"Vectors, record_ids, and texts must have the same length. Skipping batch insertion.")
            return False
        
        if len(metadatas) == 0 or metadatas is None:
            metadatas = [{}] * len(vectors)

        async with self.client() as session:
            async with session.begin():
                self.logger.info(f"Inserting batch of records into collection {collection_name}...")
                for i in range(0, len(vectors), batch_size):
                    batch_texts = texts[i:i + batch_size]
                    batch_vectors = vectors[i:i + batch_size]
                    batch_metadatas = metadatas[i:i + batch_size]
                    batch_record_ids = record_ids[i:i + batch_size]

                    values = []
                    for _text, _vector, _metadata, _record_id in zip(batch_texts, batch_vectors, batch_metadatas, batch_record_ids):
                        values.append({
                            "text" : _text,
                            "vector" : "[" + ", ".join(str(x) for x in _vector) + "]",
                            "metadata" : _metadata or {},
                            "chunk_id" : _record_id
                        })

                    batch_insert_sql = sql_text(f'INSERT INTO :collection_name {pgvectorTableSchema.TEXT.value}, {pgvectorTableSchema.VECTOR.value}, {pgvectorTableSchema.METADATA.value}, {pgvectorTableSchema.CHUNK_ID.value} VALUES (:text, :vector, :metadata, :chunk_id)')
                    await session.execute(batch_insert_sql, values, {'collection_name': f"{collection_name}"})
                    

                return True
            
    async def search_collection_by_vector(self, collection_name:str , vector:list , limit:int = 10) -> List[retrievedchunk]:

        if not await self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} does not exist. Skipping batch insertion.")
            return False
        
        vector = "[" + ", ".join(str(x) for x in vector) + "]"
        async with self.client() as session:
            async with session.begin():
                self.logger.info(f"Searching collection {collection_name} by vector...")
                search_sql = sql_text(f'SELECT {pgvectorTableSchema.TEXT.value} as text , {pgvectorTableSchema.VECTOR.value} <=> :vector as score',
                                    'FROM :collection_name ',
                                    'ORDER BY score DESC ',
                                    'LIMIT :limit')
                session_result = await session.execute(search_sql, {'collection_name': f"{collection_name}",
                                                                    'vector': vector,
                                                                    'limit': limit})
                records = session_result.fetchall()
                
                return {
                    retrievedchunk(**{
                        "text" : record.text,
                        "score" : record.score
                    })

                    for record in records
                }