import os
from openai import OpenAI

client = OpenAI()

def ask_chatgpt(file_path):
    """Read the file and ask a question to ChatGPT."""
    try:
        # Read the file contents
        with open(file_path, "r") as f:
            file_contents = f.read()

        # Create the prompt
        prompt = (
            '''
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
'''
            f"{file_contents}\n\n"
        )

        # Call OpenAI API
        response =  client.chat.completions.create(
            model="gpt-4o",  # Use gpt-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a code evaluation assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        # Extract and return the response
        answer =  response.choices[0].message.content
        return answer

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # File path and question
    file_path = "branch_changes_output.txt"
    #question = "Is the code well commented?, please provide just the score out of 2 in the first line, the score can be 0, 0.5, 1,1.5 or 2; followed with the explanation"

    # Ask ChatGPT
    answer = ask_chatgpt(file_path)
    if answer:
        print("ChatGPT's Response:\n")
        print(answer)
