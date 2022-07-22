import random as rand
import io
import argparse
import json
from re import L
import uuid

series_factory={
    "weather_temp":"f:Data_Weather_Temperature"
}
robot_manufacturer=["ACME", "Wayne", "Humanitech"]
linelvl=[[1],[1,1],[1,1,1],[1,1,2],[1,1,3],[1,2],[1,2,1],[1,2,2],[1,2,3],[1,3],[1,3,1],[1,3,2],[1,3,3],[2],[2,1],[2,1,1],[2,1,2],[2,1,3],[2,2],[2,2,1],[2,2,2],[2,2,3],[2,3],[2,3,1],[2,3,2],[2,3,3]]
linedepth=[1,2,3]
workorders=[1,2,3]
series_robot={
    "energy":"f:Data_Power",
    "voltage":"f:Data_Voltage",
    "current":"f:Data_Current",
    "state":"f:Data_State",
    "onoff":"f:Data_OnOff",
}
joints=range(2,4)
series_joint={
    "temperature":"f:Data_Robot_Temperature",
    "angle_alpha":"f:Data_Angle_Alpha",
    "angle_beta":"f:Data_Angle_Beta",
    "angle_gamma":"f:Data_Angle_Gamma",
}
series_arm={
    "position_x":"f:Data_Position_X",
    "position_y":"f:Data_Position_Y",
    "position_z":"f:Data_Position_Z",
}
series_belt={
    "energy":"f:Data_Power",
    "voltage":"f:Data_Voltage",
    "current":"f:Data_Current",
    "state":"f:Data_State",
    "onoff":"f:Data_OnOff",
}
file_robot={
    "handbook":"f:Data_Handbook"
}
json_robot={
    "asset_history":"f:Data_Asset_History"
}

