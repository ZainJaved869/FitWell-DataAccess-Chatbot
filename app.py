import os
import re
from rich.console import Console
from rich.panel import Panel
from rich.box import HEAVY

console = Console()

def file_exists(filepath):
    """Check if the file exists."""
    return os.path.isfile(filepath)

def clean_text(text):
    """Remove markdown formatting and URLs while preserving essential content."""
    text = re.sub(r'http\S+|\[.*?\]\(.*?\)', '', text)
    text = text.replace('**', '').replace('__', '').replace('#', '')
    return text.strip()

def find_lines_with_headings(content, keyword):
    """Find lines containing the keyword along with their headings."""
    sections = re.split(r'\n\s*\n', content)
    results = []
    current_heading = "Untitled Section"

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue

        # Detect heading
        if lines[0].strip().endswith(':') or lines[0].isupper():
            current_heading = lines[0].strip(':').strip()

        # Check each line for the keyword
        for line in lines:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                cleaned_line = clean_text(line)
                if cleaned_line:
                    results.append((current_heading, cleaned_line))

    return results if results else None

def search_definition(filepath, keyword):
    """Search for keyword and return matching lines with headings."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        return find_lines_with_headings(content, keyword)

def text_chatbot():
    """Chatbot for FitWellHub text data with heading detection (line-focused)."""
    console.print(Panel("[bold cyan]Welcome! I'm your FitWellHub Data Assistant 📚\nType 'exit' to quit.[/bold cyan]",
                        title="Line-Aware Info Bot", box=HEAVY))

    file_path = r"C:\Users\Ic\Desktop\Buzz Chatbot\FitWell data Access by text bot\Fit.txt"

    if not file_exists(file_path):
        console.print(Panel("[bold red]Data file not found. Exiting...[/bold red]", box=HEAVY))
        return
    else:
        console.print(Panel("[bold green]System loaded and ready for queries.[/bold green]", box=HEAVY))

    while True:
        question = console.input("[bold magenta]🧑 You:[/bold magenta] ").strip()

        if question.lower() == 'exit':
            console.print(Panel("[bold cyan]Session ended.[/bold cyan]", box=HEAVY))
            break

        if question.lower() in ["developer", "who is your developer?", "what is your developer name?"]:
            console.print(Panel("Developer: Rao Zain", box=HEAVY))
            continue

        if not question:
            console.print(Panel("[bold red]❌ Please type a question.[/bold red]", box=HEAVY))
            continue

        keyword = re.sub(r'^(what is|tell me about|explain|show|where|)\s+', '', question.lower()).strip(' ?')
        results = search_definition(file_path, keyword)

        if results:
            for i, (heading, line) in enumerate(results[:10]):  # Show up to 10 matching lines
                console.print(Panel(line,
                                    title=f"📖 {heading} — Match {i+1}",
                                    style="bold green",
                                    box=HEAVY))
        else:
            console.print(Panel(f"[bold red]No content found for '{keyword}'.[/bold red]", box=HEAVY))

if __name__ == "__main__":
    text_chatbot()
