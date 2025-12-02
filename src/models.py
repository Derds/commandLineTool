"""
Data models for tasks and habits
"""

from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TimeOfDay(Enum):
    """Time periods for habit scheduling"""
    MORNING = "morning"      # Before 1pm
    AFTERNOON = "afternoon"  # 11:30am - 5pm
    EVENING = "evening"      # After 5pm
    ANYTIME = "anytime"      # No specific time


def get_current_time_of_day() -> TimeOfDay:
    """Determine current time of day based on system time"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    # Morning: midnight to 12:59pm
    if hour < 13:
        return TimeOfDay.MORNING
    # Afternoon: 1pm to 4:59pm
    elif hour < 17:
        return TimeOfDay.AFTERNOON
    # Evening: 5pm onwards
    else:
        return TimeOfDay.EVENING


def is_time_relevant(habit_time: str, current_time: Optional[TimeOfDay] = None) -> bool:
    """Check if a habit is relevant for the current time of day"""
    if current_time is None:
        current_time = get_current_time_of_day()
    
    # Anytime habits are always relevant
    if habit_time == TimeOfDay.ANYTIME.value:
        return True
    
    # Morning habits show in morning
    if habit_time == TimeOfDay.MORNING.value and current_time == TimeOfDay.MORNING:
        return True
    
    # Afternoon habits show from 11:30am onwards (allow morning planning)
    if habit_time == TimeOfDay.AFTERNOON.value:
        now = datetime.now()
        # Show afternoon habits if it's after 11:30am
        if (now.hour == 11 and now.minute >= 30) or now.hour >= 12:
            return True
    
    # Evening habits show from 5pm onwards
    if habit_time == TimeOfDay.EVENING.value and current_time == TimeOfDay.EVENING:
        return True
    
    return False


def format_time_of_day(time_of_day: str) -> str:
    """Format time of day for display"""
    time_emojis = {
        TimeOfDay.MORNING.value: "🌅",
        TimeOfDay.AFTERNOON.value: "☀️",
        TimeOfDay.EVENING.value: "🌙",
        TimeOfDay.ANYTIME.value: "⏰"
    }
    emoji = time_emojis.get(time_of_day, "⏰")
    return f"{emoji} {time_of_day.capitalize()}"


class Task:
    """Task model"""
    
    def __init__(self, task_dict: Dict):
        self.data = task_dict
    
    @property
    def id(self) -> int:
        return self.data['id']
    
    @property
    def description(self) -> str:
        return self.data['description']
    
    @property
    def completed(self) -> bool:
        return self.data.get('completed', False)
    
    def to_dict(self) -> Dict:
        return self.data


class Habit:
    """Habit model with time of day support"""
    
    def __init__(self, habit_dict: Dict):
        self.data = habit_dict
        # Set default time_of_day if not present
        if 'time_of_day' not in self.data:
            self.data['time_of_day'] = TimeOfDay.ANYTIME.value
    
    @property
    def id(self) -> int:
        return self.data['id']
    
    @property
    def description(self) -> str:
        return self.data['description']
    
    @property
    def frequency(self) -> str:
        return self.data['frequency']
    
    @property
    def days(self) -> List[str]:
        return self.data.get('days', [])
    
    @property
    def time_of_day(self) -> str:
        return self.data.get('time_of_day', TimeOfDay.ANYTIME.value)
    
    @property
    def completions(self) -> List[str]:
        return self.data.get('completions', [])
    
    def is_due_today(self, today_weekday: str) -> bool:
        """Check if habit is due today"""
        if self.frequency == 'daily':
            return True
        elif self.frequency == 'weekly':
            return today_weekday in [d.lower() for d in self.days]
        return False
    
    def is_completed_today(self, today: str) -> bool:
        """Check if habit is completed today"""
        return today in self.completions
    
    def is_relevant_now(self) -> bool:
        """Check if habit is relevant for current time of day"""
        return is_time_relevant(self.time_of_day)
    
    def to_dict(self) -> Dict:
        return self.data
