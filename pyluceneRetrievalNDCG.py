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
import math


def BM25Search(index_path, q, matched_qrels, k1=1.2, b=0.75, search_field="body"):
    annotated_docs = matched_qrels["doc_id"].tolist()
    matched_qrels = matched_qrels.sort_values(by='relevance', ascending=False)
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
    i = 0
    total_relavant_docs = len(annotated_docs)
    precisionList = []
    cumulative_gain = 0
    discounted_cumulative_gain = {}
    k = 10
    q = 0
    for scoreDoc in scoreDocs:
        i += 1
        doc = searcher.doc(scoreDoc.doc)
        if doc.get("doc_id") in annotated_docs:
            no_of_rel_docs_retrieved += 1
            cumulative_gain += matched_qrels.loc[matched_qrels["doc_id"] == doc.get("doc_id")]["relevance"].to_numpy()[0]
        if i < 3:
            discounted_cumulative_gain[i-1] = cumulative_gain
        else:
            discounted_cumulative_gain[i-1] = discounted_cumulative_gain[i-2] + dfqrel[doc.get("doc_id")]/math.log(i-1, 2)
        news.add(doc.get("title"))
        if i == k:
            break
    i = 0
    cumulative_gain = 0
    ideal_cumulative_gain = {}
    for index, row in matched_qrels.iterrows():
        i += 1
        cumulative_gain += row["relevance"]
        if i < 3:
            ideal_cumulative_gain[i-1] = cumulative_gain
        else:
            ideal_cumulative_gain[i-1] = ideal_cumulative_gain[i-2] + row["relevance"]/math.log(i-1, 2)
        if i == k:
            break
    normalized_discounted_cumulative_gain = 
    return 


dfq = pd.read_csv("WAPO_2018_core_queries.csv")
dfqrel = pd.read_csv("WAPO_2018_core_qrels.csv")
dfqrel = dfqrel[dfqrel['relevance'] > 0]
print(dfqrel)

results = {}

for index, row in dfq.iterrows():
    # ls = dfqrel[dfqrel['query_id'] == row["query_id"]]["doc_id"].tolist()
    ls = dfqrel[dfqrel['query_id'] == row["query_id"]]
    ndcg = BM25Search("index/", row['title'], ls)
    results[row["query_id"]] = {"ndcg":ndcg}

avgNDCG = 0

for key in results:
    avgNDCG += results[key]['ndcg']
results["Average NDCG"] = avgNDCG/len(results)
dfr = pd.DataFrame(results)
dfr = dfr.T
dfr.to_csv('resultsNDCG.csv')