prefix="""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dt: <http://www.ibm.com/digital_twin_factory.owl#> .
@prefix f: <http://www.ibm.com/factory.owl#> .

<http://www.ibm.com/digital_twin_factory.owl>
  a owl:Ontology ;
  rdfs:comment "An digital twin core ontology" ;
  rdfs:label "Digital Twin Benchmark Core Model" .

<http://www.ibm.com/factory.owl>
  a owl:Ontology ;
  rdfs:comment "An digital twin factory benchmark tests" ;
  rdfs:label "Factory Ontology" .

dt:Location
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A location".

dt:Asset
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A physical asset such as a machine".

dt:Data
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An associated dataset" .

dt:Data_Json
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An associated json dataset" ;
  rdfs:subClassOf dt:Data .

dt:Data_File
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An associated file dataset" ;
  rdfs:subClassOf dt:Data .

dt:Data_Series
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An associated time series dataset" ;
  rdfs:subClassOf dt:Data .

f:Workorder
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A maintenance workorder";
  rdfs:subClassOf dt:Data_Json .

dt:Data_Series_Numeric
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A numeric time series" ;
  rdfs:subClassOf dt:Data_Series .

dt:Data_Series_Categoric
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A categorical time series" ;
  rdfs:subClassOf dt:Data_Series .

dt:Data_Series_Logical
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A boolean time series" ;
  rdfs:subClassOf dt:Data_Series .

dt:Data_Series_Temporal
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A temporal time series" ;
  rdfs:subClassOf dt:Data_Series .

f:Country
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A country location" ;
  rdfs:subClassOf dt:Location .

f:City
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A city location" ;
  rdfs:subClassOf dt:Location .

f:Factory
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A factory location" ;
  rdfs:subClassOf dt:Location .

f:Line
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A production line in a factory" ;
  rdfs:subClassOf dt:Location .

f:Machine
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A machine" ;
  rdfs:subClassOf dt:Asset .

f:Robot
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A robotic arm" ;
  rdfs:subClassOf f:Machine .

f:Robot_ACME
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A robotic arm" ;
  rdfs:subClassOf f:Robot .

f:Robot_Wayne
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A robotic arm" ;
  rdfs:subClassOf f:Robot .

f:Robot_Humanitech
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A robotic arm" ;
  rdfs:subClassOf f:Robot .

f:Belt
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A conveyor belt" ;
  rdfs:subClassOf dt:Asset .

f:Robot_Joint
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The joint of a robot" ;
  rdfs:subClassOf dt:Asset .

f:Robot_Arm
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The arm of a robot" ;
  rdfs:subClassOf dt:Asset .

f:Robot_Tool
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The tool of a robot" ;
  rdfs:subClassOf dt:Asset .

f:Data_Temperature
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A temperature measurement" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Weather_Temperature
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A outside temperature measurement" ;
  rdfs:subClassOf f:Data_Temperature .

f:Data_Robot_Temperature
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "A inside temperature measurement" ;
  rdfs:subClassOf f:Data_Temperature .

f:Data_Angle
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of an angle" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Angle_Alpha
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of alpha angle" ;
  rdfs:subClassOf f:Data_Angle .

f:Data_Angle_Beta
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of beta angle" ;
  rdfs:subClassOf f:Data_Angle .

f:Data_Angle_Gamma
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of gamma angle" ;
  rdfs:subClassOf f:Data_Angle .

f:Data_Position
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of an position" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Position_X
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of x coordinates" ;
  rdfs:subClassOf f:Data_Position .

f:Data_Position_Y
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of y coordinates" ;
  rdfs:subClassOf f:Data_Position .

f:Data_Position_Z
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of z coordinates" ;
  rdfs:subClassOf f:Data_Position .

f:Data_State_Agg
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The aggregated state" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Power_Agg
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The aggregated power consumption" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Power_Pred
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The predicted power consumption" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Power
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of power consumption" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Voltage
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of voltage" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_Current
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The measurement of a current" ;
  rdfs:subClassOf dt:Data_Series_Numeric .

f:Data_State
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The categoric state of a machine" ;
  rdfs:subClassOf dt:Data_Series_Categoric .

f:Data_OnOff
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The on/off state of a machine" ;
  rdfs:subClassOf dt:Data_Series_Logical .

f:Data_Handbook
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The on/off state of a machine" ;
  rdfs:subClassOf dt:Data_File .

f:Data_Asset_History
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "The asset history machine" ;
  rdfs:subClassOf dt:Data_Json .

dt:Function
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An AI Function" .

f:Function_Agg
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An AI Function that summs input" ;
  rdfs:subClassOf dt:Function .

f:Function_Pred
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An AI Function that predicts the target input" ;
  rdfs:subClassOf dt:Function .

f:Function_Sum
  a rdfs:Class ;
  a owl:Class ;
  rdfs:label "An AI Function that summs input" ;
  rdfs:subClassOf dt:Data_Json .

dt:hasPart
  a owl:ObjectProperty .

dt:hasSubAsset
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasPart .

dt:hasSubLocation
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasPart .

f:hasLine
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasSubLocation .

f:hasJoint
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasSubAsset .

f:hasArm
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasSubAsset .

f:hasBelt
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasSubAsset .

f:hasRobot
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasSubAsset .

dt:hasData
  a owl:ObjectProperty .

f:hasWorkorder
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasData .

dt:hasSeries
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasData .

dt:hasFile
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasData .

dt:hasJson
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:hasData .

dt:connects
  a owl:ObjectProperty .

dt:hasInput
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:connects .

dt:hasOutput
  a owl:ObjectProperty;
  rdfs:subPropertyOf dt:connects .

dt:hasInputData
  a owl:ObjectProperty .

dt:hasInputDataTarget
  a owl:ObjectProperty ;
  rdfs:subPropertyOf dt:hasInputData .

dt:hasOutputData
  a owl:ObjectProperty .

dt:hasDataKey
  a owl:DatatypeProperty ;
  rdfs:label "A key literal pointing to raw data stored in a storage backend" .

dt:hasDataKeySeries
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a single time series stored in a storage backend" ;
  rdfs:subPropertyOf dt:hasDataKey .

dt:hasDataKeyFile
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a single file stored in a storage backend" ;
  rdfs:subPropertyOf dt:hasDataKey .

dt:hasDataKeyJson
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a single json document stored in a storage backend" ;
  rdfs:subPropertyOf dt:hasDataKey .

f:hasDataKeySeriesIOT1
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a single time series stored in IOT platform 1" ;
  rdfs:subPropertyOf dt:hasDataKeySeries .

f:hasDataKeySeriesWeater1
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a single time series stored in weather platform" ;
  rdfs:subPropertyOf dt:hasDataKeySeries .

f:hasDataKeyJsonAssetMgmt2
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to JSON API in an asset management system 2" ;
  rdfs:subPropertyOf dt:hasDataKeyJson .

f:hasDataKeyFileDocumentMgmt3
  a owl:DatatypeProperty ;
  rdfs:label "A  key literal pointing to a file in a document management system 3" ;
  rdfs:subPropertyOf dt:hasDataKeyFile .

"""

