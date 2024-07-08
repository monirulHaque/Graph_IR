# import libraries
import lucene
print(lucene.initVM(vmargs=['-Djava.awt.headless=true']))
from java.nio.file import Paths
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.store import  FSDirectory, NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import IndexReader, DirectoryReader
from org.apache.lucene.search import IndexSearcher, ScoreDoc, TopDocs

import pandas as pd

def BM25Search(index_path, q, k1=1.2, b=0.75, search_field="body", field_to_retrieve='title'):
    print("Query Search:", q)
    analyzer = EnglishAnalyzer()
    directory = FSDirectory(File(index_path).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(BM25Similarity(k1, b))
    query = QueryParser(search_field, analyser).parse(q)
    scoreDocs = searcher.search(query, top_size).soreDocs
    print("Total number of matching Documents:", len(scoreDocs))
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print(doc.get(field_to_retrieve))

