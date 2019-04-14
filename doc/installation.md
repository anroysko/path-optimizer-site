# Installation

These instructions are for linux, and might not work on other OSes.

1. Clone the repository to your local computer with the command `git clone [url]`, where `[url]` is the clone url, currently https://github.com/anroysko/path-optimizer-site.git
2. Enter the directory the repository is in
3. Create a new virtual environment in the repository directory with the command `python3 -m venv venv`
4. Use the command `source venv/bin/activate` to activate the virtual environment
5. Make sure you have the newest version of pip by updating it, with the command `pip install --upgrade pip`
6. Install the dependencies with pip using `pip install -r requirements.txt`
7. Start the flask webserver with `python3 run.py`. Now the site should be running on your localhost.
