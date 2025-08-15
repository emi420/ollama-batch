# Ollama Batch Classification Tool

This simple utility will runs LLM prompts over a list of texts
or images for classify them, printing the results as a JSON response.

## Quick start

### Requirements

You'll need Ollama installed in your system.

Default model is `gemma3:4b`, but you can use any other model with the `-m <model>` parameter.

### Install

`pip install ollama-batch`

### Usage

```
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?'
```

### Other examples

```bash
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=ingredients
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=title
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url
ollama-batch -d examples/images -i --prompt-file examples/sweet_or_salty.txt
```

### Help

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

### License

You may use this project under the terms of the GNU Affero General Public License (GNU AGPL) Version 3.

(c) 2024 Emilio Mariscal
