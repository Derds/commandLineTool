"""
TodoManager - handles data persistence and business logic
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

from .models import Task, Habit, TimeOfDay


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
                    
                    # Migrate old habits to include time_of_day
                    for habit in self.habits:
                        if 'time_of_day' not in habit:
                            habit['time_of_day'] = TimeOfDay.ANYTIME.value
                    
                    # Save migrated data
                    if self.habits:
                        self.save_data()
                        
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
    
    def add_habit(self, description: str, frequency: str, days: Optional[List[str]] = None,
                  time_of_day: str = TimeOfDay.ANYTIME.value) -> int:
        """Add a new habit with daily or weekly frequency and time of day"""
        habit = {
            'id': len(self.habits) + 1,
            'description': description,
            'frequency': frequency,
            'days': days or [],
            'time_of_day': time_of_day,
            'created_at': datetime.now().isoformat(),
            'completions': []
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
                     new_frequency: str = None, new_days: List[str] = None,
                     new_time_of_day: str = None) -> bool:
        """Update a habit's description, frequency, days, or time of day"""
        for habit in self.habits:
            if habit['id'] == habit_id:
                if new_description:
                    habit['description'] = new_description
                if new_frequency:
                    habit['frequency'] = new_frequency
                if new_days is not None:
                    habit['days'] = new_days
                if new_time_of_day:
                    habit['time_of_day'] = new_time_of_day
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
    
    def get_habits(self, time_filter: Optional[str] = None) -> List[Habit]:
        """Get all habits with today's completion status, optionally filtered by time"""
        today = datetime.now().date().isoformat()
        today_weekday = datetime.now().strftime('%A').lower()
        
        habit_objects = []
        for habit_dict in self.habits:
            habit = Habit(habit_dict)
            
            # Apply time filter if specified
            if time_filter and not habit.is_relevant_now():
                continue
            
            habit_objects.append(habit)
        
        return habit_objects
    
    def get_relevant_habits_now(self) -> List[Habit]:
        """Get habits that are relevant for the current time of day and due today"""
        today = datetime.now().date().isoformat()
        today_weekday = datetime.now().strftime('%A').lower()
        
        relevant = []
        for habit_dict in self.habits:
            habit = Habit(habit_dict)
            
            # Check if due today
            if not habit.is_due_today(today_weekday):
                continue
            
            # Check if already completed
            if habit.is_completed_today(today):
                continue
            
            # Check if relevant for current time
            if not habit.is_relevant_now():
                continue
            
            relevant.append(habit)
        
        return relevant
