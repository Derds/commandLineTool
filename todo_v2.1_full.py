#!/usr/bin/env python3
"""
Todo List Command Line Tool
A simple CLI tool for managing tasks and habits
"""

import cmd
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class TodoManager:
    """Manages tasks and habits with persistence"""
    
    def __init__(self, data_file='todo_data.json'):
        self.data_file = data_file
        self.tasks = []
        self.habits = []
        self.load_data()
    
    def load_data(self):
        """Load tasks and habits from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.habits = data.get('habits', [])
            except Exception as e:
                print(f"Error loading data: {e}")
                self.tasks = []
                self.habits = []
        else:
            self.tasks = []
            self.habits = []
    
    def save_data(self):
        """Save tasks and habits to JSON file"""
        try:
            data = {
                'tasks': self.tasks,
                'habits': self.habits
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_task(self, description: str) -> int:
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_data()
        return task['id']
    
    def add_habit(self, description: str, frequency: str, days: Optional[List[str]] = None) -> int:
        """Add a new habit with daily or weekly frequency"""
        habit = {
            'id': len(self.habits) + 1,
            'description': description,
            'frequency': frequency,  # 'daily' or 'weekly'
            'days': days or [],  # For weekly: ['monday', 'wednesday', etc.]
            'created_at': datetime.now().isoformat(),
            'completions': []  # List of completion dates
        }
        self.habits.append(habit)
        self.save_data()
        return habit['id']
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def remove_task(self, task_id: int) -> bool:
        """Remove a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(i)
                self.save_data()
                return True
        return False
    
    def complete_habit_today(self, habit_id: int) -> bool:
        """Mark a habit as completed for today"""
        for habit in self.habits:
            if habit['id'] == habit_id:
                today = datetime.now().date().isoformat()
                if today not in habit['completions']:
                    habit['completions'].append(today)
                    self.save_data()
                    return True
        return False
    
    def remove_habit(self, habit_id: int) -> bool:
        """Remove a habit"""
        for i, habit in enumerate(self.habits):
            if habit['id'] == habit_id:
                self.habits.pop(i)
                self.save_data()
                return True
        return False
    
    def update_task(self, task_id: int, new_description: str) -> bool:
        """Update a task's description"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updated_at'] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def update_habit(self, habit_id: int, new_description: str = None, 
                     new_frequency: str = None, new_days: List[str] = None) -> bool:
        """Update a habit's description, frequency, or days"""
        for habit in self.habits:
            if habit['id'] == habit_id:
                if new_description:
                    habit['description'] = new_description
                if new_frequency:
                    habit['frequency'] = new_frequency
                if new_days is not None:
                    habit['days'] = new_days
                habit['updated_at'] = datetime.now().isoformat()
                self.save_data()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_habit(self, habit_id: int) -> Optional[Dict]:
        """Get a specific habit by ID"""
        for habit in self.habits:
            if habit['id'] == habit_id:
                return habit
        return None
    
    def get_tasks(self, show_completed=False) -> List[Dict]:
        """Get all tasks, optionally filtering out completed ones"""
        if show_completed:
            return self.tasks
        return [t for t in self.tasks if not t['completed']]
    
    def get_habits(self) -> List[Dict]:
        """Get all habits with today's completion status"""
        today = datetime.now().date().isoformat()
        today_weekday = datetime.now().strftime('%A').lower()
        
        habits_with_status = []
        for habit in self.habits:
            habit_copy = habit.copy()
            habit_copy['completed_today'] = today in habit['completions']
            
            # Check if habit is due today
            if habit['frequency'] == 'daily':
                habit_copy['due_today'] = True
            elif habit['frequency'] == 'weekly':
                habit_copy['due_today'] = today_weekday in [d.lower() for d in habit['days']]
            else:
                habit_copy['due_today'] = False
                
            habits_with_status.append(habit_copy)
        
        return habits_with_status


