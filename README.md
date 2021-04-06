**Python-Challenge**

**Tasks:**

1. Dataset - recipes.json
2. Write a script in Python that reads the recipes and extracts every recipe that has “Chilies” as one of the ingredients. Your code should allow for misspelling of the word for example Chiles as well as the singular form of the word.
3. Add an extra field to each of the extracted recipes with the name difficulty. The difficulty field would have a value of "Hard" if the sum of prepTime and cookTime is greater than 1 hour, "Medium" if the total is between 30 minutes and 1 hour, "Easy" if the total is less than 30 minutes, and "Unknown" otherwise.
4. The resulting dataset should be saved as a *.csv file.

*Moreover, I wrote an additional function which sends an email with final CSV file and wrapped the application into Docker image and following tutorial instructions I made a deployment to the Amazon Elastic Compute Instance.*

**How to run program:**

I assume you are using a Unix system and Python 3.

Execute the next steps in yours command line:

- pip install virtualenv
- python3 -m venv test_task_Belova_venv
- source test_task_Belova_venv/bin/activate
- pip install -r requirements.txt
- python3 main.py


Recipes will be downloaded automatically.

Good luck!
