# import libraries
import lucene
print(lucene.initVM(vmargs=['-Djava.awt.headless=true']))
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader
from java.io import File
import org.apache.lucene.document as document
from org.apache.lucene.store import SimpleFSDirectory, FSDirectory
# from org.apache.lucene.search import IndexSearcher, BM25Similarity

indexPath = File("index/").toPath()
indexDir = FSDirectory.open(indexPath)
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(indexDir, config)

import pandas as pd

# load dataset
df = pd.read_csv('WAPO_2018_news_10000.csv', low_memory=False)
print(df.head(10))
print(df.info())