# Todo List Command Line Tool 📝

A simple and powerful terminal-based todo list manager with support for tasks and habits.

## Features

- ✅ **Tasks**: One-time todos that you can add, complete, and remove
- 🔄 **Habits**: Recurring tasks that repeat daily or on specific weekdays
- 💾 **Persistent Storage**: All data saved automatically to JSON file
- 🎨 **Clean Interface**: Easy-to-read terminal UI with emojis
- 🚀 **Extensible**: Built with future API integrations in mind

## Installation

No installation required! Just Python 3.6+

## Usage

### Starting the Tool

```bash
python3 todo.py
```

Or run directly (after making it executable):
```bash
./todo.py
```

### Available Commands

#### Task Management

| Command | Description | Example |
|---------|-------------|---------|
| `add <description>` | Add a new task | `add Buy groceries` |
| `list` | Show incomplete tasks | `list` |
| `list all` | Show all tasks (including completed) | `list all` |
| `done <id>` | Mark task as completed | `done 1` |
| `remove <id>` | Remove a task | `remove 1` |

#### Habit Management

| Command | Description | Example |
|---------|-------------|---------|
| `habit daily <description>` | Add a daily habit | `habit daily Drink 8 glasses of water` |
| `habit weekly <days> <description>` | Add a weekly habit | `habit weekly monday,wednesday,friday Go to gym` |
| `habits` | List all habits with status | `habits` |
| `check <id>` | Mark habit as completed for today | `check 1` |
| `remove_habit <id>` | Remove a habit | `remove_habit 1` |

#### General Commands

| Command | Description |
|---------|-------------|
| `clear` | Clear the screen |
| `help` | Show available commands |
| `quit` or `q` | Exit the application |

## Example Session

```
📋 > add Buy milk
✅ Task added with ID: 1

📋 > add Call dentist
✅ Task added with ID: 2

📋 > list
============================================================
ID    Status     Task                                    
============================================================
1     ○ Todo     Buy milk                                
2     ○ Todo     Call dentist                            
============================================================

📋 > habit daily Morning meditation
✅ Daily habit added with ID: 1

📋 > habit weekly monday,wednesday,friday Workout
✅ Weekly habit added with ID: 2 (Days: Monday, Wednesday, Friday)

📋 > habits
================================================================================
ID    Status          Frequency       Habit                         
================================================================================
1     ○ Due Today     Daily           Morning meditation            
2     ○ Due Today     Weekly (Monday, Wednesday, Friday) Workout                        
================================================================================

📋 > check 1
✅ Habit 1 checked off for today!

📋 > done 1
✅ Task 1 marked as completed!

📋 > quit
👋 Goodbye! Stay productive!
```

## Data Storage

All your tasks and habits are stored in `todo_data.json` in the same directory as the script. The file is created automatically on first use.

## Future Extensions

This tool is designed to be easily extensible. Planned features include:

- 🌤️ Weather API integration
- 📊 Statistics and streak tracking
- 🏆 Achievement system
- 📅 Calendar view
- ⏰ Reminders and notifications
- 📤 Export to various formats

## Technical Details

- **Language**: Python 3
- **Libraries**: Built-in Python modules only (cmd, json, os, datetime)
- **Storage**: JSON file format
- **Architecture**: Modular design with TodoManager (business logic) and TodoCLI (interface)

## Contributing

Feel free to extend this tool with new features! The code is organized to make adding new commands and functionality straightforward.
