# routinerun

A simple CLI tool for running multi-step command pipelines defined in YAML files.

## Features

- Load pipeline definitions from `.yaml` / `.yml` files in `~/.routinerun`
- List available pipelines in a formatted table (`list`)
- Execute pipeline steps sequentially using token lists via `subprocess` (`run`)

## Project Structure

```text
src/
└── routinerun/
    ├── core/
    │   ├── parser.py    # YAML loading and parsing
    │   └── runner.py    # Sequential step execution
    ├── tools/
    │   └── ...          # CLI commands (list, run)
    ├── main.py          # Typer CLI entry point
    ├── models.py        # Pipeline and step data models
    └── ui.py            # Rich terminal output
```

## Example Pipeline

Save a YAML file in ~/.routinerun/ (for example, example.yaml):
```yaml
name: Example
description: Three echo commands
steps:
  - name: Step 1
    command:
      - python
      - -c
      - "print('Hello')"
  - name: Step 2
    command:
      - python
      - -c
      - "print('World')"
```

## Usage
1) Show all available pipelines:
```bash
routinerun list
```

2) Start a pipeline by name:
```bash
routinerun run Example
```