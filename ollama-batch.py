import ollama
import argparse
import os

# Process file with URL list
def processFile(directory, question):
  files = sorted(os.listdir(directory))
  for filename in files:
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file:
      print("----")
      print(filename)
      answerQuestion(file.read(), question)

# Answer question about content
def answerQuestion(content, question):
  response = ollama.chat(model='llama3', messages=[
    {
      'role': 'user',
      'content':  content + " \n " + question
    },
  ])
  print(response['message']['content'])


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--directory", "-d", help="Directory", type=str, default=None)
    args.add_argument("--file", "-f", help="Prompt file", type=str, default=None)
    args.add_argument("--prompt", "-p", help="Prompt", type=str, default=None)
    args = args.parse_args()

    if args.directory and args.prompt:
        processFile(args.directory, args.prompt)
        return
    elif args.directory and args.file:
        with open(args.file) as f:
          processFile(args.directory, f.read())
        return

    print("Ollama Batch Text Processor")
    print("")
    print("This script can run text prompts over a list of text files")
    print("and print the results.")
    print("")
    print("Usage: python ollama-batch.py -d <file> -p <prompt>")
    print("       python ollama-batch.py -d recipes -p 'Is this recipe a sweet dessert or salty food?'")
    print("")
    print("       python ollama-batch.py -d <file> -f <prompt file>")
    print("       python ollama-batch.py -d recipes -f sweet_or_salty.txt")

if __name__ == "__main__":
    main()