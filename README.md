# Chatbot Tutorial

## What Will We Learn

* ChatGPT: State of the Art Techology
* Frontend Development: HTML, CSS, JavaScript
    * HTML, CSS, JavaScript -> React -> React Native (Mobile APP development)
    * JavaScript -> TypeScript
* Backend Development: Python, MongoDB
    * Python -> Data Science
    * MongoDB: NoSQL is the future development trend, has better performance, and is more suitable for processing big data.

## Lessons

### Lesson 2

* OpenAI [ChatGPT](https://chat.openai.com/) Demo
* Prompt Engineering
    * How to ask ChatGPT, so that the ChatGPT will generate more accurate answers
    * Without Prompt Engineering
        ```
        how many calories for one orange?
        ```
    * With Prompt Engineering
        ```
        For examples:
        Input:
        how many calories for one apple?
        Output:
        95

        Now please do for this input:
        Input:
        how many calories for one orange?
        Output:
        ```
* Install MongoDB, Anaconda, PyCharm, Postman
* Get ChatGPT Key
* Coding Project Part 1: Backend Development using Python, MongoDB and OpenAI ChatGPT, Testing using Postman
* Homework (Review recording, try to implement the code by yourself)

### Lesson 3

* Coding Project Part 2: Frontend Development using HTML, CSS, JavaScript
* Homework (Review recording, try to implement the code by yourself)

## Quick Start

### Database

1. Install MongoDB following the [link](https://www.mongodb.com/try/download/community).
```
# macOS User
brew tap mongodb/brew
brew install mongodb-community@4.4
```

2. Install MongoDB Compass (GUI)  following the [link](https://www.mongodb.com/try/download/compass).

### Python

1. Install Anaconda following the [link](https://docs.anaconda.com/anaconda/install/index.html).

2. Create and activate environment using the following commands.
```
# Create Python environment
conda create --name chatbot-tutorial python=3.10.10

# Check Python environment
conda info --envs

# Activate environment
conda activate chatbot-tutorial

# Deactivate environment
conda deactivate

# Remove environment
conda remove -n chatbot-tutorial --all
```

3. Install `requirements.txt`.
```
pip install -r /path/to/requirements.txt
```

4. Install PyCharm following the [link](https://www.jetbrains.com/pycharm/download/?section=mac).

5. Install Postman following the [link](https://www.postman.com/downloads/).
