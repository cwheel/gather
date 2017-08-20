import argparse
import json
from os import path

from pattern import Pattern

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description='Aggregate internet facing data from multiple sources and generate queriable records')

    argParser.add_argument('-p', '--pattern', help='path to the JSON encoded gather pattern', required=True)

    args = argParser.parse_args()

    if not path.isfile(args.pattern):
        print 'Pattern argument must be a JSON encoded pattern file'
        exit()

    with open(args.pattern, 'r') as f:
        try:
            jsonPattern = json.load(f)
        except:
            print 'Failed to parse pattern, pattern must be JSON encoded'
            exit()

        fullFileName = path.basename(args.pattern)
        fileName = fullFileName.split('.')[0]

        userPattern = Pattern(jsonPattern, fileName)
        userPattern.run()
