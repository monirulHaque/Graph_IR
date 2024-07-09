# import libraries
import lucene
print(lucene.initVM(vmargs=['-Djava.awt.headless=true']))
from java.nio.file import Paths
# from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader
from java.io import File
import org.apache.lucene.document as document
from org.apache.lucene.store import  FSDirectory, NIOFSDirectory
# from org.apache.lucene.search import IndexSearcher, BM25Similarity

import pandas as pd

indexPath = File("index/").toPath()
indexDir = FSDirectory.open(indexPath)
analyzer = EnglishAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(indexDir, config)


def indexSingleNews(title, body, doc_id):
    doc = document.Document()
    doc.add(document.Field("doc_id", doc_id, TextField.TYPE_STORED))
    doc.add(document.Field("title", title, TextField.TYPE_STORED))
    doc.add(document.Field("body", body, TextField.TYPE_STORED))
    writer.addDocument(doc)
    
def makeInvertedIndex(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    for i, row in df.iterrows():
        indexSingleNews(row['title'], row['body'], row["doc_id"])
    writer.commit()


makeInvertedIndex('WAPO_2018_docs.csv')
