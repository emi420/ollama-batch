# Ollama Batch Text Processor

This simple utility will runs LLM prompts over a list of texts
and print the results as a JSON response.

### How it works? 

It contatenates your prompt with each text and call ollama over it.

For example, if your prompt is:

`Is this recipe a sweet dessert or salty food? answer only with a hashtag #sweet or #salty`

And your texts are:

`Fruit salad: apple, orange, pear, grape, strawberry, sugar`
`Potatoes, mayonnaise, salt, black pepper, red onion, eggs`

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

pip install git+https://github.com/emi420/ollama-batch

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
  --question-first JSON_APPEND
            First the question, then the prompt
```

### Examples

```bash
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?'
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=ingredients
ollama-batch -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=title
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt
ollama-batch -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url
```

## Quick start

### Requirements

1. Install [Ollama](https://ollama.com/download)
2. Install the package `pip install ollama`
3. Run Ollama `ollama serve`

### Run

```sh
ollama-batch -d examples/recipes \
    -p "Is this recipe a sweet dessert or salty food" \
    > recipes_results.json
```

(c) 2024 Emilio Mariscal