model="""---
concepts:
- id: dt:Node
  name: Either a location or asset
- id: dt:Location
  c: [ dt:Node ]
  name: A location
- id: dt:Asset
  c: [ dt:Node ]
  name: A physical asset such as a machine
- id: dt:Data
  name: An associated dataset
- id: dt:Function
  name: An AI function
- id: f:Function_Agg
  c: [ dt:Function ]
  name: An AI function that summs input
- id: f:Function_Pred
  c: [ dt:Function ]
  name: An AI function that summs input
- id: dt:Data_Json
  c: [ dt:Data ]  
  name: An associated json dataset
- id: dt:Data_File
  c: [ dt:Data ]  
  name: An associated file dataset
- id: dt:Data_Series
  c: [ dt:Data ]  
  name: An associated time series dataset
- id: dt:Data_Series_Numeric
  c: [ dt:Data_Series ]  
  name: A numeric time series
- id: dt:Data_Series_Categoric
  c: [ dt:Data_Series ]  
  name: A categorical time series
- id: dt:Data_Series_Logical
  c: [ dt:Data_Series ]  
  name: A boolean time series
- id: f:Workorder
  c: [ dt:Data_Json ]
  name: A maintenance workorder
- id: f:Country
  c: [ dt:Location ]  
  name: A country location
- id: f:City
  c: [ dt:Location ]  
  name: A City location
- id: f:Factory
  c: [ dt:Location ]  
  name: A factory location
- id: f:Line
  c: [ dt:Location ]  
  name: A production line in a factory
- id: f:Machine
  c: [ dt:Asset ]  
  name: A machine
- id: f:Robot
  c: [ f:Machine ]  
  name: A robotic arm
- id: f:Robot_Wayne
  c: [ f:Robot ]  
  name: A robotic arm
- id: f:Robot_ACME
  c: [ f:Robot ]  
  name: A robotic arm
- id: f:Robot_Humanitech
  c: [ f:Robot ]  
  name: A robotic arm
- id: f:Belt
  c: [ dt:Asset ]  
  name: A conveyor belt
- id: f:Robot_Joint
  c: [ dt:Asset ]  
  name: The joint combining two robotic arms
- id: f:Robot_Arm
  c: [ dt:Asset ]  
  name: The arm of a robot
- id: f:Robot_Tool
  c: [ dt:Asset ]  
  name: The tool of a robot
- id: f:Data_Temperature
  c: [ dt:Data_Series_Numeric ]  
  name: A temperature measurement
- id: f:Data_Robot_Temperature
  c: [ f:Data_Temperature ]  
  name: A robot temperature measurement
- id: f:Data_Weather_Temperature
  c: [ f:Data_Temperature ]  
  name: A outside temperature measurement
- id: f:Data_Power
  c: [ dt:Data_Series_Numeric ]  
  name: The measurement of power consumption
- id: f:Data_State_Agg
  c: [ dt:Data_Series_Numeric ]  
  name: The aggregated state
- id: f:Data_Power_Agg
  c: [ dt:Data_Series_Numeric ]  
  name: The aggregated power consumption
- id: f:Data_Power_Pred
  c: [ dt:Data_Series_Numeric ]  
  name: The predicted power consumption
- id: f:Data_Angle
  c: [ dt:Data_Series_Numeric ]  
  name: The measurement of an angle
- id: f:Data_Angle_Alpha
  c: [ f:Data_Angle ]  
  name: The measurement of an alpha angle
- id: f:Data_Angle_Beta
  c: [ f:Data_Angle ]  
  name: The measurement of an beta angle
- id: f:Data_Angle_Gamma
  c: [ f:Data_Angle ]  
  name: The measurement of an gamma angle
- id: f:Data_Position
  c: [ dt:Data_Series_Numeric ]  
  name: The measurement of an position
- id: f:Data_Position_X
  c: [ f:Data_Position ]  
  name: The measurement of an x position
- id: f:Data_Position_Y
  c: [ f:Data_Position ]  
  name: The measurement of an y position
- id: f:Data_Position_Z
  c: [ f:Data_Position ]  
  name: The measurement of an z position
- id: f:Data_Voltage
  c: [ dt:Data_Series_Numeric ]  
  name: The measurement of voltage
- id: f:Data_Current
  c: [ dt:Data_Series_Numeric ]  
  name: The measurement of current
- id: f:Data_State
  c: [ dt:Data_Series_Categoric ]  
  name: The categoric state of a machine
- id: f:Data_OnOff
  c: [ dt:Data_Series_Logical ]  
  name: The on/off state of a machine
- id: f:Data_Handbook
  c: [ dt:Data_File ]  
  name: A handbook
- id: f:Data_Asset_History
  c: [ dt:Data_File ]  
  name: The asset history machine
ireftypes:
- id: dt:hasPart
- id: dt:hasSubAsset
  c: dt:hasPart
- id: f:hasJoint
  c: dt:hasSubAsset
- id: f:hasArm
  c: dt:hasSubAsset
- id: f:hasBelt
  c: dt:hasSubAsset
- id: f:hasRobot
  c: dt:hasSubAsset
- id: dt:hasSubLocation
  c: dt:hasPart
- id: f:hasLine
  c: dt:hasSubLocation
- id: dt:hasData
- id: f:hasWorkorder
  c: dt:hasData
- id: dt:connects
- id: dt:hasInput
  c: dt:connects
- id: dt:hasOutput
  c: dt:connects
- id: dt:hasSeries
  c: dt:hasData
- id: dt:hasFile
  c: dt:hasData
- id: dt:hasJson
  c: dt:hasData
- id: dt:hasInputData
- id: dt:hasInputDataTarget
  c: dt:hasInputData
- id: dt:hasOutputData
"""
dataprops={}

