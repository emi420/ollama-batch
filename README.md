# Ollama Batch Text Processor

This simple script run text LLM prompts over a list of texts and print the results as JSON. 

## Usage

```bash
python ollama-batch.py -d <directory> -p <prompt> 
python ollama-batch.py -d <directory> --prompt-file <prompt file>
python ollama-batch.py -f <json_ file> -p <prompt> 
python ollama-batch.py -f <json file> -p <prompt> --json-property=<json property to analyze>
python ollama-batch.py -f <json file> -p <prompt> --json-append=<propreties to append>
```

### Examples

```bash
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?'
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=ingredients
python ollama-batch.py -d examples/recipes -p 'Is this recipe a sweet dessert or salty food?' --json-property=title
python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt
python ollama-batch.py -f examples/recipes.json --prompt-file examples/sweet_or_salty.txt --json-append=title,url
```

## Requirements

1. Install [Ollama](https://ollama.com/download)
2. Install the Python package `pip install ollama`
3. Run Ollama `ollama run llama3` / `ollama serve`


(c) 2024 Emilio Mariscal
