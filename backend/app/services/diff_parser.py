import re

def is_diff(text: str) -> bool:
    """Check if the text represents a unified git diff."""
    if not text:
        return False
    # Common unified diff headers
    indicators = [
        r"^diff --git ",
        r"^--- (a/|\w+)",
        r"^\+\+\+ (b/|\w+)",
        r"^@@ -\d+,\d+ \+\d+,\d+ @@"
    ]
    return any(re.search(ind, text, re.MULTILINE) for ind in indicators)

def extract_files(diff_text: str) -> list:
    """Extract files modified in the diff."""
    files = []
    current_file = None
    
    for line in diff_text.split("\n"):
        if line.startswith("diff --git"):
            # Extract filenames
            parts = line.split(" ")
            if len(parts) >= 4:
                file_a = parts[2][2:] if parts[2].startswith("a/") else parts[2]
                file_b = parts[3][2:] if parts[3].startswith("b/") else parts[3]
                current_file = file_b
                files.append(current_file)
    return files
