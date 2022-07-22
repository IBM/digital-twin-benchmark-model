import argparse
import asyncio
import random
import sys
import time
import os
import json
from MAS_Data_Dictionary.KITT import KITT
from dateutil import parser

api = None

# %% [markdown]
# #### Query Generators

# %%
def generate_q1(size: int, product_types: list, product_features: list, execute: bool = False):
    queries = []
    for i in range(size):
        prt = product_types[random.randint(0, len(product_types) - 1)]
        pf1 = product_features[random.randint(0, len(product_features) - 1)]
        pf2 = product_features[random.randint(0, len(product_features) - 1)]
        value = random.randint(1, 500)
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric1", value)\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf1).v("f1")\
            .go("p")\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf2).v("f2")\
            .rtrn().id("p").name("p").build()
        queries.append(q.list(limit=10, page=0)) if execute else queries.append(q)
    return queries

# %%
def generate_q2(size: int, products:list, execute: bool = False):
    queries = []
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        q = api.reasoner().search()\
            .I("bsbm:Product").id(pr).v("p")\
                .OUT("bsbm:producer").I("bsbm:Producer").v("pd")\
            .go("p")\
                .OUT("bsbm:productFeature").I("bsbm:ProductFeature").v("f")\
            .rtrn().p("p").id("pd").id("f").build()
        queries.append(q.list()) if execute else queries.append(q)
    return queries

# %%
def generate_q3(size: int, product_types: list, product_features: list, execute: bool = False):
    queries = []
    for i in range(size):
        prt = product_types[random.randint(0, len(product_types) - 1)]
        pf1 = product_features[random.randint(0, len(product_features) - 1)]
        pf2 = product_features[random.randint(0, len(product_features) - 1)]
        p1 = random.randint(1, 500)
        p3 = random.randint(1, 500)
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric1", p1).filter_lower("p/bsbm_productPropertyNumeric3", p3)\
                .OUT("bsbm:productFeature").multi(0, 1)\
                    .I("bsbm:ProductFeature").id(pf1).v("f")\
            .go("p")\
                .OUT("bsbm:productFeature").multi(0, 1)\
                    .I("bsbm:ProductFeature").v("f2").filter_not_equal("id", pf1).filter_not_equal("id", pf2)\
            .rtrn().id("p").build()
        queries.append(q.list(limit=10, page=0)) if execute else queries.append(q)
    return queries

# %%
async def generate_q4_async(size: int, product_types: list, product_features: list):
    queries = []
    for i in range(size):
        prt = product_types[random.randint(0, len(product_types) - 1)]
        pf1 = product_features[random.randint(0, len(product_features) - 1)]
        pf2 = product_features[random.randint(0, len(product_features) - 1)]
        p1 = random.randint(1, 500)
        p2 = random.randint(1, 500)
        sub_q = []
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric1", p1)\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf1).v("f1")\
            .go("p")\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf2).v("f2")\
            .rtrn().id("p").p("p", "bsbm_productPropertyTextual1").build()
        sub_q.append(q)
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric2", p2)\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf1).v("f1")\
            .go("p")\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf2).v("f2")\
            .rtrn().id("p").p("p", "bsbm_productPropertyTextual1").build()
        sub_q.append(q)
        queries.append(asyncio.gather(*[sub_q[i].async_list(limit=10, page=0) for i in range(len(sub_q))]))
    for q in queries:
        await q

# %%
def generate_q4(size: int, product_types: list, product_features: list):
    queries = []
    for i in range(size):
        prt = product_types[random.randint(0, len(product_types) - 1)]
        pf1 = product_features[random.randint(0, len(product_features) - 1)]
        pf2 = product_features[random.randint(0, len(product_features) - 1)]
        p1 = random.randint(1, 500)
        p2 = random.randint(1, 500)
        sub_q = []
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric1", p1)\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf1).v("f1")\
            .go("p")\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf2).v("f2")\
            .rtrn().id("p").p("p", "bsbm_productPropertyTextual1").build()
        sub_q.append(q)
        q = api.reasoner().search()\
            .I(prt).v("p").filter_greater("p/bsbm_productPropertyNumeric2", p2)\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf1).v("f1")\
            .go("p")\
                .OUT("bsbm:productFeature")\
                    .I("bsbm:ProductFeature").id(pf2).v("f2")\
            .rtrn().id("p").p("p", "bsbm_productPropertyTextual1").build()
        sub_q.append(q)
        queries.append(sub_q)
    return queries

