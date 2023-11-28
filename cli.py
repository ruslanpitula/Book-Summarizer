import os
import sys
import click

def get_epub_files():
    current_directory = os.getcwd()
    files = [f for f in os.listdir(current_directory) if f.lower().endswith('.epub')]
    return files

def select_from_list(options, prompt):
    # Display options
    click.echo("\n".join(f"{i + 1}. {option}" for i, option in enumerate(options)))
    
    # Get user input
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

    # Display file options
    selected_file = select_from_list(files, "Select an EPUB file")
    
    return selected_file

def get_instruction_input():
    # Define instruction options
    instruction_options = [
        "Summarize the following text",
        "Craft a comprehensive summary that captures the essence of the following text by highlighting key plot points, also if there are any any intriguing, humorous, salacious or lesser-known details that are worthwhile, please highlight those as well.",
        "Provide a concise summary focusing on the main ideas in the given text",
        "Create a summary of the strangest and funniest pieces of trivia from the following text",
        "Summarize the content, emphasizing significant details and important information",
        "Enter your own instruction"
    ]

    # Display instruction options
    selected_option = select_from_list(instruction_options, "Choose an instruction option")
    
    return selected_option

if __name__ == "__main__":
    # Add your main program logic here if needed
    pass

