# Student Helper Chatbot - Milestone 3: Advanced Features
# This version includes reminders, progress tracking, and data persistence!

import re
import random
import json
import os
from datetime import datetime, timedelta

def greet_student():
    """
    Welcome message for our advanced chatbot
    """
    print("🎓 Welcome to your Advanced Student Helper!")
    print("I can now do much more than just answer questions!")
    print("\n🌟 New Features:")
    print("📚 Track your subjects and grades")
    print("⏰ Set study reminders")
    print("📊 View your academic progress")
    print("🎯 Set and track study goals")
    print("💾 Save your data for next time")
    print("\n💬 Try commands like:")
    print("- 'add subject Math grade 8.5'")
    print("- 'set reminder study Physics at 7pm tomorrow'")
    print("- 'show my progress'")
    print("- 'set goal study 2 hours daily'")
    print("- Type 'help' for all commands or 'quit' to exit")
    print("-" * 70)

class AdvancedStudentBot:
    def __init__(self):
        self.data_file = "student_data.json"
        self.student_data = self.load_student_data()
        
        # Enhanced patterns for new features
        self.patterns = {
            # Original patterns
            'gpa_question': [r'.*what.*gpa.*', r'.*explain.*gpa.*', r'.*gpa.*mean.*'],
            'cgpa_question': [r'.*what.*cgpa.*', r'.*explain.*cgpa.*', r'.*cgpa.*mean.*'],
            'cgpa_calculation': [r'.*calculate.*cgpa.*', r'.*cgpa.*calculation.*', r'.*find.*cgpa.*'],
            'study_tips': [r'.*study.*tips.*', r'.*how.*study.*', r'.*study.*better.*'],
            'time_management': [r'.*time.*management.*', r'.*manage.*time.*'],
            'exam_prep': [r'.*exam.*prep.*', r'.*prepare.*exam.*'],
            
            # New advanced patterns
            'add_subject': [r'.*add.*subject.*', r'.*new.*subject.*', r'.*subject.*grade.*'],
            'show_subjects': [r'.*show.*subjects.*', r'.*list.*subjects.*', r'.*my.*subjects.*'],
            'show_progress': [r'.*show.*progress.*', r'.*my.*progress.*', r'.*academic.*progress.*'],
            'set_reminder': [r'.*set.*reminder.*', r'.*remind.*me.*', r'.*reminder.*'],
            'show_reminders': [r'.*show.*reminders.*', r'.*my.*reminders.*', r'.*list.*reminders.*'],
            'set_goal': [r'.*set.*goal.*', r'.*goal.*', r'.*target.*'],
            'show_goals': [r'.*show.*goals.*', r'.*my.*goals.*', r'.*list.*goals.*'],
            'help_command': [r'^help$', r'.*help.*', r'.*commands.*', r'.*what.*can.*do.*']
        }
        
        self.responses = {
            'gpa_question': [
                "GPA stands for Grade Point Average! 📊 It's your academic performance in numbers. I can help you track your GPA by subject too! Try 'add subject Math grade 8.5'"
            ],
            'study_tips': [
                "📚 Smart Study Tips:\n🎯 Use the Pomodoro Technique (25min focus + 5min break)\n📝 Active recall: Test yourself regularly\n🏠 Dedicated study space\n😴 7-8 hours sleep for memory\n💡 Teach concepts to others\n\nI can set study reminders for you! Try 'set reminder study Math at 6pm'"
            ]
        }
    
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
        Set a study reminder
        """
        # Simple reminder parsing
        if 'at' in text.lower():
            parts = text.lower().split('at')
            if len(parts) >= 2:
                task = parts[0].replace('set reminder', '').replace('remind me', '').strip()
                time_part = parts[1].strip()
                
                reminder = {
                    'task': task,
                    'time': time_part,
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'completed': False
                }
                
                self.student_data['reminders'].append(reminder)
                self.save_student_data()
                
                return f"⏰ Reminder set!\n📝 Task: {task}\n🕐 Time: {time_part}\n💡 I'll remind you when you ask 'show reminders'!"
        
        return "⏰ Format: 'set reminder [task] at [time]'\nExample: 'set reminder study Physics at 7pm tomorrow'"
    
    def show_reminders(self):
        """
        Show all reminders
        """
        if not self.student_data['reminders']:
            return "⏰ No reminders set! Try: 'set reminder study Math at 6pm'"
        
        result = "⏰ Your Study Reminders:\n" + "="*30 + "\n"
        
        for i, reminder in enumerate(self.student_data['reminders'], 1):
            status = "✅ Completed" if reminder['completed'] else "⏳ Pending"
            result += f"\n{i}. 📝 {reminder['task']}\n"
            result += f"   🕐 {reminder['time']}\n"
            result += f"   {status}\n"
        
        result += "\n💡 Tip: Mark reminders complete by saying 'complete reminder 1'"
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

⏰ REMINDERS:
• 'set reminder [task] at [time]' - Set a study reminder
• 'show reminders' - View all reminders

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

Example: 'add subject Math grade 8.5'"""
    
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

def main_advanced_chat():
    """
    Main chat loop for advanced chatbot
    """
    greet_student()
    bot = AdvancedStudentBot()
    
    print("✅ Advanced features loaded! Type 'help' to see all commands.")
    
    while True:
        user_input = input("\n💬 Command or question: ")
        
        if user_input.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Goodbye! Your data has been saved. Keep studying smart! 🌟")
            break
        
        if user_input.strip() == "":
            continue
        
        response = bot.get_response(user_input)
        print(f"\n🤖 Assistant: {response}")

# Start the advanced chatbot
if __name__ == "__main__":
    print("🚀 Starting Advanced Student Helper Chatbot...")
    main_advanced_chat()