# %%
def generate_q5(size: int, products:list, execute: bool = False):
    queries = []
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        pd = api.query().instance().id(pr).rtrn()\
            .p("bsbm_productPropertyNumeric1").p("bsbm_productPropertyNumeric2").build().get()
        pd = pd["p"]
        q = api.query().instance().a("bsbm:Product")\
            .filter_lower("p/bsbm_productPropertyNumeric1", pd['bsbm_productPropertyNumeric1'] + 120)\
            .filter_greater("p/bsbm_productPropertyNumeric1", pd['bsbm_productPropertyNumeric1'] - 120)\
            .filter_lower("p/bsbm_productPropertyNumeric2", pd['bsbm_productPropertyNumeric2'] + 120)\
            .filter_greater("p/bsbm_productPropertyNumeric2", pd['bsbm_productPropertyNumeric2'] - 170)\
            .rtrn().name().build()
        queries.append(q.list(limit=5, page=0)) if execute else queries.append(q)
    return queries

# %%
def get_random_str(main_str, substr_len):
    idx = random.randrange(0, len(main_str) - substr_len + 1)    # Randomly select an "idx" such that "idx + substr_len <= len(main_str)".
    return main_str[idx : (idx+substr_len)]

def generate_q6(size: int, products:list, execute: bool = False):
    queries = []
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        pd = api.query().instance().id(pr).rtrn().name().build().get()
        name = pd["p"]["name"] if "p" in pd and "name" in pd["p"]["name"] else None
        if not name or len(name) <= 4:
            i -= 1
            continue
        name = get_random_str(name, 5)
        q = api.query().instance().a("bsbm:Product").filter_match("id", f".*{name}*.").rtrn().name().build()
        queries.append(q.list(limit=10, page=0)) if execute else queries.append(q)
    return queries

# %%
def generate_q7(size: int, products:list, lang: str = 'DE', execute: bool = False):
    queries = []
    dt = int(parser.parse('2008-06-20T00:00:00').timestamp())
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        q = api.reasoner().search()\
            .I("bsbm:Product").id(pr).v("p")\
                .IN("bsbm:product")\
                    .I("bsbm:Offer").v("o").filter_greater("p/bsbm_validTo", dt)\
                        .OUT("bsbm:vendor")\
                            .I("bsbm:Vendor").v("v").filter_equal("p/bsbm_country", f"ns1:{lang}")\
            .go("p")\
                .IN("bsbm:reviewFor")\
                    .I('bsbm:Review').v("rv")\
            .rtrn().p("o").p("v").p("rv").build()
        queries.append(q.list()) if execute else queries.append(q)
    return queries

# %%
def generate_q8(size: int, products:list, lang: str = 'en', execute: bool = False):
    queries = []
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        q = api.reasoner().search()\
            .I("bsbm:Product").id(pr).v("pr")\
                .IN("bsbm:reviewFor")\
                    .I('bsbm:Review').v("r").filter_match('p/rev_text', f".*@lang:{lang}*.")\
                        .OUT("rev:reviewer")\
                            .I("foaf:Person").v("rvr")\
            .rtrn().p("r").p("rvr").build()
        queries.append(q.list(limit=20, page=0)) if execute else queries.append(q)
    return queries

# %%
def generate_q9(size: int, reviews: list, execute: bool = False):
    queries = []
    for i in range(size):
        review = reviews[random.randint(0, len(reviews) - 1)]
        q = api.reasoner().search()\
            .I("bsbm:Review").id(review)\
                .OUT("rev:reviewer")\
                    .I("foaf:Person").v("r")\
            .rtrn().p("r").build()
        queries.append(q.get()) if execute else queries.append(q)
    return queries

