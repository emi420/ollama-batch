'''
    This utility cleans the data, removing any noise introduced
    by the LLM result

    (c) 2024 Emilio Mariscal
'''

import json
import argparse

def processFile(filename, labels):
    with open(filename) as f:
        json_string = f.read()
        json_object = json.loads(json_string)
        for item in json_object:
            for label in labels:
                for key, value in label.items():
                    if item['result'].lower().find(key) > -1:
                        item['result'] = value
        return json.dumps(json_object)

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--file", "-f", help="File to process", type=str, default=None)
    args.add_argument("--config", "-c", help="Config file", type=str, default="neat.config.json")
    args = args.parse_args()

    config = {}
    with open(args.config) as f:
        json_string = f.read()
        config = json.loads(json_string)

    if args.file and 'labels' in config:
        print(processFile(args.file, config['labels']))
        return
   
    print("Usage: python neat.py -f your_file.json") 

if __name__ == "__main__":
    main()
