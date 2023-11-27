import os
import time
import sys
import threading
import itertools
import curses
import warnings

import ebooklib
from ebooklib import epub

from nltk.tokenize import word_tokenize

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Suppress specific UserWarning in ebooklib
warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")

def animate_processing(seconds=3, width=3):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        progress = int((elapsed_time / seconds) * width)
        bar = f"{'.' * progress}{' ' * (width - progress)}"

        sys.stdout.write('\rSummarizing, please wait' + bar)
        sys.stdout.flush()

        if elapsed_time > seconds:
            break

        time.sleep(0.1)

    sys.stdout.write('\r')  # Clear the line
    sys.stdout.flush()

def get_epub_files():
    current_directory = os.getcwd()
    files = [f for f in os.listdir(current_directory) if f.lower().endswith('.epub')]
    return files

def draw_menu(stdscr, selected_row_idx):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    files = get_epub_files()

    for idx, file in enumerate(files):
        x = width // 2 - len(file) // 2
        y = height // 2 - len(files) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, file)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, file)

    stdscr.refresh()

def file_picker(stdscr):
    if stdscr is None:
        return None

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0
    key = 0

    while key != 10:  # Enter key
        draw_menu(stdscr, current_row)
        key = stdscr.getch()

        if key == curses.KEY_DOWN and current_row < len(get_epub_files()) - 1:
            current_row += 1
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1

    selected_file = get_epub_files()[current_row]
    return selected_file

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = ''

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text += item.get_content().decode('utf-8', 'ignore') + ' '

    return text

def tokenize_into_chunks(text, chunk_size=70000):
    tokens = word_tokenize(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def summarize_with_anthropic(text_chunk, instructions):
    anthropic = Anthropic()

    animate_processing()

    completion = anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=100000,
        prompt=f"{HUMAN_PROMPT} {instructions}:\n{text_chunk}{AI_PROMPT}",
    )

    # clear the processing animation
    sys.stdout.write('\r')  # Clear the line
    sys.stdout.flush()

    return completion.completion

def main():
    
    epub_path = curses.wrapper(file_picker)

    while not os.path.isfile(epub_path) or not epub_path.lower().endswith('.epub'):
        print('Invalid file path or file is not an EPUB. Please try again.')
        epub_path = curses.wrapper(file_picker)

    instructions = input("Enter summarization instructions (or press Enter for default 'Summarize the following text'): ") or "Summarize the following text"

    text = epub_to_text(epub_path)
    chunks = tokenize_into_chunks(text)
    
    for i, chunk in enumerate(chunks):

        summary = summarize_with_anthropic(chunk,instructions)
        print(f'Summary of section {i + 1} of {len(chunks)+1}:              \n\n{summary}\n')

    print(f'Done! Text has been tokenized and summaries were generated.')

if __name__ == "__main__":
    main()