class TodoCLI(cmd.Cmd):
    """Interactive command-line interface for todo list"""
    
    intro = """
╔════════════════════════════════════════╗
║     📝 TODO LIST MANAGER 📝           ║
║  Manage your tasks and habits easily   ║
╚════════════════════════════════════════╝

Quick Commands:
  today  - Show all tasks & habits due today
  next   - Show next 1-3 items to focus on
  add    - Add a new task or habit
  done   - Mark item as complete
  help   - Show detailed help

Type 'quit' or 'q' to exit.
"""
    prompt = '📋 > '
    
    def __init__(self):
        super().__init__()
        self.manager = TodoManager()
    
    def _get_today_items(self):
        """Get all tasks and habits due today"""
        tasks = self.manager.get_tasks(show_completed=False)
        habits = self.manager.get_habits()
        
        # Filter habits to only those due today and not completed
        habits_due = [h for h in habits if h['due_today'] and not h['completed_today']]
        
        # Combine and return
        items = []
        for task in tasks:
            items.append({
                'type': 'task',
                'id': task['id'],
                'description': task['description'],
                'created_at': task.get('created_at', '')
            })
        
        for habit in habits_due:
            items.append({
                'type': 'habit',
                'id': habit['id'],
                'description': habit['description'],
                'frequency': habit['frequency'],
                'days': habit.get('days', [])
            })
        
        return items
    
    # Main View Commands
    def do_today(self, line):
        """Show all tasks and habits due today
        Usage: today
        
        From this view you can:
        - Type 'add <description>' to add a task
        - Type 'done task <id>' or 'done habit <id>' to complete
        - Type 'remove task <id>' or 'remove habit <id>' to delete"""
        items = self._get_today_items()
        
        if not items:
            print("\n🎉 Great! You have nothing due today!\n")
            return
        
        print("\n" + "="*70)
        print("TODAY'S AGENDA".center(70))
        print("="*70)
        
        # Group by type
        tasks = [i for i in items if i['type'] == 'task']
        habits = [i for i in items if i['type'] == 'habit']
        
        if tasks:
            print("\n📋 TASKS:")
            for item in tasks:
                print(f"  [{item['id']}] {item['description']}")
        
        if habits:
            print("\n🔄 HABITS:")
            for item in habits:
                freq_info = item['frequency'].capitalize()
                if item['frequency'] == 'weekly':
                    freq_info += f" ({', '.join(item['days'])})"
                print(f"  [{item['id']}] {item['description']} - {freq_info}")
        
        print("\n" + "="*70)
        print(f"Total: {len(tasks)} task(s), {len(habits)} habit(s)")
        print("="*70 + "\n")
    
    def do_next(self, line):
        """Show next 1-3 items to focus on
        Usage: next [number]
        
        Shows up to 3 items (or specify number). You can:
        - Type 'add <description>' to add a task
        - Type 'done task <id>' or 'done habit <id>' to complete
        - Type 'remove task <id>' or 'remove habit <id>' to delete
        
        Example: next 2 (shows next 2 items)"""
        
        # Parse number of items to show
        try:
            max_items = int(line.strip()) if line.strip() else 3
            max_items = min(max(1, max_items), 10)  # Clamp between 1-10
        except ValueError:
            max_items = 3
        
        items = self._get_today_items()
        
        if not items:
            print("\n🎉 Nothing to do! You're all caught up!\n")
            return
        
        # Show only the first N items
        next_items = items[:max_items]
        
        print("\n" + "="*70)
        print(f"NEXT {len(next_items)} ITEM(S) TO FOCUS ON".center(70))
        print("="*70 + "\n")
        
        for i, item in enumerate(next_items, 1):
            icon = "📋" if item['type'] == 'task' else "🔄"
            type_label = "Task" if item['type'] == 'task' else "Habit"
            
            if item['type'] == 'habit':
                freq_info = item['frequency'].capitalize()
                if item['frequency'] == 'weekly':
                    freq_info += f" ({', '.join(item['days'])})"
                print(f"{i}. {icon} [{item['id']}] {item['description']}")
                print(f"   Type: {type_label} - {freq_info}\n")
            else:
                print(f"{i}. {icon} [{item['id']}] {item['description']}")
                print(f"   Type: {type_label}\n")
        
        print("="*70 + "\n")
        
        if len(items) > max_items:
            remaining = len(items) - max_items
            print(f"💡 Tip: You have {remaining} more item(s). Type 'today' to see all.\n")
    
    # Quick Add/Complete/Remove Commands
    def do_add(self, line):
        """Add a new task or habit
        Usage: 
          add <task description>          - Add a task
          add daily <habit description>   - Add daily habit
          add weekly <days> <description> - Add weekly habit
        
        Examples:
          add Buy groceries
          add daily Drink water
          add weekly monday,friday Exercise"""
        
        if not line:
            print("❌ Please provide a description")
            return
        
        parts = line.strip().split(maxsplit=2)
        
        # Check if it's a habit
        if parts[0].lower() == 'daily':
            if len(parts) < 2:
                print("❌ Usage: add daily <description>")
                return
            description = ' '.join(parts[1:])
            habit_id = self.manager.add_habit(description, 'daily')
            print(f"✅ Daily habit added with ID: {habit_id}")
        
        elif parts[0].lower() == 'weekly':
            if len(parts) < 3:
                print("❌ Usage: add weekly <days> <description>")
                print("   Example: add weekly monday,wednesday,friday Go to gym")
                return
            
            days_str = parts[1]
            description = parts[2]
            days = [d.strip().capitalize() for d in days_str.split(',')]
            
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            invalid_days = [d for d in days if d not in valid_days]
            
            if invalid_days:
                print(f"❌ Invalid days: {', '.join(invalid_days)}")
                return
            
            habit_id = self.manager.add_habit(description, 'weekly', days)
            print(f"✅ Weekly habit added with ID: {habit_id}")
        
        else:
            # It's a regular task
            task_id = self.manager.add_task(line)
            print(f"✅ Task added with ID: {task_id}")
    
    def do_view(self, line):
        """View full lists of tasks and habits
        Usage: 
          view tasks [all]  - View all incomplete tasks (or all tasks)
          view habits       - View all habits
        
        Examples:
          view tasks
          view tasks all
          view habits"""
        
        parts = line.strip().lower().split()
        
        if not parts or parts[0] == 'tasks':
            show_all = len(parts) > 1 and parts[1] == 'all'
            tasks = self.manager.get_tasks(show_completed=show_all)
            
            if not tasks:
                print("📭 No tasks found\n")
                return
            
            print("\n" + "="*70)
            print("ALL TASKS".center(70))
            print("="*70)
            print(f"{'ID':<5} {'Status':<12} {'Task':<50}")
            print("="*70)
            
            for task in tasks:
                status = "✓ Done" if task['completed'] else "○ Pending"
                print(f"{task['id']:<5} {status:<12} {task['description']:<50}")
            
            print("="*70 + "\n")
        
        elif parts[0] == 'habits':
            habits = self.manager.get_habits()
            
            if not habits:
                print("📭 No habits found\n")
                return
            
            print("\n" + "="*80)
            print("ALL HABITS".center(80))
            print("="*80)
            print(f"{'ID':<5} {'Status':<15} {'Frequency':<20} {'Habit':<35}")
            print("="*80)
            
            for habit in habits:
                if habit['due_today']:
                    status = "✓ Done Today" if habit['completed_today'] else "○ Due Today"
                else:
                    status = "— Not Due"
                
                freq_info = habit['frequency'].capitalize()
                if habit['frequency'] == 'weekly':
                    days_str = ', '.join(habit['days'])
                    freq_info += f" ({days_str})"
                
                print(f"{habit['id']:<5} {status:<15} {freq_info:<20} {habit['description']:<35}")
            
            print("="*80 + "\n")
        
        else:
            print("❌ Usage: view tasks [all] | view habits")
    
    def do_done(self, line):
        """Mark a task or habit as completed
        Usage: 
          done task <id>   - Mark task as completed
          done habit <id>  - Mark habit as completed for today
          done <id>        - Auto-detect type (tries task first)
        
        Examples:
          done task 1
          done habit 2
          done 3"""
        
        parts = line.strip().split()
        
        if not parts:
            print("❌ Usage: done task <id> | done habit <id> | done <id>")
            return
        
        try:
            if len(parts) == 2:
                # Explicit type specified
                item_type = parts[0].lower()
                item_id = int(parts[1])
                
                if item_type == 'task':
                    if self.manager.complete_task(item_id):
                        print(f"✅ Task {item_id} marked as completed!")
                    else:
                        print(f"❌ Task {item_id} not found")
                
                elif item_type == 'habit':
                    if self.manager.complete_habit_today(item_id):
                        print(f"✅ Habit {item_id} checked off for today!")
                    else:
                        print(f"❌ Habit {item_id} not found or already completed")
                
                else:
                    print("❌ Type must be 'task' or 'habit'")
            
            else:
                # Try to auto-detect
                item_id = int(parts[0])
                
                # Try task first
                if self.manager.complete_task(item_id):
                    print(f"✅ Task {item_id} marked as completed!")
                # Then try habit
                elif self.manager.complete_habit_today(item_id):
                    print(f"✅ Habit {item_id} checked off for today!")
                else:
                    print(f"❌ Item {item_id} not found")
                    print("💡 Tip: Use 'done task <id>' or 'done habit <id>' to be specific")
        
        except ValueError:
            print("❌ Please provide a valid ID (number)")
    
    def do_remove(self, line):
        """Remove a task or habit
        Usage: 
          remove task <id>   - Remove a task
          remove habit <id>  - Remove a habit
        
        Examples:
          remove task 1
          remove habit 2"""
        
        parts = line.strip().split()
        
        if len(parts) != 2:
            print("❌ Usage: remove task <id> | remove habit <id>")
            return
        
        try:
            item_type = parts[0].lower()
            item_id = int(parts[1])
            
            if item_type == 'task':
                if self.manager.remove_task(item_id):
                    print(f"🗑️  Task {item_id} removed")
                else:
                    print(f"❌ Task {item_id} not found")
            
            elif item_type == 'habit':
                if self.manager.remove_habit(item_id):
                    print(f"🗑️  Habit {item_id} removed")
                else:
                    print(f"❌ Habit {item_id} not found")
            
            else:
                print("❌ Type must be 'task' or 'habit'")
        
        except ValueError:
            print("❌ Please provide a valid ID (number)")
    
    def do_update(self, line):
        """Update/edit a task or habit
        Usage:
          update task <id> <new description>       - Update task description
          update habit <id> desc <new description> - Update habit description
          update habit <id> days <new days>        - Update weekly habit days
          update habit <id> freq <daily|weekly>    - Update habit frequency
        
        Examples:
          update task 1 Buy milk and bread
          update habit 2 desc Exercise for 45 minutes
          update habit 2 days monday,wednesday,friday
          update habit 3 freq daily"""
        
        parts = line.strip().split(maxsplit=2)
        
        if len(parts) < 3:
            print("❌ Usage: update task <id> <description> | update habit <id> <field> <value>")
            return
        
        try:
            item_type = parts[0].lower()
            item_id = int(parts[1])
            
            if item_type == 'task':
                # update task <id> <new description>
                if len(parts) < 3:
                    print("❌ Usage: update task <id> <new description>")
                    return
                
                # Everything after the ID is the new description
                new_description = parts[2]
                task = self.manager.get_task(item_id)
                
                if not task:
                    print(f"❌ Task {item_id} not found")
                    return
                
                print(f"\n📝 Current: {task['description']}")
                print(f"   New:     {new_description}\n")
                
                if self.manager.update_task(item_id, new_description):
                    print(f"✅ Task {item_id} updated!")
                else:
                    print(f"❌ Failed to update task {item_id}")
            
            elif item_type == 'habit':
                # update habit <id> <field> <value>
                if len(parts) < 3:
                    print("❌ Usage: update habit <id> <field> <value>")
                    print("   Fields: desc, days, freq")
                    return
                
                # Split the third part to get field and value
                field_and_value = parts[2].split(maxsplit=1)
                if len(field_and_value) < 2:
                    print("❌ Usage: update habit <id> <field> <value>")
                    return
                
                field = field_and_value[0].lower()
                value = field_and_value[1]
                
                habit = self.manager.get_habit(item_id)
                
                if not habit:
                    print(f"❌ Habit {item_id} not found")
                    return
                
                if field == 'desc' or field == 'description':
                    print(f"\n📝 Current: {habit['description']}")
                    print(f"   New:     {value}\n")
                    
                    if self.manager.update_habit(item_id, new_description=value):
                        print(f"✅ Habit {item_id} description updated!")
                    else:
                        print(f"❌ Failed to update habit")
                
                elif field == 'days':
                    if habit['frequency'] != 'weekly':
                        print(f"❌ Can only set days for weekly habits (this is {habit['frequency']})")
                        return
                    
                    days = [d.strip().capitalize() for d in value.split(',')]
                    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    invalid_days = [d for d in days if d not in valid_days]
                    
                    if invalid_days:
                        print(f"❌ Invalid days: {', '.join(invalid_days)}")
                        return
                    
                    print(f"\n📝 Current days: {', '.join(habit['days'])}")
                    print(f"   New days:     {', '.join(days)}\n")
                    
                    if self.manager.update_habit(item_id, new_days=days):
                        print(f"✅ Habit {item_id} days updated!")
                    else:
                        print(f"❌ Failed to update habit")
                
                elif field == 'freq' or field == 'frequency':
                    if value.lower() not in ['daily', 'weekly']:
                        print("❌ Frequency must be 'daily' or 'weekly'")
                        return
                    
                    print(f"\n📝 Current frequency: {habit['frequency']}")
                    print(f"   New frequency:     {value.lower()}\n")
                    
                    # Clear days if switching to daily
                    new_days = [] if value.lower() == 'daily' else habit.get('days', [])
                    
                    if self.manager.update_habit(item_id, new_frequency=value.lower(), new_days=new_days):
                        print(f"✅ Habit {item_id} frequency updated!")
                        if value.lower() == 'daily':
                            print("   Note: Cleared weekly days (now daily)")
                    else:
                        print(f"❌ Failed to update habit")
                
                else:
                    print(f"❌ Unknown field '{field}'. Use: desc, days, or freq")
            
            else:
                print("❌ Type must be 'task' or 'habit'")
        
        except ValueError:
            print("❌ Please provide a valid ID (number)")
        except IndexError:
            print("❌ Invalid command format")
    
    # Edit menu - for organizing commands
    def do_edit(self, line):
        """Enter edit mode to manage tasks and habits
        Usage: edit
        
        In edit mode you can:
        - Add tasks and habits
        - Update/edit tasks and habits
        - Remove tasks and habits
        - View complete lists
        
        This is just a reminder of available commands.
        You can use these commands directly anytime:
        - add <description>
        - update task <id> / update habit <id>
        - remove task <id> / remove habit <id>
        - view tasks / view habits"""
        
        print("\n" + "="*70)
        print("EDIT MODE - Available Commands".center(70))
        print("="*70)
        print("\n📝 Adding:")
        print("  add <description>                    - Add a task")
        print("  add daily <description>              - Add daily habit")
        print("  add weekly <days> <description>      - Add weekly habit")
        print("\n✏️  Updating:")
        print("  update task <id> <new description>   - Update task")
        print("  update habit <id> desc <description> - Update habit description")
        print("  update habit <id> days <days>        - Update habit days")
        print("  update habit <id> freq <daily|weekly> - Update frequency")
        print("\n🗑️  Removing:")
        print("  remove task <id>                     - Delete a task")
        print("  remove habit <id>                    - Delete a habit")
        print("\n👀 Viewing:")
        print("  view tasks [all]                     - View all tasks")
        print("  view habits                          - View all habits")
        print("\n" + "="*70 + "\n")
    
    # Legacy/Alias Commands (for backward compatibility)
    def do_list(self, line):
        """Alias for 'view tasks' - List all tasks"""
        self.do_view(f"tasks {line}")
    
    def do_habits(self, line):
        """Alias for 'view habits' - List all habits"""
        self.do_view("habits")
    
    def do_check(self, line):
        """Alias for 'done habit' - Mark habit as completed
        Usage: check <habit_id>"""
        if line.strip():
            self.do_done(f"habit {line}")
        else:
            print("❌ Usage: check <habit_id>")
    
    # General Commands
    def do_clear(self, line):
        """Clear the screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def do_help(self, line):
        """Show help information
        Usage: help [command]
        
        Main Commands:
          today  - Show all tasks & habits due today
          next   - Show next 1-3 items to focus on
          add    - Add a new task or habit
          done   - Mark item as complete
          remove - Remove a task or habit
          view   - View full lists
          edit   - Show edit mode commands
        
        Type 'help <command>' for detailed info on a specific command."""
        
        if not line:
            print("\n" + "="*70)
            print("📋 TODO LIST MANAGER - HELP".center(70))
            print("="*70)
            print("\n🎯 MAIN COMMANDS:")
            print("  today          - Show all tasks & habits due today")
            print("  next [n]       - Show next 1-3 items (or specify number)")
            print("  add            - Add a new task or habit")
            print("  done           - Mark a task or habit as complete")
            print("  remove         - Remove a task or habit")
            print("  view           - View complete lists of tasks/habits")
            print("  edit           - Show available edit commands")
            print("\n💡 QUICK TIPS:")
            print("  - Use 'today' to see everything due today")
            print("  - Use 'next' to focus on 1-3 items at a time")
            print("  - Add tasks quickly: 'add Buy milk'")
            print("  - Complete items: 'done 1' or 'done task 1'")
            print("  - Type 'help <command>' for detailed usage")
            print("\n🔧 OTHER COMMANDS:")
            print("  clear          - Clear the screen")
            print("  quit, q        - Exit the application")
            print("\n" + "="*70 + "\n")
        else:
            # Show help for specific command
            cmd.Cmd.do_help(self, line)
    
    def do_quit(self, line):
        """Exit the application"""
        print("\n👋 Goodbye! Stay productive!\n")
        return True
    
    def do_q(self, line):
        """Exit the application (shortcut)"""
        return self.do_quit(line)
    
    def do_EOF(self, line):
        """Exit on Ctrl+D"""
        print()
        return True


if __name__ == '__main__':
    TodoCLI().cmdloop()
