# Chatbot Tutorial

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
