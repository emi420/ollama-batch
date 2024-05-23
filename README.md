# Ollama Batch Text Processor

This simple script run text prompts over a list of text files and print the results.

## Usage

```bash
python ollama-batch.py -d <file> -p <prompt>
python ollama-batch.py -d recipes -p 'Is this recipe a sweet dessert or salty food?'
python ollama-batch.py -d <file> -f <prompt file>
python ollama-batch.py -d examples/recipes -f examples/sweet_or_salty.txt
```

## Requirements

1. Install [Ollama](https://ollama.com/download)
2. Install the Python package `pip install ollama`
3. Run Ollama `ollama run llama3` / `ollama serve`


(c) 2024 Emilio Mariscal