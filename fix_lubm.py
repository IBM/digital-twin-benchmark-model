import argparse
import os
import sys

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    input = args.input
    file = open(input, "r")
    c = 0
    skip = False
    with open(f"tmp.ttl", "w") as w:
        for line in file:
            c += 1
            if skip:
                skip = False
                continue
            line = line.strip()
            if c > 4 and (line.startswith("@prefix") or line.startswith("<> a owl:Ontology") or line.startswith("owl:imports")):
                if c < 10 and line.startswith("owl:imports"):
                    skip = True
                continue
            w.write(line + "\n")
        w.write(".")
    file.close()
    os.rename("tmp.ttl", input)
    

if __name__ == "__main__":
    main(sys.argv[1:])