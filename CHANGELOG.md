# Changelog

## Version 2.0 - Improved UX (2025-12-02)

### New Features

#### 🎯 Focus Mode
- **`next` command**: Shows 1-3 items to focus on right now
  - `next` - Shows next 3 items (default)
  - `next 1` - Ultra-focused mode, shows just 1 item
  - `next 5` - Shows next 5 items (up to 10)
  - Intelligently combines tasks and habits due today
  - Shows helpful tip about remaining items

#### 📅 Today View
- **`today` command**: Shows complete agenda for the day
  - All incomplete tasks
  - All habits due today (not yet completed)
  - Organized by type (tasks vs habits)
  - Shows total count

#### 🔧 Improved Commands
- **Enhanced `add` command**: 
  - `add <description>` - Add task (as before)
  - `add daily <description>` - Add daily habit (new shortcut)
  - `add weekly <days> <description>` - Add weekly habit (new shortcut)
  
- **Unified `done` command**:
  - `done <id>` - Auto-detects whether it's a task or habit
  - `done task <id>` - Explicitly complete a task
  - `done habit <id>` - Explicitly complete a habit
  
- **Unified `remove` command**:
  - `remove task <id>` - Remove a task
  - `remove habit <id>` - Remove a habit

- **New `view` command**:
  - `view tasks` - View all incomplete tasks
  - `view tasks all` - View all tasks including completed
  - `view habits` - View all habits with status

- **New `edit` command**:
  - Shows summary of all editing commands
  - Quick reference for add/remove/view operations

#### 📚 Better Help System
- Improved welcome screen with quick command reference
- Enhanced `help` command with organized sections
- Help text for each command now includes usage examples
- `help <command>` shows detailed help for specific commands

### Improvements
- **Streamlined workflow**: Four main commands (today, next, add, done)
- **Context-aware**: Commands work from any view
- **Better organization**: Commands grouped by purpose
- **Clearer output**: Improved formatting and emoji indicators
- **Backward compatible**: Old commands (list, habits, check) still work as aliases

### User Experience
- **Beginner-friendly**: Clear command structure and help
- **Power-user ready**: Quick shortcuts and auto-detection
- **Focus-oriented**: "next" command helps maintain focus
- **Context switching**: Easy to switch between overview (today) and focus (next) modes

## Version 1.0 - Initial Release

### Features
- Task management (add, complete, remove)
- Habit tracking (daily and weekly)
- Persistent JSON storage
- Interactive CLI with cmd module
- Emoji-enhanced UI
