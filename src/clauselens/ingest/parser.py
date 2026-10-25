import re 

def clean_text(text: str) -> str:
    # fixing the corrupted rupee symbol
    text = re.sub(r"(?<![A-Za-z])n(?=\d)", "₹", text)


    # Remove Markdown escaping from underscores ( landlord __________________)
    text = text.replace(r"\_", "_")


    return text