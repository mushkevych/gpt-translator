# GPT-powered Book Translator. Initially envisioned as a novel translator to Ukrainian language.

## Installation:

```bash
./start.sh install
```


## Translation:

1. Update `context.py` with the details of the book translation
1. Update `secrets.py` file with the OpenAI API secret key
1. Place the text of the novel into `text_source` folder
1. Update `translator.py` `__main__` section to perform translation of the chosen book
1. Call 

```bash
.miniconda/bin/conda run --name translator python translator.py 
```
1. Find the translated text of the novel in the `text_translated` folder