# %%
def generate_q10(size: int, products:list, execute: bool = False):
    queries = []
    dt = int(parser.parse('2008-06-20T00:00:00').timestamp())
    for i in range(size):
        pr = products[random.randint(0, len(products) - 1)]
        q = api.reasoner().search()\
            .I("bsbm:Product").id(pr).v("p")\
                .IN('bsbm:product')\
                    .I('bsbm:Offer').v("o").filter_lower_equal('p/bsbm_deliveryDays', '3').filter_greater('p/bsbm_validTo', dt)\
                        .OUT('bsbm:vendor')\
                            .I('bsbm:Vendor').v("v").filter_equal('p/bsbm_country', 'ns1:US')\
            .rtrn().id('v').name('v').p('o', 'bsbm_price').build()
        queries.append(q.list(limit=10, page=0)) if execute else queries.append(q)
    return queries

# %%
def generate_q11(size: int, offers: list, execute: bool = False):
    queries = []
    for i in range(size):
        offer = offers[random.randint(0, len(offers) - 1)]
        q = api.query().instance().id(offer).rtrn().p().build()
        queries.append(q.get()) if execute else queries.append(q)
    return queries

# %%
def generate_q12(size: int, offers: list, execute: bool = False):
    queries = []
    for i in range(size):
        offer = offers[random.randint(0, len(offers) - 1)]
        q = api.reasoner().search()\
            .I('bsbm:Offer').id(offer).v("o")\
                .OUT('bsbm:product').I("bsbm:Product").v("p")\
            .go("o")\
                .OUT('bsbm:vendor').I('bsbm:Vendor').v("v")\
            .rtrn()\
            .id('p').as_("bsbm-export/productlabel")\
            .name('v').as_("bsbm-export/vendorname")\
            .p('o', 'bsbm_deliveryDays').as_("bsbm-export/deliveryDays")\
            .p('o', 'bsbm_price').as_("bsbm-export/price")\
            .p('o', 'bsbm_validTo').as_("bsbm-export/validuntil")\
            .p('o', 'bsbm_offerWebpage').as_("bsbm-export/offerURL")\
            .p('v', 'foaf_homepage').as_("bsbm-export/vendorhomepage")\
            .build()
        queries.append(q.list()) if execute else queries.append(q)
    return queries

# %%
async def gather_with_concurrency_limit(n: int = 0, queries: list = [], single=False, limit=None, page=None):
    if n > 0:
        semaphore = asyncio.Semaphore(n)
 
    async def sem_task(query, single=False, limit=None, page=None):
        start = time.time()
        if semaphore:
            async with semaphore:
                if single:
                    res = await query.async_get()
                elif isinstance(query, list):
                    res = await asyncio.gather(*[query[i].async_list(10, 0) for i in range(len(query))])
                else:
                    res = await query.async_list(limit=limit, page=page)
        else:
            if single:
                res = await query.async_get()
            else:
                res = await query.async_list(limit=limit, page=page)
        total_time = time.time() - start
        return {'time':total_time, 'ressize':len(res)}

    return await asyncio.gather(*(sem_task(query, single, limit, page) for query in queries))

async def async_fetch(id, q, parallelism):
    start = time.time()
    c = await gather_with_concurrency_limit(parallelism, q, limit=10, page=0)
    total_time = time.time() - start
    rt_time = round(total_time, 4)
    avg_time = round((total_time / len(c)), 4)
    qps=1/avg_time
    print(f"Q{id} total time: {rt_time}\nQ{id} avg time: {avg_time}\nQ{id} results ({c} results)")
    times=[cc['time'] for cc in c]
    ressize=[cc['ressize'] for cc in c]
    return {
        'query':id, 
        'executecount':len(q), 
        'qps':qps, 
        'time_total':rt_time, 
        'time_min':min(times), 
        'time_avg':sum(times)/len(times), 
        'time_avg2':avg_time, 
        'time_max':max(times),
        "minresults":min(ressize), 
        "avgresults":sum(ressize)/len(ressize), 
        "maxresults":max(ressize), 
        'results':c, 
    }

