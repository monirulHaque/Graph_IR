# import libraries
import lucene
print(lucene.initVM(vmargs=['-Djava.awt.headless=true']))
from java.nio.file import Paths
from java.io import File
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.store import  FSDirectory, NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import IndexReader, DirectoryReader
from org.apache.lucene.search import IndexSearcher, ScoreDoc, TopDocs
from org.apache.lucene.search.similarities import BM25Similarity

import pandas as pd


def BM25Search(index_path, q, annotated_docs, k1=1.2, b=0.75, search_field="body"):
    print("Query Search:", q)
    analyzer = EnglishAnalyzer()
    directory = FSDirectory.open(File(index_path).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(BM25Similarity(k1, b))
    query = QueryParser(search_field, analyzer).parse(q)
    scoreDocs = searcher.search(query, searcher.getIndexReader().numDocs()).scoreDocs
    print("Total number of matching Documents:", len(scoreDocs))
    news = set() # costly
    no_of_rel_docs_retrieved = 0
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # print(doc.get("doc_id"), doc.get("title"), scoreDoc.score)
        if scoreDoc.score < 4:
            break
        if doc.get("doc_id") in annotated_docs:
            no_of_rel_docs_retrieved += 1
        news.add(doc.get("title"))
    print("--------------------------------------------------------")
    print(len(news))
    print("--------------------------------------------------------")
    no_of_total_docs_retrieved = len(news)
    try:
        precision = no_of_rel_docs_retrieved / no_of_total_docs_retrieved
    except:
        precision = 0
    try:
        recall = no_of_rel_docs_retrieved / len(annotated_docs)
    except:
        recall = 0
    return precision, recall


dfq = pd.read_csv("WAPO_2018_core_queries.csv")
dfqrel = pd.read_csv("WAPO_2018_core_qrels.csv")
dfqrel = dfqrel[dfqrel['relevance'] > 0]

results = {}

for index, row in dfq.iterrows():
    ls = dfqrel[dfqrel['query_id'] == row["query_id"]]["doc_id"].tolist()
    print(len(ls))
    precision, recall = BM25Search("index/", row['title'], ls)
    results[row["query_id"]] = {"precision":precision, "recall":recall}


dfr = pd.DataFrame(results)
dfr.to_csv('results.csv')
