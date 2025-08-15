'''
    This simple script run text LLM prompts over a list of texts
    or images and print the results as JSON. 

    (c) 2024 Emilio Mariscal
'''

import ollama
import argparse
import os
import json
import sys
import base64
from PIL import Image
import io

OPTIONS = {
  "temperature": 0.0,
  "top_p": 0.9,
  "max_new_tokens": 25,
  "stream": False,
}

# Downscale and encode images as base64 strings
def load_image_as_base64(path, max_dim=1024, quality=85):
    img = Image.open(path)
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()

# Process files inside a directory
def processDirectory(question, model, directory, questionFirst, images):
  files = sorted(os.listdir(directory))
  firstLine = True
  for filename in files:
    path = os.path.join(directory, filename)
    if images:
      if filename.endswith(("png", "jpg", "jpeg")):
        jsonObject = answerQuestion(question, model=model, questionFirst=questionFirst, image=path)
        if jsonObject:
          if not firstLine:
            sys.stdout.write(",\n")
          else:
            firstLine = False 
          jsonObject['image'] = path
          sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
          sys.stdout.flush()
        
    else:
      with open(path, 'r', encoding='utf-8') as file:
        if not firstLine:
          sys.stdout.write(",\n")
        else:
          firstLine = False 
        jsonObject = answerQuestion(question, file.read(), model=model, questionFirst=questionFirst)
        jsonObject['path'] = path
        sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
        sys.stdout.flush()

# Process a JSON file
def processJSONFile(question, model, path, property, json_append, questionFirst):
    with open(path, 'r', encoding='utf-8') as file:
      jsonObject = json.loads(file.read())
      firstLine = True
      for item in jsonObject:
        if not firstLine:
          sys.stdout.write(",\n")
        else:
          firstLine = False 
        jsonObject = answerQuestion(question, item[property], model=model, questionFirst=questionFirst)
        if json_append:
           for prop in json_append:
              jsonObject[prop] = item[prop]
        sys.stdout.write(json.dumps(jsonObject, ensure_ascii=False))
        sys.stdout.flush()

# Answer question about content
def answerQuestion(question, content = None, questionFirst = False, model = "gemma3:4b", image = None):
  if type(content) == list:
     content = " ".join(content)
  response = None
  if image:
    try:
      image_b64 = load_image_as_base64(image)
      response = ollama.chat(model=model, 
        messages=[
          {
            'role': 'user',
            'content':  question,
            'images': [image_b64]
          },
        ],
        options=OPTIONS,
      )
    except Exception as e:
      pass
  else:
    response = ollama.chat(model=model,
      messages=[
        {
          'role': 'user',
          'content':  (content + " \n " + question) if not questionFirst else (question + " \n " + content)
        },
      ],
      options=OPTIONS,
    )
  if response:
    return {
      'result': response['message']['content'].replace("\n",' ').lower()
    }

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--directory", "-d", help="Directory with files you want to process", type=str, 
                      default=None)
    args.add_argument("--file", "-f", help="JSON file you want to process", type=str, default=None)
    args.add_argument("--model", "-m", help="Model you want to use", type=str, default="gemma3:4b")
    args.add_argument("--prompt", "-p", help="Prompt text", type=str, default=None)
    args.add_argument("--prompt-file", help="Text file with a prompt", type=str, default=None)
    args.add_argument("--json-property", help="JSON property that you want to use", type=str, default="content")
    args.add_argument("--json-append", help="Property that you want to append to the results", type=str, 
                      default=None)
    args.add_argument("--question-first", help="First the question, then the prompt", default=False, 
                      action='store_true')
    args.add_argument("--images", "-i", help="Look for image files", default=False, 
                      action='store_true')
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
          processDirectory(prompt, args.model, args.directory, args.question_first, args.images)
          print("\n]\n")
          return
      elif args.file:
          if (args.file[-4:] == "json"):
            processJSONFile(prompt, args.model, args.file, args.json_property, args.json_append.split(",") 
                            if args.json_append else None, args.question_first)
            print("\n]\n")
            return

    print("Ollama Batch Text Processor")
    print("")
    print("This script can run text prompts over a list texts or images and print the results as JSON.")
    print("")
    print("ollama-batch -h prints help")
    print("")
    print("Usage: ollama-batch -d <directory> -p <prompt>")
    print("       ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' > \
          recipes_result.json")
    print("")
    print("       ollama-batch -f <json file> --prompt-file <prompt file>")
    print("       ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt")
    print("       ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt \
          --json-property=ingredients")
    print("       ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt \
          --json-append=title,url")
    print("       ollama-batch -m llava:13b -d examples/images -i -p 'Describe this image'")

if __name__ == "__main__":
    main()