# Ollama Batch Text Processor

This simple script run text LLM prompts over a list of texts and print the results as JSON. 

## Usage

```sh
python ollama-batch.py \
    [--directory DIRECTORY] \
    [--file FILE] [--model MODEL] \
    [--prompt PROMPT] \
    [--prompt-file PROMPT_FILE] \
    [--json-property JSON_PROPERTY] \
    [--json-append JSON_APPEND]

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
```

### Examples

```bash
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?'
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=ingredients
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=title
python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt
python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url
```

## Quick start

### Requirements

1. Install [Ollama](https://ollama.com/download)
2. Install the Python package `pip install ollama`
3. Run Ollama `ollama serve`

### Run

```sh
python ollama-batch.py -d examples/recipes \
    -p "Is this recipe a sweet dessert or salty food" \
    > recipes_results.json
```

(c) 2024 Emilio Mariscal
