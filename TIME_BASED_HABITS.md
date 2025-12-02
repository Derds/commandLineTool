# Time-Based Habits - Version 3.0

## 🎉 What's New

Your todo tool now has **TIME-AWARE HABITS**! Habits can be scheduled for specific times of day, and the `next` command intelligently shows you only what's relevant right now.

## ⏰ Time Periods

Habits can be assigned to one of four time periods:

- **🌅 Morning** (before 1pm) - Breakfast, teeth brushing, morning routines
- **☀️ Afternoon** (11:30am - 5pm) - Lunch, walks, afternoon activities  
- **🌙 Evening** (after 5pm) - Dinner, evening class, bedtime routines
- **⏰ Anytime** - No specific time, always shows up

## 📝 Adding Time-Based Habits

### Daily Habits with Time
```bash
add daily <time> <description>

Examples:
add daily morning Brush teeth
add daily morning Make breakfast
add daily afternoon Eat lunch
add daily afternoon Go for a walk
add daily evening Make dinner
add daily evening Read for 30 minutes
add daily anytime Drink 8 glasses of water
```

### Weekly Habits with Time
```bash
add weekly <days> <time> <description>

Examples:
add weekly monday,wednesday evening Evening yoga class
add weekly tuesday,thursday afternoon Go to gym
add weekly saturday,sunday morning Sleep in and enjoy breakfast
```

## 🎯 Smart "Next" Command

The `next` command now shows items based on current time:

**In the Morning (before 1pm):**
- Shows morning habits
- Shows anytime habits
- Shows all tasks
- Afternoon/evening habits are hidden

**In the Afternoon (11:30am - 5pm):**
- Shows afternoon habits (starts at 11:30am for planning)
- Shows anytime habits
- Shows all tasks
- Morning habits are hidden (already past)
- Evening habits are hidden (not yet time)

**In the Evening (after 5pm):**
- Shows evening habits
- Shows anytime habits
- Shows all tasks  
- Morning/afternoon habits are hidden (already past)

Example:
```
📋 > next

======================================================================
                      NEXT 3 ITEM(S) TO FOCUS ON                      
                              🌙 Evening                               
======================================================================

1. 🔄 [6] Make dinner
   Type: Habit | 🌙 Evening | Daily

2. 📋 [5] Buy groceries
   Type: Task

3. 🔄 [2] Exercise
   Type: Habit | ⏰ Anytime | Daily

======================================================================
```

## 📅 Today View

The `today` command still shows EVERYTHING due today, regardless of time.
Each habit displays its time period with an emoji:

```
📋 > today

======================================================================
                            TODAY'S AGENDA                            
======================================================================

🔄 HABITS:
  [4] Brush teeth
       🌅 Morning | Daily
  [5] Go for a walk
       ☀️ Afternoon | Daily
  [6] Make dinner
       🌙 Evening | Daily
  [7] Evening class
       🌙 Evening | Weekly (Monday, Wednesday)

======================================================================
```

## 🏗️ Code Structure

The code has been refactored into modules for better organization:

```
commandLineTool/
├── todo.py                 # Main entry point (simple!)
├── src/
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Task, Habit, TimeOfDay models
│   ├── manager.py         # TodoManager (data & business logic)
│   └── cli.py             # TodoCLI (command-line interface)
├── todo_data.json         # Your data (migrated automatically)
└── README.md              # Documentation
```

### Benefits:
- ✅ Easier to maintain and extend
- ✅ Cleaner separation of concerns
- ✅ Still runs with simple `python3 todo.py`
- ✅ Can import modules for testing/extending

## 🔄 Data Migration

Your existing habits were automatically migrated!
- Old habits without time_of_day → set to "anytime"
- All your completions and data are preserved
- The migration happens automatically on first run

## ⚙️ How It Works

**Time Detection:**
- Uses system time to determine current period
- Morning check: hour < 13
- Afternoon check: hour >= 11:30 and hour < 17
- Evening check: hour >= 17

**Afternoon Planning:**
- Afternoon habits start showing at 11:30am
- This lets you plan your afternoon during late morning

**Smart Filtering:**
- `next` filters by time relevance
- `today` shows everything
- Completed habits are hidden from both views

## 🎮 Usage Examples

### Morning Routine (8am)
```
📋 > next 2
Shows: Morning habits + tasks

📋 > add daily morning Meditate for 10 minutes
📋 > done habit 4
📋 > next 1
```

### Afternoon Planning (11:45am)
```
📋 > next
Shows: Afternoon habits starting to appear!

📋 > add daily afternoon Take vitamins
```

### Evening Wind-down (7pm)
```
📋 > next
Shows: Evening habits + remaining tasks

📋 > add weekly monday,wednesday,friday evening Prepare tomorrow's lunch
```

## 🚀 Next Steps

TODO (not yet implemented):
1. Add `view habits` command with time filter
2. Add `update habit <id> time <time>` to change time periods
3. Add remaining commands (remove, edit, help)
4. Update documentation fully

The core time-based system is working! Test it by adding habits at different times and seeing how `next` adapts throughout the day.
