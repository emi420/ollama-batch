'''
    This simple script run text LLM prompts over a list of texts
    and print the results as JSON. 

    (c) 2024 Emilio Mariscal
'''

import ollama
import argparse
import os
import json
import sys

# Process files inside a directory
def processDirectory(question, model, directory, questionFirst, system):
  files = sorted(os.listdir(directory))
  firstLine = True
  for filename in files:
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file:
      if not firstLine:
        sys.stdout.write(",\n")
      else:
        firstLine = False 
      jsonObject = answerQuestion(file.read(), question, model=model, questionFirst=questionFirst, system=system)
      sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
      sys.stdout.flush()

# Process a JSON file
def processJSONFile(question, model, path, property, json_append, questionFirst, system):
    with open(path, 'r', encoding='utf-8') as file:
      jsonObject = json.loads(file.read())
      firstLine = True
      for item in jsonObject:
        if not firstLine:
          sys.stdout.write(",\n")
        else:
          firstLine = False 
        jsonObject = answerQuestion(item[property], question, model=model, questionFirst=questionFirst, system=system)
        if json_append:
           for prop in json_append:
              jsonObject[prop] = item[prop]
        sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
        sys.stdout.flush()

# Answer question about content
def answerQuestion(content, question, questionFirst = False, model = "llama3", system = None):
  if type(content) == list:
     content = " ".join(content)
  response = ollama.chat(model=model if not system else "custom", messages=[
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
    args.add_argument("--directory", "-d", help="Directory with files you want to process", type=str, 
                      default=None)
    args.add_argument("--file", "-f", help="JSON file you want to process", type=str, default=None)
    args.add_argument("--model", "-m", help="Model you want to use", type=str, default="llama3")
    args.add_argument("--prompt", "-p", help="Prompt text", type=str, default=None)
    args.add_argument("--prompt-file", help="Text file with a prompt", type=str, default=None)
    args.add_argument("--json-property", help="JSON property that you want to use", type=str, default="content")
    args.add_argument("--json-append", help="Property that you want to append to the results", type=str, 
                      default=None)
    args.add_argument("--question-first", help="First the question, then the prompt", default=False, 
                      action='store_true')
    args.add_argument("--system", help="System message", type=str, default=None)
    args.add_argument("--message-user", help="An example message of what the user could have asked.", type=str, default=None)
    args.add_argument("--message-assistant", help="An example message of how the model should respond.", type=str, default=None)
    args = args.parse_args()

    prompt = None

    if args.prompt:
      prompt = args.prompt
    elif args.prompt_file:
      with open(args.prompt_file) as f:
        prompt = f.read()
    
    if prompt:

      modelfile = 'FROM {model}'.format(model=args.model)

      if args.system:
        modelfile += '\nSYSTEM {system}'.format(system=args.system)

      if args.message_user:
        modelfile += '\nMESSAGE user {message_user}'.format(message_user=args.message_user)

      if args.message_assistant:
        modelfile += '\nMESSAGE assistant {message_assistant}'.format(
           message_assistant=args.message_assistant)

      ollama.create(model='custom', modelfile=modelfile)

      print("[")
      if args.directory:
          processDirectory(prompt, args.model, args.directory, args.question_first, args.system)
          print("\n]\n")
          return
      elif args.file:
          if (args.file[-4:] == "json"):
            processJSONFile(prompt, args.model, args.file, args.json_property, args.json_append.split(",") 
                            if args.json_append else None, args.question_first, args.system)
            print("\n]\n")
            return

    print("Ollama Batch Text Processor")
    print("")
    print("This script can run text prompts over a list texts and print the results as JSON.")
    print("")
    print("Run 'ollama-batch -h' for help")




if __name__ == "__main__":
    main()