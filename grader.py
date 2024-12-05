import subprocess
import json
import os
from typing import Counter
from openai import OpenAI


class CodeEvaluationPipeline:
    def __init__(self):
        self.repo_name = None
        self.branch_name = None
        self.language_used = None
        self.commit_history = None
        self.lint_check_result = None
        self.changed_files = None
        self.directory_structure = None
        self.openai_client = OpenAI()

    # Methods from evaluate.py
    def get_all_branches(self):
        try:
            result = subprocess.run(
                ["git", "branch", "-r"],
                text=True,
                capture_output=True,
                check=True,
            )
            branches = result.stdout.strip().split("\n")
            return [
                branch.strip().replace("origin/", "")
                for branch in branches
                if "origin/" in branch
            ]
        except subprocess.CalledProcessError as e:
            return f"Error getting branches: {e}"

    def find_extra_branch(self, branches, main_branch="main"):
        extra_branches = [branch for branch in branches if branch != main_branch]
        return extra_branches[0] if extra_branches else None

    def get_commits_on_branch(self, extra_branch, main_branch="main"):
        try:
            # handle the case where changes are directly made on the main branch

            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"origin/{main_branch}..origin/{extra_branch}",
                    "--oneline",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n")
            return commits if commits else []
        except subprocess.CalledProcessError as e:
            return f"Error checking commits: {e}"

    def run_lint_check(self, extra_branch):
        try:
            subprocess.run(["git", "checkout", extra_branch], check=True)
            result = subprocess.run(
            ["npm", "--prefix", self.language_used, "run", "lint"],
                text=True,
                capture_output=True,
            )
      
            return (
                f"Linter check passed on branch '{extra_branch}' ✅"
                if result.returncode == 0
                else f"Linter issues found on branch '{extra_branch}':\n{result.stdout}"
            )
        except subprocess.CalledProcessError as e:
            return f"Error running linter: {e}"

    # Methods from extract_contents.py
    def get_repo_name(self):
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.repo_name = os.path.basename(result.stdout.strip())
            return self.repo_name
        except subprocess.CalledProcessError as e:
            return f"Error getting repository name: {e}"

    def get_changed_files(self, branch, main_branch="main"):
        try:
            result = subprocess.run(
                [
                    "git",
                    "diff",
                    "--name-only",
                    f"origin/{main_branch}..origin/{branch}",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            self.changed_files = [
                file for file in result.stdout.strip().split("\n") if file
            ]
            return self.changed_files
        except subprocess.CalledProcessError as e:
            return f"Error getting changed files: {e}"

    def detect_language_from_files(self):
        """
        Deduce the language used based on the majority of the top-level directories in changed files.
        """
        if not self.changed_files:
            return "Unknown"

        # Extract the top-level directories
        top_level_dirs = [
            file.split("/")[0] for file in self.changed_files if "/" in file
        ]

        # Count occurrences of each directory
        dir_counts = Counter(top_level_dirs)
        most_common_dir, _ = dir_counts.most_common(1)[0]
        return most_common_dir

    def get_file_content(self, file_path):
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {file_path}: {e}"

    def format_directory_structure(self, files):
        directory_structure = {self.repo_name: {}}
        for file in files:
            parts = file.split("/")
            current = directory_structure[self.repo_name]
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = None
        return directory_structure

    # Methods from openapi_handler.py
    def ask_openai(self, file_path):
        try:
            with open(file_path, "r") as f:
                file_contents = f.read()
            prompt = f"""
                Evaluation Prompt
                You are tasked with assessing a coding assignment against specific criteria. The assessment is divided into four sections. Follow the instructions and scoring guidelines carefully.

                Section 1: Code Quality
                Stewardship (0–2 points):

                2 Points: The code is linted, unused code is removed, and the repository is clean of local environment files.
                1 Point: Some effort is made to maintain the codebase, but it falls short in one or more areas.
                0 Points: Codebase shows little to no effort in stewardship.
                Style and Documentation (0–2 points):

                2 Points: Code is logical, easy to follow, efficient, and accompanied by adequate documentation (comments, README, etc.).
                1 Point: Code is somewhat logical and documented but could be improved.
                0 Points: Code is poorly styled or lacks adequate documentation.
                Section 2: Version Control and Clever Code Usage
                Separate Branch (1 or 0):

                1 Point: The code is submitted on a branch other than main.
                0 Points: The code is submitted directly on the main branch.
                Clear Commits (1 or 0):

                1 Point: The repository includes multiple, clearly described commits.
                0 Points: Commit messages are unclear or there are no meaningful commits.
                Advanced Coding Practices (0–2 points):

                2 Points: The majority of the following are present:
                Clever use of classes, dependency injection, or recursion.
                Clean, commented code that is easy to follow.
                README is well-updated.
                Clear instructions for running the service.
                1 Point: At least one of the above practices is present.
                0 Points: None of these practices are present.
                Section 3: Data Persistence – Schema Design
                Evaluate the schema based on the following boolean criteria (1 or 0 for each):

                Model can be created and updated:
                1 Point: The schema can be implemented using the chosen database and supports updates.
                0 Points: It cannot.
                Supports multiple trees:
                1 Point: Schema can handle multiple trees efficiently.
                0 Points: It cannot.
                Root node representation:
                1 Point: A node with no parent is represented (e.g., parent_id is nullable).
                0 Points: It is not.
                Proper data types:
                1 Point: IDs are appropriate types (e.g., integer or bigint); label is a suitable type (e.g., varchar).
                0 Points: They are not.
                Schema scalability:
                1 Point: Schema is efficient for thousands of nodes and multiple trees, includes appropriate indexing, or trade-offs are explained.
                0 Points: It is not.
                Score: Sum of all points (Maximum: 5).

                Section 4: Data Persistence – Queries
                Evaluate the queries based on the following boolean criteria (1 or 0 for each):

                Query for GET:
                1 Point: Query retrieves proper results, including single or all records.
                0 Points: It does not.
                Tree-building logic:
                1 Point: A recursive function or description effectively builds the tree.
                0 Points: It does not.
                Query for CREATE:
                1 Point: Query properly creates a record with attributes.
                0 Points: It does not.
                Query for UPDATE:
                1 Point: Query properly updates a record.
                0 Points: It does not.
                Query for DELETE:
                1 Point: Query deletes a record only if it has no children; child check and delete are transactional.
                0 Points: It does not.
                Query Performance:
                1 Point: Queries use appropriate indexing (e.g., node_id and parent_id).
                0 Points: They do not.
                Supports multiple trees:
                1 Point: Handles root node representation and avoids ID conflicts.
                0 Points: It does not.
                Score: Sum of all points (Maximum: 7).

                Meta Section: Final Recommendation
                Recommend Moving Forward (Y/N):

                Use the total score as a strong guide.
                Bias toward "Yes" if the score is close but avoid soft answers. Provide a final "Yes" (Y) or "No" (N).
                Output Structure
                Section 1: Code Quality

                Stewardship: [Score: X/2]
                Style and Documentation: [Score: X/2]
                Total: X/4
                Section 2: Version Control and Clever Code Usage

                Separate Branch: [1/0]
                Clear Commits: [1/0]
                Advanced Practices: [Score: X/2]
                Total: X/4
                Section 3: Schema Design

                Model creatable and updatable: [1/0]
                Supports multiple trees: [1/0]
                Root node representation: [1/0]
                Proper data types: [1/0]
                Schema scalability: [1/0]
                Total: X/5
                Section 4: Queries

                GET Query: [1/0]
                Tree-building logic: [1/0]
                CREATE Query: [1/0]
                UPDATE Query: [1/0]
                DELETE Query: [1/0]
                Query performance: [1/0]
                Supports multiple trees: [1/0]
                Total: X/7
                Final Total Points: X/20
                Recommendation: [Yes/No]

                Additional Notes: [Optional detailed feedback]
                Here is the code submitted by the candidate:
                {file_contents}
                """
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code evaluation assistant.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI API: {e}"

    # Main workflow method
    def evaluate_code(self, main_branch="main"):
        branches = self.get_all_branches()
        self.branch_name = self.find_extra_branch(branches, main_branch)
        print("branch worked on:", self.branch_name)
        if not self.branch_name:
            print("No extra branch found apart from 'main'. ❌")
            self.branch_name = "main"

        self.commit_history = self.get_commits_on_branch(self.branch_name)
        print("commit history:", self.commit_history)

        self.get_repo_name()
        print("repo name:", self.repo_name)

        self.get_changed_files(self.branch_name)
        print("changed files:", self.changed_files)

        self.language_used = self.detect_language_from_files()
        print("language used:", self.language_used)

        self.lint_check_result = self.run_lint_check(self.branch_name)
        print("lint check result:", self.lint_check_result)

        self.directory_structure = self.format_directory_structure(self.changed_files)
        print("directory structure:", self.directory_structure)

        # Prepare the directory structure for output
        directory_output = "\n".join(self.print_directory_structure(self.directory_structure))
        print("directory output:", directory_output)

        # Prepare the output content
        output = [
            "### Repository Evaluation Summary",
            f"**Branch Worked On:** {self.branch_name}",
            f"**Repository Name:** {self.repo_name}",
            f"**Language Used:** {self.language_used}",
            f"**Commit History:**",
        ]

        if isinstance(self.commit_history, list):
            output.extend([f"- {commit}" for commit in self.commit_history])
        else:
            output.append(self.commit_history)  # Include error message if commits couldn't be fetched

        output.extend([
            f"**Lint Check Result:**\n{self.lint_check_result}",
            "\n### Directory Structure:\n",
            directory_output,
            "\n### Changed Files and Their Contents:\n",
        ])

        # Add file contents to the output
        for file in self.changed_files:
            content = self.get_file_content(file)
            if content:
                output.append(f"#### {file}:\n```\n{content}\n```\n")

        # Save the formatted output to a file
        output_file = "branch_changes_output.txt"
        with open(output_file, "w") as f:
            f.write("\n".join(output))

        print(f"Evaluation completed. Results saved to {output_file}.")
        return output_file

    def print_directory_structure(self, structure, prefix=""):
        result = []
        for key, value in structure.items():
            if value is None:
                result.append(f"{prefix}{key}")
            else:
                result.append(f"{prefix}{key}/")
                result.extend(self.print_directory_structure(value, prefix + "  "))
        return result


# Example usage:
if __name__ == "__main__":
    evaluator = CodeEvaluationPipeline()
    result = evaluator.evaluate_code()
    print(result)
