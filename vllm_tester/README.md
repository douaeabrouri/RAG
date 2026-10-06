# TaskPilot

A lightweight command-line task manager that keeps your to-do list in a plain JSON file.

![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.2.0-blue)

## Features

- Add, list, complete, and delete tasks from the terminal
- Priorities and due dates
- Data stored locally in a readable JSON file
- No external dependencies

## Installation

Requires Python 3.9 or newer.

```bash
git clone https://github.com/your-username/taskpilot.git
cd taskpilot
pip install .
```

## Usage

```bash
# Add a task
taskpilot add "Write project report" --priority high --due 2026-10-15

# List all tasks
taskpilot list

# Mark a task as done
taskpilot done 3

# Delete a task
taskpilot delete 3
```

Example output:

```
ID  Priority  Due         Task
1   high      2026-10-15  Write project report
2   low       -           Buy groceries
```

## Configuration

TaskPilot reads an optional config file at `~/.taskpilot/config.json`:

| Option          | Default                   | Description                  |
|-----------------|---------------------------|------------------------------|
| `data_file`     | `~/.taskpilot/tasks.json` | Where tasks are stored       |
| `date_format`   | `%Y-%m-%d`                | Format used for due dates    |
| `color_output`  | `true`                    | Enable colored terminal text |

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

Please run the tests before submitting:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Questions or feedback? Open an issue or email maintainer@example.com.
## Installation

Requires Python 3.9 or newer.

```bash
git clone https://github.com/your-username/taskpilot.git
cd taskpilot
pip install .
```

## Usage

```bash
# Add a task
taskpilot add "Write project report" --priority high --due 2026-10-15

# List all tasks
taskpilot list

# Mark a task as done
taskpilot done 3

# Delete a task
taskpilot delete 3
```

Example output:

```
ID  Priority  Due         Task
1   high      2026-10-15  Write project report
2   low       -           Buy groceries
```

## Configuration

TaskPilot reads an optional config file at `~/.taskpilot/config.json`:

| Option          | Default                   | Description                  |
|-----------------|---------------------------|------------------------------|
| `data_file`     | `~/.taskpilot/tasks.json` | Where tasks are stored       |
| `date_format`   | `%Y-%m-%d`                | Format used for due dates    |
| `color_output`  | `true`                    | Enable colored terminal text |

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

Please run the tests before submitting:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Questions or feedback? Open an issue or email maintainer@example.com.