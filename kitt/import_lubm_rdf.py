import argparse
import os
import sys

import rdflib

from MAS_Data_Dictionary.KITT import KITT
from MAS_Data_Dictionary.io.rdf import RdfImport


# python3 import_rdf -i scale2000.ttl -f turtle -t iswc -g scale2000 -ps 20000
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format', default="turtle")
    parser.add_argument('-t', '--tenant')
    parser.add_argument('-g', '--graphid')
    parser.add_argument('-ps', '--paginationsize', default=20000)
    args = parser.parse_args()
    inputfile = args.input
    outputfile = args.output
    format = args.format
    tenant_id = args.tenant
    graph_id = args.graphid
    pagination_size = int(args.paginationsize)

    if 'KITT_URL' in os.environ and 'KITT_USR' in os.environ and "KITT_PWD" in os.environ:
        api = KITT(os.environ['KITT_URL'])
        api.login_usr(os.environ['KITT_USR'], os.environ['KITT_PWD'])
        if api and api.connected():
            print(f"Connection to Data Dictionary has been established.")
        else:
            print("Connection to Data Dictionary failed")
            sys.exit(1)
    else:
        print("Required env [KITT_URL, KITT_USR, KITT_PWD] missing")
        sys.exit(2)

    if tenant_id and graph_id:
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

    g = rdflib.Graph()
    g.parse(inputfile, format=format)
    print("RDF graph has been parsed.")
    rdf = RdfImport(api)
    print("Construct Data Dictionary model has been started.")
    rdf.import_rdf_graph(g, create_missing=True)
    rdf.g = None
    rdf.model['ireftypes'] = [{"id": "ub:subOrganizationOf"}, {"id": "ub:teacherOf"}, {"id": "ub:degreeFrom"}, {"id": "ub:undergraduateDegreeFrom", "c":"ub:degreeFrom"}, { "id": "ub:mastersDegreeFrom" , "c":"ub:degreeFrom"}, { "id": "ub:doctoralDegreeFrom" , "c":"ub:degreeFrom"}, { "id": "ub:worksFor" }, { "id": "ub:headOf" }, { "id": "ub:memberOf" }, { "id": "ub:takesCourse" }, { "id": "ub:advisor" }, { "id": "ub:teachingAssistantOf" }, { "id": "ub:publicationAuthor" }]
    rdf.model['concepts'] = [ { "id": "owl:Ontology" }, { "id": "ub:Person" }, { "id": "ub:Student", "c": [ "ub:Person" ] }, { "id": "ub:Professor", "c": [ "ub:Person" ] }, { "id": "ub:AssistantProfessor", "c": [ "ub:Professor" ] }, { "id": "ub:AssociateProfessor", "c": [ "ub:Professor" ] }, { "id": "ub:Course" }, { "id": "ub:Department" }, { "id": "ub:FullProfessor", "c": [ "ub:Professor" ] }, { "id": "ub:GraduateCourse", "c": [ "ub:Course" ] }, { "id": "ub:GraduateStudent", "c": [ "ub:Student" ] }, { "id": "ub:Lecturer", "c": [ "ub:Person" ] }, { "id": "ub:Publication" }, { "id": "ub:ResearchAssistant", "c": [ "ub:Person" ] }, { "id": "ub:ResearchGroup" }, { "id": "ub:TeachingAssistant", "c": [ "ub:Person" ] }, { "id": "ub:UndergraduateStudent", "c": [ "ub:Student" ] }, { "id": "ub:University" }, {"id":"owl:Restriction"}, {"id":"owl:DatatypeProperty"}, {"id":"owl:TransitiveProperty"} ]
    print(f"concepts: {len(rdf.model['concepts'])}")
    print(f"creftypes: {len(rdf.model['creftypes'])}")
    print(f"ireftypes: {len(rdf.model['ireftypes'])}")
    print(f"instances: {len(rdf.model['instances'])}")
    print(f"creferences: {len(rdf.model['creferences'])}")
    print(f"ireferences: {len(rdf.model['ireferences'])}")
    print(f"isVerified: {len(rdf.verify(consider_mas_core=True)) == 0}")
    if tenant_id and graph_id:
        print("The push of the DD model into the Data Dictionary has been started.")
        rdf.send()
    if outputfile:
        print("The model extraction to disk has been started")
        rdf.save(outputfile)
        print(f"Saved yaml file {outputfile}")


if __name__ == "__main__":
    main(sys.argv[1:])
