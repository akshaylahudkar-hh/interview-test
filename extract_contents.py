import subprocess
import os



def get_repo_name():
    """Get the name of the current repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=True,
        )
        repo_path = result.stdout.strip()
        repo_name = os.path.basename(repo_path)
        return repo_name
    except subprocess.CalledProcessError as e:
        print(f"Error getting repository name: {e}")
        return "unknown_repo"

def get_changed_files(branch, main_branch="main"):
    """Get the list of files changed/added in a branch compared to the main branch."""
    try:
        # Use origin/<branch> to compare remote branches
        result = subprocess.run(
            ["git", "diff", "--name-only", f"origin/{main_branch}..origin/{branch}"],
            text=True,
            capture_output=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        print("files", files)
        return [file for file in files if file]  # Filter out empty lines
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def get_file_content(file_path):
    """Get the content of a specific file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def format_directory_structure(files, repo_name):
    """Format the directory structure of the changed files with repo name as root."""
    directory_structure = {repo_name: {}}
    for file in files:
        parts = file.split("/")
        current = directory_structure[repo_name]
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = None  # Mark file
    return directory_structure


def print_directory_structure(structure, prefix=""):
    """Print the directory structure recursively."""
    result = []
    for key, value in structure.items():
        if value is None:  # It's a file
            result.append(f"{prefix}{key}")
        else:  # It's a directory
            result.append(f"{prefix}{key}/")
            result.extend(print_directory_structure(value, prefix=prefix + "  "))
    return result

def main():
    """Main function to extract changed files and format them."""
    # Get the current branch
    branch = "test1"
    # Fetch all branches (needed in GitHub Actions)
    subprocess.run(["git", "fetch", "--all", "--tags", "--prune"], check=True)

    repo_name = get_repo_name()
    language = " "
    code_path = repo_name + "/" + language
    print("code_path", code_path)
    # Get the changed files
    changed_files = get_changed_files(branch)
    if not changed_files:
        print("No changed files detected.")
        return

    # # Format the directory structure
    # # Format the directory structure
    directory_structure = format_directory_structure(changed_files, code_path)
    directory_output = print_directory_structure(directory_structure)

    # Prepare the final output
    output = ["### Directory Structure:\n"]
    output.extend(directory_output)
    output.append("\n### File Contents:\n")

    for file in changed_files:
        content = get_file_content(file)
        if content is not None:
            output.append(f"#### {file}:\n")
            output.append("```\n")
            output.append(content)
            output.append("\n```\n")

    # Save the output to a file
    output_file = "branch_changes_output.txt"
    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"Branch changes have been saved to {output_file}.")

    #make openapi call 
    


if __name__ == "__main__":
    main()
