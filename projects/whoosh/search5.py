from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
import os, os.path
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser
import sys
import configparser

def index_search(dirname, search_fields, search_query, numResult):
    ix = index.open_dir(dirname)
    schema = ix.schema
    numOutput=int(numResult)

    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(search_fields, schema, group = og)

    
    q = mp.parse(search_query)
    
    
    with ix.searcher() as s:
        results = s.search(q, terms=True, limit = 10)
        print("Search Results: ")
        
        for i in range(0, numOutput):
            # print(results[0:])
            docWithPath = results[i]['path']
            textcontent= results[i]["textdata"]
            # print(docWithPath, "\n", textcontent)
            print("Doc name: ", docWithPath[docWithPath.rindex('/')+1:], "\n", textcontent)
        

config = configparser.RawConfigParser()
config.read("configFile.properties")
query = config.get("ParameterSearch", "query")
indexDir=config.get("ParameterSearch", "indexDir")
numResult=config.get("ParameterSearch", "numResult")

# query = str(sys.argv[1])
results_dict = index_search("indexdir", ['title','content'], query, numResult)
