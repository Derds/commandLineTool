# Quick Start Guide 🚀

## Running the Tool

```bash
cd ../commandLineTool
python3 todo.py
```

## Basic Workflow

### Managing Tasks
```
📋 > add Buy milk
📋 > add Finish report
📋 > list
📋 > done 1
📋 > remove 2
```

### Managing Habits

**Daily habits** (repeat every day):
```
📋 > habit daily Drink 8 glasses of water
📋 > habit daily Exercise for 30 minutes
📋 > habits
📋 > check 1
```

**Weekly habits** (repeat on specific days):
```
📋 > habit weekly monday,friday Team meeting prep
📋 > habit weekly tuesday,thursday Yoga class
📋 > habits
📋 > check 2
```

## Tips

- Use `list all` to see completed tasks
- Habits show "Due Today" or "Not Due" based on the current day
- Daily habits are due every day
- Weekly habits are only due on the days you specify
- Data is automatically saved after each command
- Use `clear` to clear the screen if it gets cluttered
- Press `Ctrl+D` or type `quit` to exit

## Command Reference Card

| Command | Purpose |
|---------|---------|
| `add <task>` | Add new task |
| `list` | Show pending tasks |
| `done <id>` | Complete task |
| `habit daily <desc>` | Add daily habit |
| `habit weekly <days> <desc>` | Add weekly habit |
| `habits` | Show all habits |
| `check <id>` | Complete habit today |
| `quit` | Exit |

## Examples

### Morning Routine Setup
```
📋 > habit daily Morning meditation
📋 > habit daily Review daily goals
📋 > habit daily Check emails
📋 > add Prepare presentation for Monday
```

### Fitness Tracking
```
📋 > habit weekly monday,wednesday,friday Gym workout
📋 > habit weekly tuesday,thursday Yoga
📋 > habit daily 10k steps
📋 > habit daily Drink water reminder
```

### Work Tasks
```
📋 > add Review pull requests
📋 > add Update documentation
📋 > add Respond to client email
📋 > habit daily Standup meeting
📋 > habit weekly friday Weekly report
```

Enjoy staying organized! 📝✨
