# Todo List Command Line Tool 📝

A simple and powerful terminal-based todo list manager with support for tasks and habits.

## Features

- ✅ **Tasks**: One-time todos that you can add, complete, and remove
- 🔄 **Habits**: Recurring tasks that repeat daily or on specific weekdays
- 🎯 **Focus Mode**: "Next" view shows 1-3 items to focus on right now
- 📅 **Today View**: See all tasks and habits due today in one place
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

### Main Commands

The tool is organized around 4 main workflows:

#### 📅 Today - See everything due today
```bash
today          # Show all tasks and habits due today
```

#### 🎯 Next - Focus on 1-3 items
```bash
next           # Show next 3 items to focus on
next 1         # Show just 1 item
next 5         # Show next 5 items
```

#### ➕ Add - Create tasks and habits
```bash
add <description>                    # Add a task
add daily <description>              # Add daily habit
add weekly <days> <description>      # Add weekly habit
```

#### ✅ Done - Complete items
```bash
done <id>                # Auto-detect and complete task or habit
done task <id>           # Complete a specific task
done habit <id>          # Check off a habit for today
```

#### 🗑️ Remove - Delete items
```bash
remove task <id>         # Remove a task
remove habit <id>        # Remove a habit
```

#### 👀 View - See complete lists
```bash
view tasks              # View all incomplete tasks
view tasks all          # View all tasks including completed
view habits             # View all habits with status
```

#### 🔧 Other Commands
```bash
edit                    # Show edit mode commands
help                    # Show detailed help
help <command>          # Get help for specific command
clear                   # Clear the screen
quit, q                 # Exit the application
```

## Example Session

```
📋 > add Buy milk
✅ Task added with ID: 1

📋 > add Call dentist
✅ Task added with ID: 2

📋 > add daily Morning meditation
✅ Daily habit added with ID: 1

📋 > add weekly monday,friday Workout
✅ Weekly habit added with ID: 2 (Days: Monday, Friday)

📋 > today
======================================================================
                            TODAY'S AGENDA                            
======================================================================

📋 TASKS:
  [1] Buy milk
  [2] Call dentist

🔄 HABITS:
  [1] Morning meditation - Daily
  [2] Workout - Weekly (Monday, Friday)

======================================================================
Total: 2 task(s), 2 habit(s)
======================================================================

📋 > next 2
======================================================================
                      NEXT 2 ITEM(S) TO FOCUS ON                      
======================================================================

1. 📋 [1] Buy milk
   Type: Task

2. 📋 [2] Call dentist
   Type: Task

======================================================================

💡 Tip: You have 2 more item(s). Type 'today' to see all.

📋 > done 1
✅ Task 1 marked as completed!

📋 > done habit 1
✅ Habit 1 checked off for today!

📋 > next
======================================================================
                      NEXT 1 ITEM(S) TO FOCUS ON                      
======================================================================

1. 📋 [2] Call dentist
   Type: Task

======================================================================

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
