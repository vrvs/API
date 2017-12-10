from untagged import *
import json
import sys

def main(args):
    retriever.init("hotels")
    rank = retriever.retrieveContent(args[0], args[1], args[2:])
    out = json.dumps(rank)
    print(out)

if __name__ == "__main__":
    main(sys.argv[1:])