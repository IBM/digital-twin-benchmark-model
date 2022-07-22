import argparse
import json
import os
import sys
import time

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions, POST
from py2neo import Graph


def run_queries_sparql(sparql: SPARQLWrapper, sparqlU: SPARQLWrapper, runs: int, queries: list, output: str):
    queries_stats = []
    queries.sort(key=lambda q: q["id"])
    for q in queries:
        avg_time = 0
        print(f"Query: {q['id']}")
        times = []
        res = []
        for it in range(runs):
            start = time.time() * 1000
            try:
                if "INSERT" in q["query"]:
                    sparqlU.setMethod(POST)
                    sparqlU.setQuery(q["query"])
                    if "7200" in sparqlU.endpoint:
                        sparqlU.addParameter('infer', 'true')
                        sparqlU.addParameter('action', 'UPDATE')
                    _ = sparqlU.query()
                    result = {"results":{"bindings":[]}}
                else:
                    sparql.setMethod(POST)
                    sparql.setQuery(q["query"])
                    result = sparql.queryAndConvert()
            except SPARQLExceptions.QueryBadFormed as e:
                print(f"Error for query {q['id']} and run {it + 1}")
                print(e.__cause__)
                continue
            end = time.time() * 1000
            total_time = (end - start)
            avg_time += total_time
            times.append(total_time)
            res.append(len(result["results"]["bindings"]))
        queries_stats.append({"query": q["id"], "total_avg_time": avg_time / runs, "times": times, "result_size": res})
    outfile = open(output, "w")
    json.dump(queries_stats, outfile, indent=4)
    outfile.close()

def run_queries_cypher(cypher: Graph, runs: int, queries: list, output: str):
    queries_stats = []
    queries.sort(key=lambda q: q["id"])
    for q in queries:
        avg_time = 0
        print(f"Query: {q['id']}")
        times = []
        res = []
        for it in range(runs):
            start = time.time() * 1000
            try:
                result = cypher.run(q["query"]).data()
            except Exception as e:
                print(f"Error for query {q['id']} and run {it + 1}")
                print(e.__cause__)
                continue
            end = time.time() * 1000
            total_time = (end - start)
            avg_time += total_time
            times.append(total_time)
            res.append(len(result))
        queries_stats.append({"query": q["id"], "total_avg_time": avg_time / runs, "times": times, "result_size": res})
    outfile = open(output, "w")
    json.dump(queries_stats, outfile, indent=4)
    outfile.close()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lang', default="sparql")
    parser.add_argument('-e', '--endpoint')
    parser.add_argument('-u', '--updateendpoint')
    parser.add_argument('-q', '--queriesdir')
    parser.add_argument('-r', '--runs', default="1")
    parser.add_argument('-o', '--output', default="results.json")
    args = parser.parse_args()
    lang = args.lang
    endpoint = args.endpoint
    updateendpoint = args.updateendpoint
    queriesdir = args.queriesdir
    runs = int(args.runs)
    output = args.output

    queries = []
    dir_list = os.listdir(queriesdir)
    print(dir_list)
    for f in dir_list:
        qid = int(f.split(".")[0].split("query")[1])
        with open(queriesdir + f, 'r') as query:
            queries.append({"id": qid, "query": query.read().rstrip()})

    if lang == "cypher":
        cypher = Graph(endpoint)
        run_queries_cypher(cypher, runs, queries, output)
    else:
        sparql = SPARQLWrapper(endpoint)
        sparql.setReturnFormat(JSON)
        if updateendpoint:
            sparqlU = SPARQLWrapper(updateendpoint)
            sparqlU.setReturnFormat(JSON)
        else:
            sparqlU = sparql
        run_queries_sparql(sparql, sparqlU, runs, queries, output)


if __name__ == "__main__":
    main(sys.argv[1:])
