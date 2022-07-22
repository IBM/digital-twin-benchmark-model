import argparse
import json
import os
import time
import aiohttp
import asyncio
import requests

from MAS_Data_Dictionary.KITT import KITT


def run_queries(api: KITT, runs: int, queries: list, output: str):
    queries_stats = []
    queries.sort(key=lambda q: q["id"])
    para={'limit': 1000, 'page': 0}
    cheader = {**api.header(), **{"Content-Type": "application/json"}}
    s = requests.Session()
    for q in queries:
        avg_time = 0
        print(f"Query: {q['id']} - Warmup")
        times = []
        res = []
        if "search" in q["query"]:
            urlq=f'{api.get_api_url()}/space/{api.spaceID}/graph/{api.graphID}/reasoning'
        else:
            urlq=f'{api.get_api_url()}/space/{api.spaceID}/graph/{api.graphID}'
        req = requests.Request('POST', urlq, json=q["query"], headers=cheader, params=para)
        prepped = req.prepare()
        for it in range(50): # warmup
            try:
                r = s.send(prepped)
            except Exception as e:
                print(f"Error for query {q['id']} and run {it + 1}")
                print(e,e.__cause__)
                continue
        for it in range(runs):
            if it % 50==0:
                print(f"Query: {q['id']} - {it}")
            start = time.time() * 1000
            try:
                r = s.send(prepped)
                if r.content:
                    result=r.json()
            except Exception as e:
                continue
            end = time.time() * 1000
            total_time = (end - start)
            avg_time += total_time
            times.append(total_time)
            res.append(len(result))
        queries_stats.append({"query": q["id"], "total_avg_time": avg_time / runs, "times": times, "result_size": res})
        time.sleep(20)
    outfile = open(output, "w")
    json.dump(queries_stats, outfile, indent=4)
    outfile.close()

async def run_queries_async(api: KITT, runs: int, queries: list, output: str):
    queries_stats = []
    queries.sort(key=lambda q: q["id"])
    para={'limit': 1000, 'page': 0}
    tic = time.time()
    for q in queries:
        print(f"Query: {q['id']} - Warmup")
        async with aiohttp.ClientSession() as s:
            times = []
            res = []
            api.invalidate_token()
            api.reauthenticate()
            cheader = {"Content-Type": "application/json", "Accepts": "application/json", "Accept-Encoding":"gzip, compress, br"}
            cheader['Authorization']=api.header()['Authorization']
            print(f"Total time: {(time.time() - tic)}s", cheader['Authorization'])
            dat = json.dumps(q["query"])
            if "search" in q["query"]:
                urlq=f'{api.get_api_url()}/space/{api.spaceID}/graph/{api.graphID}/reasoning'
            else:
                urlq=f'{api.get_api_url()}/space/{api.spaceID}/graph/{api.graphID}'
            for it in range(50): # warmup
                try:
                    async with s.post(urlq, data =dat, params=para, headers=cheader) as r:
                        await r.text()
                except Exception as e:
                    print(f"Error for query {q['id']} and run {it + 1}")
                    print(e,e.__cause__)
                    continue
            for it in range(runs):
                try:
                    if it % 50==0:
                        print(f"Query: {q['id']} - {it}")
                    api.reauthenticate()
                    cheader['Authorization']=api.header()['Authorization']
                    start = time.time()
                    async with s.post(urlq, data =dat, params=para, headers=cheader) as r:
                        result = await r.text()
                        end = time.time()
                    times.append(1000*(end - start))
                    res.append(len(json.loads(result)))
                except Exception as e:
                    print(f"Error for query {q['id']} and run {it + 1}")
                    print(e, e.__cause__)
                    #continue
                    break
            queries_stats.append({"query": q["id"], "total_avg_time": sum(times) / len(times) if times else 1, "times": times, "avg_result_size": sum(res) / len(res) if res else 1, "result_size": res})
            print(f"Query: {q['id']}; total_avg_time: {sum(times) / len(times) if times else 1}; total_time: {sum(times)}; avg_result_size: {sum(res)/len(res) if res else 1}")
            await s.close()
            time.sleep(10)
    outfile = open(output, "w")
    json.dump(queries_stats, outfile, indent=4)
    outfile.close()
    print(f"Total time: {(time.time() - tic)}s")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint')
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('-t', '--tenant')
    parser.add_argument('-g', '--graph')
    parser.add_argument('-q', '--queriesdir')
    parser.add_argument('-pg', '--pagination', default="2000")
    parser.add_argument('-r', '--runs', default="1")
    parser.add_argument('-o', '--output', default="results.json")
    args = parser.parse_args()
    endpoint = args.endpoint
    user = args.user
    password = args.password
    graph = args.graph
    queriesdir = args.queriesdir
    pagination = int(args.pagination)
    runs = int(args.runs)
    output = args.output
    tenant = args.tenant

    api = KITT(endpoint) \
        .login_usr(user, password) \
        .space_set(tenant).graph_set(graph) \
        .download_pagination_set(pagination)

    queries = []
    dir_list = os.listdir(queriesdir)
    for f in dir_list:
        qid = int(f.split(".")[0].split("query")[1])
        with open(queriesdir + f, 'r') as query:
            queries.append({"id": qid, "query": json.load(query)})

    #run_queries(api, runs, queries, output)
    await run_queries_async(api, runs, queries, output)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
