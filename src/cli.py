"""
Command-line interface for todo list manager
"""

import cmd
import os
from datetime import datetime

from .manager import TodoManager
from .models import TimeOfDay, get_current_time_of_day, format_time_of_day


class TodoCLI(cmd.Cmd):
    """Interactive command-line interface for todo list"""
    
    intro = """
╔════════════════════════════════════════╗
║     📝 TODO LIST MANAGER 📝           ║
║  Manage your tasks and habits easily   ║
╚════════════════════════════════════════╝

Quick Commands:
  today  - Show all tasks & habits due today
  next   - Show next 1-3 items to focus on (time-aware!)
  add    - Add a new task or habit
  done   - Mark item as complete
  help   - Show detailed help

Type 'quit' or 'q' to exit.
"""
    prompt = '📋 > '
    
    def __init__(self):
        super().__init__()
        self.manager = TodoManager()
    
    def _get_today_items(self, time_filtered=False):
        """Get all tasks and habits due today, optionally filtered by time"""
        tasks = self.manager.get_tasks(show_completed=False)
        
        if time_filtered:
            habits = self.manager.get_relevant_habits_now()
        else:
            # Get all habits due today
            today_weekday = datetime.now().strftime('%A').lower()
            today = datetime.now().date().isoformat()
            all_habits = self.manager.get_habits()
            habits = [h for h in all_habits if h.is_due_today(today_weekday) and not h.is_completed_today(today)]
        
        # Combine into items
        items = []
        for task in tasks:
            items.append({
                'type': 'task',
                'id': task['id'],
                'description': task['description'],
                'created_at': task.get('created_at', '')
            })
        
        for habit in habits:
            items.append({
                'type': 'habit',
                'id': habit.id,
                'description': habit.description,
                'frequency': habit.frequency,
                'days': habit.days,
                'time_of_day': habit.time_of_day
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
        items = self._get_today_items(time_filtered=False)
        
        if not items:
            print("\n🎉 Great! You have nothing due today!\n")
            return
        
        # Get current time for display
        current_time = get_current_time_of_day()
        
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
                time_display = format_time_of_day(item['time_of_day'])
                freq_info = item['frequency'].capitalize()
                if item['frequency'] == 'weekly':
                    freq_info += f" ({', '.join(item['days'])})"
                print(f"  [{item['id']}] {item['description']}")
                print(f"       {time_display} | {freq_info}")
        
        print("\n" + "="*70)
        print(f"Total: {len(tasks)} task(s), {len(habits)} habit(s)")
        print("="*70 + "\n")
    
    def do_next(self, line):
        """Show next 1-3 items to focus on (time-aware!)
        Usage: next [number]
        
        Shows items relevant to current time of day:
        - Morning (before 1pm): morning & anytime items
        - Afternoon (11:30am-5pm): afternoon & anytime items
        - Evening (after 5pm): evening & anytime items
        
        You can:
        - Type 'add <description>' to add a task
        - Type 'done task <id>' or 'done habit <id>' to complete
        
        Example: next 2 (shows next 2 items)"""
        
        # Parse number of items to show
        try:
            max_items = int(line.strip()) if line.strip() else 3
            max_items = min(max(1, max_items), 10)
        except ValueError:
            max_items = 3
        
        items = self._get_today_items(time_filtered=True)
        
        if not items:
            current_time = get_current_time_of_day()
            time_name = current_time.value.capitalize()
            print(f"\n🎉 Nothing to do right now! (Current time: {format_time_of_day(current_time.value)})")
            print("💡 Tip: Use 'today' to see your full agenda\n")
            return
        
        # Show only the first N items
        next_items = items[:max_items]
        
        current_time = get_current_time_of_day()
        print("\n" + "="*70)
        print(f"NEXT {len(next_items)} ITEM(S) TO FOCUS ON".center(70))
        print(f"{format_time_of_day(current_time.value)}".center(70))
        print("="*70 + "\n")
        
        for i, item in enumerate(next_items, 1):
            icon = "📋" if item['type'] == 'task' else "🔄"
            type_label = "Task" if item['type'] == 'task' else "Habit"
            
            if item['type'] == 'habit':
                time_display = format_time_of_day(item['time_of_day'])
                freq_info = item['frequency'].capitalize()
                if item['frequency'] == 'weekly':
                    freq_info += f" ({', '.join(item['days'])})"
                print(f"{i}. {icon} [{item['id']}] {item['description']}")
                print(f"   Type: {type_label} | {time_display} | {freq_info}\n")
            else:
                print(f"{i}. {icon} [{item['id']}] {item['description']}")
                print(f"   Type: {type_label}\n")
        
        print("="*70 + "\n")
        
        if len(items) > max_items:
            remaining = len(items) - max_items
            print(f"💡 Tip: You have {remaining} more item(s) for now. Type 'today' to see all.\n")
    
    # Quick Add/Complete/Remove Commands  
    def do_add(self, line):
        """Add a new task or habit
        Usage: 
          add <task description>                              - Add a task
          add daily <time> <habit description>                - Add daily habit
          add weekly <days> <time> <description>              - Add weekly habit
        
        Time options: morning, afternoon, evening, anytime
        
        Examples:
          add Buy groceries
          add daily morning Brush teeth
          add daily evening Make dinner
          add weekly monday,friday afternoon Go to gym"""
        
        if not line:
            print("❌ Please provide a description")
            return
        
        parts = line.strip().split(maxsplit=3)
        
        # Check if it's a habit
        if parts[0].lower() == 'daily':
            if len(parts) < 3:
                print("❌ Usage: add daily <time> <description>")
                print("   Times: morning, afternoon, evening, anytime")
                return
            
            time_of_day = parts[1].lower()
            description = ' '.join(parts[2:])
            
            # Validate time of day
            valid_times = [t.value for t in TimeOfDay]
            if time_of_day not in valid_times:
                print(f"❌ Invalid time. Use: {', '.join(valid_times)}")
                return
            
            habit_id = self.manager.add_habit(description, 'daily', time_of_day=time_of_day)
            print(f"✅ Daily habit added with ID: {habit_id} {format_time_of_day(time_of_day)}")
        
        elif parts[0].lower() == 'weekly':
            if len(parts) < 4:
                print("❌ Usage: add weekly <days> <time> <description>")
                print("   Example: add weekly monday,friday afternoon Go to gym")
                return
            
            days_str = parts[1]
            time_of_day = parts[2].lower()
            description = parts[3]
            
            # Validate time of day
            valid_times = [t.value for t in TimeOfDay]
            if time_of_day not in valid_times:
                print(f"❌ Invalid time. Use: {', '.join(valid_times)}")
                return
            
            days = [d.strip().capitalize() for d in days_str.split(',')]
            
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            invalid_days = [d for d in days if d not in valid_days]
            
            if invalid_days:
                print(f"❌ Invalid days: {', '.join(invalid_days)}")
                return
            
            habit_id = self.manager.add_habit(description, 'weekly', days, time_of_day)
            print(f"✅ Weekly habit added with ID: {habit_id} {format_time_of_day(time_of_day)}")
        
        else:
            # It's a regular task
            task_id = self.manager.add_task(line)
            print(f"✅ Task added with ID: {task_id}")
    
    def do_done(self, line):
        """Mark a task or habit as completed
        Usage: 
          done <id>            - Auto-detect and complete
          done task <id>       - Complete a specific task
          done habit <id>      - Check off a habit for today
        
        Examples:
          done 1
          done task 2
          done habit 3"""
        
        parts = line.strip().split()
        
        if not parts:
            print("❌ Usage: done <id> | done task <id> | done habit <id>")
            return
        
        try:
            if len(parts) == 2:
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
                item_id = int(parts[0])
                
                if self.manager.complete_task(item_id):
                    print(f"✅ Task {item_id} marked as completed!")
                elif self.manager.complete_habit_today(item_id):
                    print(f"✅ Habit {item_id} checked off for today!")
                else:
                    print(f"❌ Item {item_id} not found")
        
        except ValueError:
            print("❌ Please provide a valid ID (number)")
    
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
