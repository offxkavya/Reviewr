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

def parse_diff_to_hunks(diff_text: str) -> list:
    """
    Parse a unified diff into files, hunks, and lines.
    Returns a list of files, each containing hunks, and each hunk containing lines with original line numbers.
    """
    files = []
    current_file = None
    hunks = []
    current_hunk = None
    new_line_no = 0
    
    hunk_header_re = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
    
    for line in diff_text.split("\n"):
        if line.startswith("diff --git"):
            if current_file:
                if current_hunk:
                    hunks.append(current_hunk)
                current_file["hunks"] = hunks
                files.append(current_file)
            parts = line.split(" ")
            file_b = parts[3][2:] if len(parts) >= 4 and parts[3].startswith("b/") else (parts[3] if len(parts) >= 4 else "unknown")
            current_file = {"filename": file_b, "hunks": []}
            hunks = []
            current_hunk = None
        elif line.startswith("@@"):
            if current_hunk:
                hunks.append(current_hunk)
            match = hunk_header_re.match(line)
            if match:
                new_line_no = int(match.group(1))
                current_hunk = {"header": line, "lines": []}
        elif current_hunk is not None:
            if line.startswith("+"):
                current_hunk["lines"].append({
                    "type": "added",
                    "line_number": new_line_no,
                    "content": line[1:]
                })
                new_line_no += 1
            elif line.startswith("-"):
                current_hunk["lines"].append({
                    "type": "deleted",
                    "line_number": None,
                    "content": line[1:]
                })
            else:
                # Context line (starts with space or empty)
                content = line[1:] if line.startswith(" ") else line
                current_hunk["lines"].append({
                    "type": "context",
                    "line_number": new_line_no,
                    "content": content
                })
                new_line_no += 1
                
    if current_file:
        if current_hunk:
            hunks.append(current_hunk)
        current_file["hunks"] = hunks
        files.append(current_file)
        
    return files
