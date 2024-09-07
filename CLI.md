# CLI Wrapper for User and Sentence Management

This CLI tool allows you to manage users and sentences through a set of easy-to-use commands. You can create users, get reports, reward users, and manage sentences on the platform.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
   - [User Commands](#user-commands)
   - [Sentence Commands](#sentence-commands)
4. [Examples](#examples)

## Installation

Install dependencies via `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before using the CLI, create a configuration file named `cli_config.yaml` in the same directory as the script. The configuration file should have the following structure:

```yaml
host: "http://89.169.168.72/api"
admin_username: <<SET ME>>
admin_password: <<SET ME>>
```

- **`host`**: The base URL of the API.
- **`admin_username`** and **`admin_password`**: Credentials used for authentication with the API.

## Usage

### Running the CLI

To run the CLI tool, use the following command:

```bash
python cli.py --help
```

### User Commands

You can manage users by using the `user` subcommands:

1. **Create User**:
   Create a new user with a username and password. If no password is provided, a strong password will be generated automatically.

   ```bash
   python cli.py user create --username new_user --password password123
   ```

   You can skip the confirmation by using the `--yes` flag.

   ```bash
   python cli.py user create --username new_user --yes
   ```

2. **Get User Report**:
   Get a report for a specific user.

   ```bash
   python cli.py user report username
   ```

3. **Reward User**:
   Reward a user with a specified amount.

   ```bash
   python cli.py user reward --username username --amount 100
   ```

### Sentence Commands

You can manage sentences on the platform using the `sentence` subcommands:

1. **List Sentences**:
   List all sentences, or filter them by reviewer, error type, or other conditions.

   ```bash
   python cli.py sentence ls --reviewer reviewer_username --error-type grammar
   ```

   To include all sentences:

   ```bash
   python cli.py sentence ls --all
   ```

2. **Get Sentence by ID**:
   Retrieve a sentence by its ID.

   ```bash
   python cli.py sentence get 1
   ```

3. **Add Sentences**:
   Upload sentences from a JSON file.

   ```bash
   python cli.py sentence add sentences.json
   ```

## Examples

1. **Create a User**:

   Create a user with the username `john_doe` and an auto-generated password:

   ```bash
   python cli.py user create --username john_doe
   ```

2. **Reward a User**:

   Reward the user `john_doe` with 200 points:

   ```bash
   python cli.py user reward --username john_doe --amount 200
   ```

3. **List Sentences by Reviewer**:

   List all sentences reviewed by `john_doe`:

   ```bash
   python cli.py sentence ls --reviewer john_doe
   ```

4. **Get Sentence by ID**:

   Retrieve the sentence with ID `456`:

   ```bash
   python cli.py sentence get 456
   ```

5. **Add Sentences from JSON**:

   Upload sentences from a file named `sentences.json`:

   ```bash
   python cli.py sentence add sentences.json
   ```
