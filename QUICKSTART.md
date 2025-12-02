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

## Command Reference Card

| Command | Purpose |
|---------|---------|
| `today` | Show all tasks & habits due today |
| `next [n]` | Show next 1-3 items to focus on |
| `add <desc>` | Add a task |
| `add daily <desc>` | Add daily habit |
| `add weekly <days> <desc>` | Add weekly habit |
| `done <id>` | Complete task or habit |
| `remove task <id>` | Delete a task |
| `remove habit <id>` | Delete a habit |
| `view tasks` | See all tasks |
| `view habits` | See all habits |
| `edit` | Show edit commands |
| `help` | Show help |
| `quit` | Exit |

## Pro Tips

💡 **Stay Focused**: Use `next 1` to see just one thing to work on at a time

💡 **Quick Complete**: Just type `done 2` instead of `done task 2` - it auto-detects!

💡 **See Everything**: Use `today` at the start of your day to see your full agenda

💡 **View Full Lists**: Use `view tasks` or `view habits` to see complete lists

💡 **Habit Tracking**: Daily habits show every day, weekly habits only on specified days

💡 **Auto-Save**: Everything is saved automatically after each command

## Examples

### Daily Workflow
```
📋 > today                              # Start your day
📋 > next 3                             # See top 3 priorities
📋 > done 1                             # Complete first item
📋 > add New urgent task                # Add something that came up
📋 > next 2                             # Focus on next 2 items
```

### Setting Up Your Life

**Morning routine:**
```
📋 > add daily Morning meditation
📋 > add daily Review daily goals  
📋 > add daily Check emails
```

**Fitness goals:**
```
📋 > add weekly monday,wednesday,friday Gym workout
📋 > add daily 10k steps
📋 > add daily Drink 8 glasses water
```

**Work habits:**
```
📋 > add daily Standup meeting
📋 > add weekly friday Weekly review
📋 > add weekly monday,wednesday Deep work session
```

### Managing Your Day
```
📋 > today                              # See everything due
📋 > next 1                             # Ultra-focused mode
📋 > done 1                             # Complete it
📋 > next 1                             # Get next item
📋 > done habit 2                       # Check off a habit
📋 > view tasks                         # See all tasks
```

Enjoy staying organized! 📝✨
