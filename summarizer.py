import os
import warnings

import ebooklib
from ebooklib import epub

from nltk.tokenize import word_tokenize

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from colorama import Fore, Style, init

#local import from cli.py
from cli import file_picker, get_instruction_input



def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = ''

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text += item.get_content().decode('utf-8', 'ignore') + ' '

    return text

def tokenize_into_chunks(text, chunk_size=100000):
    tokens = word_tokenize(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def summarize_with_anthropic(text_chunk, instructions):
    anthropic = Anthropic()

    completion = anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=200000,
        prompt=f"{HUMAN_PROMPT} {instructions}:\n{text_chunk}{AI_PROMPT}",
    )

    return completion.completion

def main():
    # Suppress specific UserWarning in ebooklib
    warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")
    
    # Initialize colorama
    init(autoreset=True)

    # File picker
    print(Fore.BLUE + "Choose an EPUB file:")
    selected_file = file_picker()
    print(Fore.GREEN + f"Selected file: {selected_file}\n")

    # Instruction input
    print(Fore.BLUE + "Choose an instruction option:")
    instructions = get_instruction_input()

    if instructions == "Enter your own instruction":
        instructions = input(Fore.BLUE + "Enter your custom summarization instructions (or enter for default): ") or "Summarize the following text"
    print(Fore.GREEN + f"Selected instruction: {instructions}\n")

    # Processing warning
    print(Fore.YELLOW + "Processing file, please wait... (this normally takes about 80 seconds)")

    text = epub_to_text(selected_file)
    chunks = tokenize_into_chunks(text)

    for i, chunk in enumerate(chunks):

        summary = summarize_with_anthropic(chunk, instructions)
        print(f'{Fore.CYAN}Summary of section {i + 1} of {len(chunks)}:\n\n{summary}\n')

        if i + 2 <= len(chunks):
            print(Fore.YELLOW + f'Processing section {i + 2} of {len(chunks)}, please wait (each section takes about 80 seconds)...')

    print(Fore.GREEN + 'Done! Text has been tokenized and summaries were generated.')

if __name__ == "__main__":
    main()

