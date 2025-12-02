# Quick Start Guide 🚀

## Running the Tool

```bash
cd /Users/dervla.obrien/Documents/personal-projects/commandLineTool
python3 todo.py
```

## The 4 Main Commands

### 1. 📅 TODAY - See what's on your plate
```
📋 > today
```
Shows all tasks and habits due today in one organized view.

### 2. 🎯 NEXT - Focus on what matters
```
📋 > next           # Shows next 3 items
📋 > next 1         # Shows just 1 item to focus on
```
Perfect for staying focused! Shows only your next 1-3 items.

### 3. ➕ ADD - Create items quickly
```
📋 > add Buy milk
📋 > add daily Exercise
📋 > add weekly monday,friday Team meeting
```

### 4. ✅ DONE - Complete items
```
📋 > done 1              # Complete task or habit
📋 > done task 1         # Specify it's a task
📋 > done habit 2        # Specify it's a habit
```

## Quick Workflow Examples

### Morning Routine
```
📋 > today                              # See what's on your plate
📋 > next 1                             # Focus on first item
📋 > done 1                             # Check it off
📋 > next 1                             # Get next item
```

### Adding Tasks
```
📋 > add Buy groceries
📋 > add Call dentist
📋 > add Finish report
📋 > today                              # See all your tasks
```

### Setting Up Habits

**Daily habits** (repeat every day):
```
📋 > add daily Drink 8 glasses of water
📋 > add daily Exercise for 30 minutes
📋 > add daily Review daily goals
```

**Weekly habits** (repeat on specific days):
```
📋 > add weekly monday,wednesday,friday Gym workout
📋 > add weekly tuesday,thursday Yoga class
📋 > add weekly friday Weekly review
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
| `update task <id> <desc>` | Edit task description |
| `update habit <id> desc <desc>` | Edit habit description |
| `update habit <id> days <days>` | Edit habit days |
| `update habit <id> freq <freq>` | Change habit frequency |
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

💡 **Editing Made Easy**: Fix typos or change habits without deleting and recreating

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