async def run_queries(api, graph_id:str, query_size: int, parallelism: int):
    product_types = api.query().concept().filter_match('id', '.*ProductType\d.').build().list_ids()
    product_features = api.query().instance().a('bsbm:ProductFeature').build().list_ids()
    products = api.query().instance().a("bsbm:Product").rtrn().id().build().list_ids()
    reviews = api.query().instance().a("bsbm:Review").rtrn().id().build().list_ids()
    offers = api.query().instance().a("bsbm:Offer").rtrn().id().build().list_ids()
    print(f"Product types loaded: {len(product_types)}")
    print(f"Products loaded: {len(products)}")
    print(f"Product features loaded: {len(product_features)}")
    print(f"Reviews loaded: {len(reviews)}")
    print(f"Offers loaded: {len(offers)}")

    q1 = generate_q1(size=query_size, product_types=product_types, product_features=product_features, execute=False)
    q2 = generate_q2(size=query_size, products=products, execute=False)
    q3 = generate_q3(size=query_size, product_types=product_types, product_features=product_features, execute=False)
    q4 = generate_q4(size=query_size, product_types=product_types, product_features=product_features)
    q5 = generate_q5(size=query_size, products=products, execute=False)
    q6 = generate_q6(size=query_size, products=products, execute=False)
    q7 = generate_q7(size=query_size, products=products, lang="DE", execute=False)
    q8 = generate_q8(size=query_size, products=products, lang="en", execute=False)
    q9 = generate_q9(size=query_size, reviews=reviews, execute=False)
    q10 = generate_q10(size=query_size, products=products, execute=False)
    q11 = generate_q11(size=query_size, offers=offers, execute=False)
    q12 = generate_q12(size=query_size, offers=offers, execute=False)

    print(f"Run {query_size} queries per query type")
    res=[]
    res.append(await async_fetch(1, q1, parallelism))
    res.append(await async_fetch(2, q2, parallelism))
    res.append(await async_fetch(3, q3, parallelism))
    res.append(await async_fetch(4, q4, parallelism))
    res.append(await async_fetch(5, q5, parallelism))
    res.append(await async_fetch(6, q6, parallelism))
    res.append(await async_fetch(7, q7, parallelism))
    res.append(await async_fetch(8, q8, parallelism))
    res.append(await async_fetch(9, q9, parallelism))
    res.append(await async_fetch(10, q10, parallelism))
    res.append(await async_fetch(11, q11, parallelism))
    res.append(await async_fetch(12, q12, parallelism))
    with open(f"stats.{graph_id}.json", 'wt') as fo:
        json.dump(res, fo)

def main(argv):
    global api
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tenant')
    parser.add_argument('-g', '--graphid', default="MAS_Core")
    parser.add_argument('-ps', '--paginationsize', default=20000)
    parser.add_argument('-qs', '--querysize', default=500)
    parser.add_argument('-pl', '--parallelism', default=0)
    args = parser.parse_args()
    tenant_id = args.tenant
    graph_id = args.graphid
    pagination_size = int(args.paginationsize)
    query_size = int(args.querysize)
    parallelism = int(args.parallelism)

    if 'KITT_URL' in os.environ and 'KITT_USR' in os.environ and "KITT_PWD" in os.environ:
        api = KITT(os.environ['KITT_URL'])
        api.login_usr(os.environ['KITT_USR'], os.environ['KITT_PWD'])
        if api and api.connected():
            print(f"Connection to Data Dictionary tenant: {tenant_id} has been established.")
        else:
            print("Connection to Data Dictionary failed")
            sys.exit(1)
        api.space_set(tenant_id)
        api.graph_set(graph_id)
        if api.space_get() is None:
            if api.space_add(space_id=tenant_id):
                print(f"Tenant: {tenant_id} has been created.")
            else:
                print(f"Something went wrong with the creation of the tenant")
                sys.exit(1)
        else:
            print(f"Connected to tenant: {tenant_id}")
        if api.graph_get() is None:
            if api.graph_add(graph_id=graph_id):
                print(f"Graph: {graph_id} has been created.")
            else:
                print(f"Something went wrong with the creation of the graph")
                sys.exit(1)
        else:
            print(f"Connected to graph: {graph_id}")
        api.upload_pagination_set(pagination_size)
        asyncio.run(run_queries(api, graph_id, query_size, parallelism))
    else:
        print("Required env [KITT_URL, KITT_USR, KITT_PWD] missing")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
