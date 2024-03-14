import os
import sys
import click

def get_epub_files():
    current_directory = os.getcwd()
    books_directory = os.path.join(current_directory, "books")

    files = [f for f in os.listdir(books_directory) if f.lower().endswith('.epub')]
    return files


def select_from_list(options, prompt):
    click.echo("\n".join(f"{i + 1}. {option}" for i, option in enumerate(options)))
    
    selected_option = click.prompt(
        prompt,
        type=click.IntRange(1, len(options)),
        default=1,
        show_default=True,
        prompt_suffix=' (Enter the number)'
    )

    return options[selected_option - 1]


def file_picker():
    files = get_epub_files()

    selected_file = select_from_list(files, "Select an EPUB file")
    
    return selected_file
    
    
def model_picker():
    models = ["Claude 3","GPT-4"]

    selected_model = select_from_list(models, "Select a model to use for summarization")
    
    return selected_model


def get_instruction_input():
    instruction_options = [
        "Craft a comprehensive summary (in English, you may need to translate) that captures the essence of the following text by highlighting key plot points, also if there are any any intriguing, humorous, salacious or lesser-known details that are worthwhile, please highlight those as well. If available, put the title, author, language and country of publication at the top of your summary.",
        "Create a summary of the strangest and funniest pieces of trivia from the following text",
        "Enter your own instruction"
    ]

    selected_option = select_from_list(instruction_options, "Choose an instruction option")
    
    return selected_option
