# ivory-orchid

# Shelter Pet Adoption Board

**“Every pet deserves a home.”**

## Overview

The **Shelter Pet Adoption Board** is a platform designed to help local animal shelters showcase pets available for adoption and connect them with the right adopters.

Each pet has a rich profile that goes beyond basic stats like age or size. We focus on **personality, habits, and special traits** because people don’t fall in love with a checklist — they fall in love with a story.

Our goal is simple:  
**Make it easier for shelters to tell each pet’s story and for adopters to find their perfect match.**

---

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML/CSS/Plain JS
- **Database**: TBD
- **Version Control**: Git & GitHub

---

## Contribution Workflow

Follow these steps to contribute to the project in a clean and consistent way.

### 1.Clone the repository

Download the repository to your local machine:

```bash
git clone https://github.com/nhcarrigan-spring-2026-cohort/ivory-orchid.git
```

### 2.Create a new working branch

Always create a new branch for your work. The branch name should describe what you're working on.

```bash
git checkout -b feature/your-branch-name-short-description
```

### 3.Make your changes and commit your work

Write clear and meaningful commit messages that explain what you added or changed.

```bash
git add .
git commit -m "Your messages"
```

### 4. Push your branch to Github

Upload your branch so it’s available for review:

```bash
git push origin feature/your-branch-name-short-description
```

### 5. Open a Pull Request

1. Go to the repository on GitHub, switch to your feature branch, and click **Compare & pull request**

2. Make sure the base branch is `main`, add a clear title and description, and link any related issues if needed.

3. Click **Create pull request** to submit your changes for review.

### 6. Remove your branch after merge:

Once your pull request is approved and merged, clean up your branch.

---

## Run the webserver

Note: on Unix systems the python executable is sometimes called python3

#### 1. Install python and pip

1. Install python
   * Windows: ``winget python``
   * Linux (debian/ubuntu): ``sudo apt install python3``

2. Install pip
``python -m pip install``

3. Clone the repository (see above) and enter it (`cd ivory-orchid`)

#### 2. (Optional) install and activate venv

1. Install venv
   * Windows: ``winget python-venv``
   * Linux (debian/ubuntu): ``sudo apt install python3-venv``

2. Change directory to the backend
``cd backend``

3. Create the virtual environment
``python -m venv .venv``
 
   _tip: to change the name of the virtual environment add `--prompt name`_

4. Activate the virtual environment 
   * Windows: ``.\.venv\Scripts\activate``
   * Linux: ``source .venv/bin/activate``
   
   To disable the virtual environment:
   * Windows command prompt: ``.\.venv\Scripts\deactivate``
   * Any other shell: `` deactivate``
5. Return to the project root `cd ..`

#### 3. Install the dependencies

```bash
pip install -r backend/requirements.txt
```

#### 4. Run flask

To host the webpage to localhost (127.0.0.1)
```bash
flask --app backend run
```

To enable debugging mode add the flag `--debug`

To expose the server to all interfaces add `--host=0.0.0.0`

