# Documentation

## Purpose

This directory contains markdown files of all the sample code found in this project's `/languages` folder. These markdown files are used by Deepgram's community knowledge AI tool to provide a knowledge base of code. Since the tool cannot read code in specific code language files, these markdown files have been created.

## Updating Languages

If you update one of the languages that already exists in this project (for example `javascript` or `python`), you must also update the corresponding markdown file in this directory. To do so, uncomment the language in the `update_languages.yaml` file. This will trigger a GitHub action that will update the markdown file when the updated code is merged into the `main` branch.

For example, if you update `javascript` and `python`, you will need to uncomment the following lines in the `update_languages.yaml` file:

```yaml
languages:
  # - "c"
  # - "cpp"
  # - "csharp"
  # - "go"
  # - "java"
  - "javascript"
  # - "php"
  - "python"
  # - "ruby"
  # - "rust"
  # - "swift"
```

## Adding Languages

If you add a new language to this project, you will do the same thing as you did for updating an existing language. Simply add the language to the `update_languages.yaml` file.

For example, if you add `rust` as a new language folder, you will need to add the following lines to the `update_languages.yaml` file:

```yaml
languages:
  # - "c"
  # - "cpp"
  # - "csharp"
  # - "go"
  # - "java"
  # - "javascript"
  # - "php"
  # - "python"
  # - "ruby"
  - "rust"
  # - "swift"
```

You must also add a config file inside the `/languages` folder. This config file will identify the target files to scrape. For example, if you add a new language called `rust`, you will need to create a config file called `rust.yaml` inside the `/languages/rust` folder. The config file should look like this:

```yaml
target_files:
  - "*.rs"
```

## Output

If you have followed the steps above, you can expect to see an updated or newly-created markdown file in the documentation directory after your code is merged into the `main` branch.
