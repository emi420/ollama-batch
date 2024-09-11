import ollama
import argparse
import os
import json
import sys

# Process files inside a directory
def processDirectory(question, model, directory):
  files = sorted(os.listdir(directory))
  firstLine = True
  for filename in files:
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file:
      if not firstLine:
        sys.stdout.write(",\n")
      else:
        firstLine = False 
      jsonObject = answerQuestion(file.read(), question, model=model)
      sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
      sys.stdout.flush()

# Process a JSON file
def processJSONFile(question, model, path, property, json_append):
    with open(path, 'r', encoding='utf-8') as file:
      jsonObject = json.loads(file.read())
      firstLine = True
      for item in jsonObject:
        if not firstLine:
          sys.stdout.write(",\n")
        else:
          firstLine = False 
        jsonObject = answerQuestion(item[property], question, model=model)
        if json_append:
           for prop in json_append:
              jsonObject[prop] = item[prop]
        sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
        sys.stdout.flush()

# Answer question about content
def answerQuestion(content, question, questionFirst = False, model = "llama3"):
  if type(content) == list:
     content = " ".join(content)
  response = ollama.chat(model=model, messages=[
    {
      'role': 'user',
      'content':  (content + " \n " + question) if not questionFirst else (question + " \n " + content)
    },
  ])
  return {
     'result': response['message']['content'].replace("\n",' ')
  }

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--directory", "-d", help="Directory", type=str, default=None)
    args.add_argument("--file", "-f", help="File", type=str, default=None)
    args.add_argument("--model", "-m", help="Model", type=str, default="llama3")
    args.add_argument("--prompt", "-p", help="Prompt", type=str, default=None)
    args.add_argument("--prompt-file", help="Prompt file", type=str, default=None)
    args.add_argument("--json-property", help="JSON property", type=str, default="content")
    args.add_argument("--json-append", help="Data from original source to append", type=str, default=None)
    args = args.parse_args()

    prompt = None

    if args.prompt:
      prompt = args.prompt
    elif args.prompt_file:
      with open(args.prompt_file) as f:
        prompt = f.read()
    
    if prompt:
      print("[")
      if args.directory:
          processDirectory(prompt, args.model, args.directory)
          print("\n]\n")
          return
      elif args.file:
          if (args.file[-4:] == "json"):
            processJSONFile(prompt, args.model, args.file, args.json_property, args.json_append.split(",") if args.json_append else None)
            print("\n]\n")
            return

    print("Ollama Batch Text Processor")
    print("")
    print("This script can run text prompts over a list texts and print the results as JSON.")
    print("")
    print("python ollama-batch.py -h prints help")
    print("")
    print("Usage: python ollama-batch.py -d <directory> -p <prompt>")
    print("       python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' > recipes_result.json")
    print("")
    print("       python ollama-batch.py -f <json file> --prompt-file <prompt file>")
    print("       python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt")
    print("       python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-property=ingredients")
    print("       python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url")

if __name__ == "__main__":
    main()