def add_ins(fout, kout, id, type, props=None):
    fout.write(f"{id} a {type} .\n")
    if props:
      for k,v in props.items():
        if k not in dataprops:
          fout.write(f"f:{k} rdfs:subPropertyOf owl:DatatypeProperty .\n")
          dataprops[k]=True
        fout.write(f"{id} f:{k} \"{v}\" .\n")
    kout.write(f"- id: {id}\n  a: {type}\n")
    if props:
      kout.write(f"  p: {json.dumps(props)}\n")

def add_ref(fout, kout, iref, src, type, tgt):
    fout.write(f"{src} {type} {tgt} .\n")
    iref.write(f"- src: {src}\n  a: {type}\n  tgt: {tgt}\n")

def add_part(fout, kout, iref, parent, id, type, hasPart, props=None):
    add_ins(fout, kout, id, type, props)
    add_ref(fout, kout, iref, parent, hasPart, id)

def add_data(fout, kout, iref, rid, series, rtype, keyreftype, random=False):
    select = rand.choices(list(series.keys()),k=rand.randint(0,len(series))) if random else series.keys()
    for sens in select:
        sid=f"{rid}_{sens}"
        key=uuid.uuid4()
        fout.write(f"{sid} a {series[sens]} .\n")
        fout.write(f"{sid} {keyreftype} \"{key}\".\n")
        kout.write(f"- id: {sid}\n  a: {series[sens]}\n  p:\n    key: {key}\n")
        add_ref(fout, kout, iref, rid, rtype, sid)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--factories', default=1)
    parser.add_argument('-r', '--robots', default=20)
    parser.add_argument('-v', '--verify', default="false")
    parser.add_argument('-x', '--random', default="false")
    args = parser.parse_args()
    factories = int(args.factories)
    robots = int(args.robots)
    verify=args.verify.lower() == "true"
    random=args.random.lower() == "true"
    fout=open(f'factory_{factories}.ttl','tw')
    fout.write(prefix)

    kout=open(f'factory_{factories}.kitt','tw')
    kout.write(model)
    kout.write("instances:\n")

    iref=io.StringIO()
    iref.write("ireferences:\n")
    lcnt=0
    rcnt=0
    for fc in range(factories):
        fid=f"f:factory{fc}"
        add_ins(fout, kout, fid, "f:Factory")
        add_data(fout, kout, iref, fid, series_factory, "dt:hasSeries", "f:hasDataKeySeriesWeater1", random=random)
        series_factory
        lineids=set()
        for llvl in linelvl:
            lid=f"{fid}_line"
            parent = fid
            for ldn in llvl:
                lid += "_"+str(ldn)
                lcnt+=1
                if lid not in lineids:
                  add_part(fout, kout, iref, parent, lid, "f:Line", "f:hasLine")
                  lineids.add(lid)
                  parent=lid
                  oldrid=None
                  oldbid=None
                  for rc in range(robots): #rand.choice(robots)
                      manu=rand.choice(robot_manufacturer)
                      rid=f"{lid}_robot_{rc}"
                      rcnt+=1
                      add_part(fout, kout, iref, parent, rid, "f:Robot_"+manu, "f:hasRobot", {'manufacturer':manu, "asset_id":str(uuid.uuid4())})
                      add_data(fout, kout, iref, rid, series_robot, "dt:hasSeries", "f:hasDataKeySeriesIOT1", random=random)
                      add_data(fout, kout, iref, rid, json_robot, "dt:hasJson", "f:hasDataKeyJsonAssetMgmt2", random=random)
                      add_data(fout, kout, iref, rid, file_robot, "dt:hasFile", "f:hasDataKeyFileDocumentMgmt3", random=random)
                      oldjid=None
                      for jc in range(rand.choice(joints)):
                          jid=f"{rid}_joint_{jc}"
                          add_part(fout, kout, iref, rid, jid, "f:Robot_Joint", "f:hasJoint", {"asset_id":str(uuid.uuid4())})
                          add_data(fout, kout, iref, jid, series_joint, "dt:hasSeries", "f:hasDataKeySeriesIOT1", random=random)
                          if oldjid:
                              aid=f"{rid}_arm_{jc}"
                              add_part(fout, kout, iref, rid, aid, "f:Robot_Arm", "f:hasArm", {"asset_id":str(uuid.uuid4())})
                              add_ref(fout, kout, iref, oldjid, "dt:connects", aid)
                              add_ref(fout, kout, iref, aid, "dt:connects", jid)
                              add_data(fout, kout, iref, aid, series_arm, "dt:hasSeries", "f:hasDataKeySeriesIOT1", random=random)
                          oldjid=jid
                      if oldrid:
                          bid=f"{rid}_belt_{jc}"
                          add_part(fout, kout, iref, rid, bid, "f:Belt", "f:hasBelt", {"asset_id":str(uuid.uuid4())})
                          add_ref(fout, kout, iref, oldrid, "dt:hasOutput", bid)
                          add_ref(fout, kout, iref, bid, "dt:hasInput", rid)
                          if oldbid:
                              add_ref(fout, kout, iref, oldbid, "dt:connects", bid)
                          add_data(fout, kout, iref, bid, series_belt, "dt:hasSeries", "f:hasDataKeySeriesIOT1", random=random)
                          oldbid=bid
                      oldrid=rid
                      for wc in range(rand.choice(workorders)):
                        wid=f"{rid}_workorder_{wc}"
                        add_part(fout, kout, iref, rid, wid, "f:Workorder", "f:hasWorkorder", {'open':rand.uniform(0.0,1.0)>0.9})
        fout.write(f"\n")
    fout.flush()
    fout.close()

    iref.flush()
    iref.seek(0)
    kout.write(iref.read())
    kout.flush()
    kout.close()

    fout=open(f'factory_{factories}.ttl','tr')
    tripples = -82
    for line in fout:
      if line != "\n":
        tripples += 1

    print(f"Factories {factories}")
    print(f"Lines {lcnt}")
    print(f"Robots {rcnt}")
    print(f"Triples {tripples}")
    if verify: # verify rdf
        import rdflib
        g = rdflib.Graph()
        g.parse(f'factory_{factories}.ttl', format="turtle")
        print(f"Triples {len(g)}")

if __name__ == "__main__":
    main()
