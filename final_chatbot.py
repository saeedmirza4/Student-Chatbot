# Student Helper Chatbot - Milestone 3: FIXED Advanced Features
# This version includes WORKING real-time reminder notifications!

import re
import random
import json
import os
from datetime import datetime, timedelta
import threading
import time

def greet_student():
    """
    Welcome message for our advanced chatbot with working reminders
    """
    print("🎓 Welcome to your Advanced Student Helper!")
    print("I can now do much more than just answer questions!")
    print("\n🌟 Features:")
    print("📚 Track your subjects and grades")
    print("⏰ Set study reminders (WITH ACTIVE NOTIFICATIONS!)")
    print("📊 View your academic progress")
    print("🎯 Set and track study goals")
    print("💾 Save your data for next time")
    print("\n💬 Try commands like:")
    print("- 'add subject Math grade 8.5'")
    print("- 'set reminder study Physics in 2 minutes'")
    print("- 'show my progress'")
    print("- 'set goal study 2 hours daily'")
    print("- Type 'help' for all commands or 'quit' to exit")
    print("-" * 70)

class AdvancedStudentBot:
    def __init__(self):
        self.data_file = "student_data.json"
        self.student_data = self.load_student_data()
        self.reminder_thread = None
        self.running = True
        
        # Enhanced patterns for new features - ORDER MATTERS!
        self.patterns = {
            # Original patterns
            'gpa_question': [r'.*what.*gpa.*', r'.*explain.*gpa.*', r'.*gpa.*mean.*'],
            'cgpa_question': [r'.*what.*cgpa.*', r'.*explain.*cgpa.*', r'.*cgpa.*mean.*'],
            'cgpa_calculation': [r'.*calculate.*cgpa.*', r'.*cgpa.*calculation.*', r'.*find.*cgpa.*'],
            'study_tips': [r'.*study.*tips.*', r'.*how.*study.*', r'.*study.*better.*'],
            'time_management': [r'.*time.*management.*', r'.*manage.*time.*'],
            'exam_prep': [r'.*exam.*prep.*', r'.*prepare.*exam.*'],
            
            # SHOW commands must come BEFORE SET commands to avoid conflicts!
            'show_subjects': [r'.*show.*subjects.*', r'.*list.*subjects.*', r'.*my.*subjects.*'],
            'show_progress': [r'.*show.*progress.*', r'.*my.*progress.*', r'.*academic.*progress.*'],
            'show_reminders': [r'.*show.*reminders.*', r'.*my.*reminders.*', r'.*list.*reminders.*'],
            'show_goals': [r'.*show.*goals.*', r'.*my.*goals.*', r'.*list.*goals.*'],
            'help_command': [r'^help$', r'.*help.*', r'.*commands.*', r'.*what.*can.*do.*'],
            
            # SET commands come after SHOW commands
            'add_subject': [r'.*add.*subject.*', r'.*new.*subject.*', r'.*subject.*grade.*'],
            'set_reminder': [r'.*set.*reminder.*', r'.*remind.*me.*'],
            'set_goal': [r'.*set.*goal.*', r'.*^goal.*', r'.*target.*']
        }
        
        self.responses = {
            'gpa_question': [
                "GPA stands for Grade Point Average! 📊 It's your academic performance in numbers. I can help you track your GPA by subject too! Try 'add subject Math grade 8.5'"
            ],
            'study_tips': [
                "📚 Smart Study Tips:\n🎯 Use the Pomodoro Technique (25min focus + 5min break)\n📝 Active recall: Test yourself regularly\n🏠 Dedicated study space\n😴 7-8 hours sleep for memory\n💡 Teach concepts to others\n\nI can set study reminders for you! Try 'set reminder study Math in 5 minutes'"
            ]
        }
        
        # Start reminder monitoring
        self.start_reminder_monitoring()
    
    def start_reminder_monitoring(self):
        """
        Start background thread to monitor reminders
        """
        def monitor_reminders():
            while self.running:
                self.check_due_reminders()
                time.sleep(30)  # Check every 30 seconds
        
        self.reminder_thread = threading.Thread(target=monitor_reminders)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
    
    def check_due_reminders(self):
        """
        Check if any reminders are due and notify
        """
        if not self.student_data.get('reminders'):
            return
        
        current_time = datetime.now()
        
        for reminder in self.student_data['reminders']:
            if not reminder.get('completed', False) and not reminder.get('notified', False):
                reminder_time = reminder.get('due_datetime')
                if reminder_time:
                    try:
                        reminder_dt = datetime.fromisoformat(reminder_time)
                        if current_time >= reminder_dt:
                            # Show notification
                            print(f"\n\n🔔 REMINDER ALERT! 🔔")
                            print(f"⏰ Time: {reminder['time']}")
                            print(f"📝 Task: {reminder['task']}")
                            print(f"💡 Don't forget to {reminder['task']}!")
                            print("="*40)
                            print("💬 Command or question: ", end="", flush=True)
                            
                            # Mark as notified
                            reminder['notified'] = True
                            self.save_student_data()
                    except:
                        pass
    
    def parse_reminder_time(self, time_str):
        """
        Parse natural language time into datetime
        """
        current_time = datetime.now()
        time_str = time_str.lower().strip()
        
        # Handle "in X minutes"
        if 'in' in time_str and 'minute' in time_str:
            try:
                minutes = int(re.search(r'(\d+)', time_str).group(1))
                due_time = current_time + timedelta(minutes=minutes)
                return due_time, f"in {minutes} minutes"
            except:
                pass
        
        # Handle "in X hours"
        if 'in' in time_str and 'hour' in time_str:
            try:
                hours = int(re.search(r'(\d+)', time_str).group(1))
                due_time = current_time + timedelta(hours=hours)
                return due_time, f"in {hours} hours"
            except:
                pass
        
        # Handle "at X:XX pm/am"
        time_pattern = r'(\d{1,2}):(\d{2})\s*(am|pm)?'
        match = re.search(time_pattern, time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            ampm = match.group(3)
            
            if ampm == 'pm' and hour != 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            
            due_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if due_time <= current_time:
                due_time += timedelta(days=1)
            
            return due_time, f"at {hour:02d}:{minute:02d}"
        
        # Default: 5 minutes from now
        due_time = current_time + timedelta(minutes=5)
        return due_time, "in 5 minutes (default)"
    
    def load_student_data(self):
        """
        Load student data from file if it exists
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default structure
        return {
            'subjects': {},  # {'Math': [8.5, 9.0], 'Physics': [7.5]}
            'reminders': [],  # [{'task': 'study Math', 'time': '2024-01-01 18:00', 'completed': False}]
            'goals': [],     # [{'goal': 'study 2 hours daily', 'target': 2, 'progress': 0}]
            'study_sessions': []  # Track study time
        }
    
    def save_student_data(self):
        """
        Save student data to file
        """
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.student_data, f, indent=2)
            return True
        except:
            return False
    
    def add_subject_grade(self, text):
        """
        Extract subject and grade from text like 'add subject Math grade 8.5'
        """
        # Pattern to extract subject and grade
        pattern = r'.*subject\s+([a-zA-Z\s]+)\s+grade\s+(\d+(?:\.\d+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            subject = match.group(1).strip().title()
            grade = float(match.group(2))
            
            if subject not in self.student_data['subjects']:
                self.student_data['subjects'][subject] = []
            
            self.student_data['subjects'][subject].append(grade)
            self.save_student_data()
            
            # Calculate current average for this subject
            avg = sum(self.student_data['subjects'][subject]) / len(self.student_data['subjects'][subject])
            
            return f"✅ Added {subject}: {grade}\n📊 Current average in {subject}: {avg:.2f}\n💾 Data saved!"
        
        return "❌ Format: 'add subject [SubjectName] grade [Grade]'\nExample: 'add subject Math grade 8.5'"
    
    def show_subjects_progress(self):
        """
        Show all subjects and their progress
        """
        if not self.student_data['subjects']:
            return "📚 No subjects added yet! Try: 'add subject Math grade 8.5'"
        
        result = "📊 Your Academic Progress:\n" + "="*40 + "\n"
        
        total_points = 0
        total_subjects = 0
        
        for subject, grades in self.student_data['subjects'].items():
            avg = sum(grades) / len(grades)
            total_points += avg
            total_subjects += 1
            
            performance = "🌟 Excellent" if avg >= 8.5 else "👍 Very Good" if avg >= 7.5 else "✅ Good" if avg >= 6.5 else "📈 Improving"
            
            result += f"\n📚 {subject}:\n"
            result += f"   Grades: {grades}\n"
            result += f"   Average: {avg:.2f} {performance}\n"
        
        if total_subjects > 0:
            overall_cgpa = total_points / total_subjects
            result += f"\n🎯 Overall CGPA: {overall_cgpa:.2f}"
            result += f"\n📈 Total Subjects: {total_subjects}"
        
        return result
    
    def set_reminder(self, text):
        """
        Set a study reminder with improved time parsing
        """
        # Extract task and time
        if 'at' in text.lower():
            parts = text.lower().split('at')
            task = parts[0].replace('set reminder', '').replace('remind me', '').strip()
            time_part = parts[1].strip()
        elif 'in' in text.lower():
            parts = text.lower().split('in')
            task = parts[0].replace('set reminder', '').replace('remind me', '').strip()
            time_part = 'in ' + parts[1].strip()
        else:
            return "⏰ Format: 'set reminder [task] at [time]' or 'set reminder [task] in [time]'\nExamples:\n- 'set reminder study Physics at 7:30pm'\n- 'set reminder review notes in 10 minutes'"
        
        if task and time_part:
            due_datetime, formatted_time = self.parse_reminder_time(time_part)
            
            reminder = {
                'task': task,
                'time': formatted_time,
                'due_datetime': due_datetime.isoformat(),
                'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed': False,
                'notified': False
            }
            
            self.student_data['reminders'].append(reminder)
            self.save_student_data()
            
            return f"⏰ Reminder set!\n📝 Task: {task}\n🕐 Time: {formatted_time}\n⚡ I'll notify you automatically when it's time!\n💾 Reminder saved!"
        
        return "⏰ Please specify both task and time!"
    
    def show_reminders(self):
        """
        Show all reminders with better formatting
        """
        if not self.student_data['reminders']:
            return "⏰ No reminders set! Try: 'set reminder study Math in 5 minutes'"
        
        result = "⏰ Your Study Reminders:\n" + "="*30 + "\n"
        
        for i, reminder in enumerate(self.student_data['reminders'], 1):
            if reminder['completed']:
                status = "✅ Completed"
            elif reminder.get('notified', False):
                status = "🔔 Notified"
            else:
                status = "⏳ Pending"
            
            result += f"\n{i}. 📝 {reminder['task']}\n"
            result += f"   🕐 {reminder['time']}\n"
            result += f"   {status}\n"
        
        result += "\n💡 Active reminders will notify you automatically!"
        return result
    
    def set_goal(self, text):
        """
        Set a study goal
        """
        goal_text = text.replace('set goal', '').replace('goal', '').strip()
        
        if goal_text:
            goal = {
                'goal': goal_text,
                'created': datetime.now().strftime('%Y-%m-%d'),
                'progress': 0,
                'target': 100  # Default target
            }
            
            self.student_data['goals'].append(goal)
            self.save_student_data()
            
            return f"🎯 Goal set: {goal_text}\n📈 Track your progress with 'show goals'\n💪 You've got this!"
        
        return "🎯 Format: 'set goal [your goal]'\nExample: 'set goal study 2 hours daily'"
    
    def show_goals(self):
        """
        Show all goals
        """
        if not self.student_data['goals']:
            return "🎯 No goals set! Try: 'set goal study 2 hours daily'"
        
        result = "🎯 Your Study Goals:\n" + "="*25 + "\n"
        
        for i, goal in enumerate(self.student_data['goals'], 1):
            result += f"\n{i}. 📋 {goal['goal']}\n"
            result += f"   📅 Created: {goal['created']}\n"
            result += f"   📈 Progress: {goal['progress']}%\n"
        
        result += "\n💡 Keep working towards your goals! 🌟"
        return result
    
    def show_help(self):
        """
        Show all available commands
        """
        return """🤖 Student Helper Commands:

📚 SUBJECT TRACKING:
• 'add subject [name] grade [grade]' - Add a subject grade
• 'show subjects' or 'show progress' - View all subjects

⏰ REMINDERS (WITH NOTIFICATIONS!):
• 'set reminder [task] at [time]' - Set timed reminder
• 'set reminder [task] in [X] minutes' - Set quick reminder
• 'show reminders' - View all reminders

Examples:
• 'set reminder study Physics at 7:30pm'
• 'set reminder review notes in 10 minutes'

🎯 GOALS:
• 'set goal [goal]' - Set a study goal
• 'show goals' - View all goals

📊 CALCULATIONS:
• 'calculate cgpa with grades X, Y, Z' - Calculate CGPA
• 'what is gpa/cgpa' - Get explanations

📚 STUDY HELP:
• 'study tips' - Get study advice
• 'time management' - Get time management tips
• 'exam prep' - Get exam preparation advice

💾 DATA:
Your data is automatically saved in 'student_data.json'

🔔 NOTIFICATIONS:
Reminders will automatically notify you when due!"""
    
    def match_pattern(self, user_input):
        """
        Enhanced pattern matching for new features
        """
        user_input = user_input.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    return intent
        
        return 'unknown'
    
    def get_response(self, user_input):
        """
        Enhanced response handling with new features
        """
        intent = self.match_pattern(user_input)
        
        # Handle new features
        if intent == 'add_subject':
            return self.add_subject_grade(user_input)
        elif intent == 'show_subjects' or intent == 'show_progress':
            return self.show_subjects_progress()
        elif intent == 'set_reminder':
            return self.set_reminder(user_input)
        elif intent == 'show_reminders':
            return self.show_reminders()
        elif intent == 'set_goal':
            return self.set_goal(user_input)
        elif intent == 'show_goals':
            return self.show_goals()
        elif intent == 'help_command':
            return self.show_help()
        
        # Handle CGPA calculation
        elif intent == 'cgpa_calculation':
            grades = self.extract_grades_from_text(user_input)
            if grades:
                cgpa = sum(grades) / len(grades)
                return f"🎯 CGPA: {cgpa:.2f} from grades {grades}\n💡 Add these to tracking: 'add subject [name] grade [grade]'"
            else:
                return "🧮 CGPA Calculator ready! Format: 'calculate cgpa with grades 8, 9, 7, 8'"
        
        # Original responses for other intents
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        
        # Smart fallback
        return f"🤔 Try 'help' to see all commands!\n💡 Or ask about: study tips, GPA/CGPA, time management, or exam prep"
    
    def extract_grades_from_text(self, text):
        """
        Extract grades from text
        """
        grades = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        return [float(grade) for grade in grades if 0 <= float(grade) <= 10]
    
    def shutdown(self):
        """
        Properly shutdown the bot
        """
        self.running = False

def main_advanced_chat():
    """
    Main chat loop for advanced chatbot with working reminders
    """
    greet_student()
    bot = AdvancedStudentBot()
    
    print("✅ Advanced features loaded! Reminders will notify automatically!")
    print("💡 Try: 'set reminder test in 1 minute' to see it work!")
    
    try:
        while True:
            user_input = input("\n💬 Command or question: ")
            
            if user_input.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n👋 Goodbye! Your data has been saved. Keep studying smart! 🌟")
                bot.shutdown()
                break
            
            if user_input.strip() == "":
                continue
            
            response = bot.get_response(user_input)
            print(f"\n🤖 Assistant: {response}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Your data has been saved.")
        bot.shutdown()

# Start the advanced chatbot
if __name__ == "__main__":
    print("🚀 Starting Advanced Student Helper with WORKING Reminders...")
    main_advanced_chat()
