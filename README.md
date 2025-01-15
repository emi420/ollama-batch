# Ollama Batch Text Processor

This simple utility will runs LLM prompts over a list of texts
or images and print the results as a JSON response.

### How it works? 

### For texts

It contatenates your prompt with each text and call Ollama over it.

For example, if your prompt is:

`Is this recipe a sweet dessert or salty food? answer only with a hashtag #sweet or #salty`

And your texts are:

1. `Fruit salad: apple, orange, pear, grape, strawberry, sugar`
2. `Potatoes, mayonnaise, salt, black pepper, red onion, eggs`

It will run:

```
Fruit salad: apple, orange, pear, grape, strawberry, sugar

Is this recipe a sweet dessert or salty food? answer only with a hashtag #sweet or #salty
```

```
Potatoes, mayonnaise, salt, black pepper, red onion, eggs

Is this recipe a sweet dessert or salty food? answer only with a hashtag #sweet or #salty
```

## Quick start

### Install

Directly from the main branch:

`pip install git+https://github.com/emi420/ollama-batch`

### Usage

```sh
ollama-batch \
    [--directory DIRECTORY] \
    [--file FILE] [--model MODEL] \
    [--prompt PROMPT] \
    [--prompt-file PROMPT_FILE] \
    [--json-property JSON_PROPERTY] \
    [--json-append JSON_APPEND] \
    [--question-first]

options:
  -h, --help
            Show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
            Directory with files you want to process
  --file FILE, -f FILE
            JSON file you want to process
  --model MODEL, -m MODEL
            Model you want to use
  --prompt PROMPT, -p PROMPT
            Prompt text
  --prompt-file PROMPT_FILE
            Text file with a prompt
  --json-property JSON_PROPERTY
            JSON property that you want to use
  --json-append JSON_APPEND
            Property that you want to append to the results
  --question-first
            First the question, then the prompt
  --images, -i
            Look for images (use a vision model)
```

### Examples

```bash
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?'
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=ingredients
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=title
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url
ollama-batch -d examples/images -i -p 'What do yoy see in this picture?'
```

(c) 2024 Emilio Mariscal
