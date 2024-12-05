import subprocess
import json


def get_all_branches():
   # """Get a list of all branches in the repository."""
    try:
        result = subprocess.run(
            ["git", "branch", "-r"],
            text=True,
            capture_output=True,
            check=True,
        )
        branches = result.stdout.strip().split("\n")
        # Extract branch names, removing "origin/" prefix
        branch_names = [branch.strip().replace("origin/", "") for 
        branch in branches if "origin/" in branch]
        return branch_names
    except subprocess.CalledProcessError as e:
        return f"Error getting branches: {e}"


def find_extra_branch(branches, main_branch="main"):
    #"""Identify an extra branch other than the main branch."""
    extra_branches = [branch for branch in branches if branch != main_branch]
    if extra_branches:
        return extra_branches[0]  # Assume only one extra branch for simplicity
    return None


def get_commits_on_branch(extra_branch, main_branch="main"):
    #"""Check if there are commits on the extra branch."""
    try:
        result = subprocess.run(
            ["git", "log", f"origin/{main_branch}..origin/{extra_branch}", "--oneline"],
            text=True,
            capture_output=True,
            check=True,
        )
        commits = result.stdout.strip().split("\n")
        if len(commits):
            print(f"Commits found on branch '{extra_branch}' ✅", commits)
            return commits
        
        else:
            print( f"No commits found on branch '{extra_branch}' ❌")
            return []
    except subprocess.CalledProcessError as e:
        return f"Error checking commits: {e}"
    

def run_lint_check(extra_branch):
    #"""Run a linter on the extra branch."""
    try:
        # Checkout the extra branch
        subprocess.run(["git", "checkout", extra_branch], check=True)

        # Run flake8 linter
        result = subprocess.run(
            ["npm", "run", "lint"],
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            return f"Linter check passed on branch '{extra_branch}' ✅"
        else:
            return f"Linter issues found on branch '{extra_branch}':\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error running linter: {e}"



def main():
    """Main function to evaluate submission."""
    # Get all branches
    branches = get_all_branches()
    if isinstance(branches, str):  # Error occurred
        print(branches)
        return

    # Find the extra branch
    extra_branch = find_extra_branch(branches)
    if not extra_branch:
        evaluation_summary = {
            "branches": branches,
            "evaluation": "No extra branch found apart from 'main'. ❌",
        }
    else:
        # Check for commits on the extra branch
        commit_check_result = get_commits_on_branch(extra_branch)

        lint_check_result = run_lint_check(extra_branch)



        evaluation_summary = {
            "branches": branches,
            "extra_branch": extra_branch,
            "commit_check": commit_check_result,
            "lint_check": lint_check_result,
        }

    

    # Save results to a JSON file
    with open("evaluation_results.json", "w") as f:
        json.dump(evaluation_summary, f, indent=4)

    print("Evaluation completed. Results saved to evaluation_results.json.")


if __name__ == "__main__":
    main()
