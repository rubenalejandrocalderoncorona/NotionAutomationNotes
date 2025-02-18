import re

def process_markdown(md_file_path):
    """
    Evaluates each line of a Markdown file, replaces <antArtifact> and </antArtifact>
    tags with code fences (```), and returns the modified content.
    """

    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:  # Handle potential encoding issues
            md_content = f.readlines()
    except FileNotFoundError:
        return f"Error: File not found at {md_file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

    modified_content = []
    in_ant_artifact = False

    for line in md_content:
        # Check for opening <antArtifact>
        match_start = re.search(r"<antArtifact.*?>", line)  # Non-greedy matching
        if match_start:
            line = line[:match_start.start()] + "```" + line[match_start.end():] #Replace <antArtifact> with ```
            in_ant_artifact = True
        elif in_ant_artifact:
            match_end = re.search(r"</antArtifact>", line)
            if match_end:
                line = line[:match_end.start()] + "```" + line[match_end.end():]
                in_ant_artifact = False
        
        modified_content.append(line)

    return "".join(modified_content)


def write_modified_markdown(modified_content, output_file_path):
    """Writes the modified Markdown content to a new file."""
    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(modified_content)
        print(f"Modified Markdown written to {output_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")



# Example usage:
input_file = "..\\automate_github_repo_updates_on_local_file_save.md"  # Replace with your input Markdown file
output_file = "output.md" # Replace with your desired output file

modified_md = process_markdown(input_file)

if isinstance(modified_md, str) and modified_md.startswith("Error"): # Check for errors
    print(modified_md)
else:
    write_modified_markdown(modified_md, output_file)