# Student Helper Chatbot - CONVERSATIONAL VERSION (Simplified)
# This version adds natural conversation without heavy AI libraries!

import re
import random
import json
import os
from datetime import datetime, timedelta
import threading
import time

def greet_student():
    """
    Welcome message for our conversational chatbot
    """
    print("🎓 Welcome to your CONVERSATIONAL Student Helper!")
    print("I can now have natural conversations AND help with structured tasks!")
    print("\n🌟 Features:")
    print("📚 Track your subjects and grades")
    print("⏰ Set study reminders (WITH ACTIVE NOTIFICATIONS!)")
    print("📊 View your academic progress")
    print("🎯 Set and track study goals")
    print("💾 Save your data for next time")
    print("🗣️ Have natural conversations about studying!")
    print("\n💬 Try natural questions like:")
    print("- 'I'm struggling with time management, can you help?'")
    print("- 'What's the best way to study for exams?'")
    print("- 'How can I improve my grades?'")
    print("- 'I feel stressed about my studies'")
    print("- Or use commands: 'add subject Math grade 8.5'")
    print("- Type 'help' for all commands or 'quit' to exit")
    print("-" * 70)

class ConversationalStudentBot:
    def __init__(self):
        self.data_file = "student_data.json"
        self.student_data = self.load_student_data()
        self.reminder_thread = None
        self.running = True
        self.conversation_context = []
        
        # Enhanced patterns for structured commands
        self.command_patterns = {
            # SHOW commands must come FIRST to avoid conflicts!
            'show_subjects': [r'.*show.*subjects.*', r'.*list.*subjects.*', r'.*my.*subjects.*'],
            'show_progress': [r'.*show.*progress.*', r'.*my.*progress.*', r'.*academic.*progress.*'],
            'show_reminders': [r'.*show.*reminders.*', r'.*my.*reminders.*', r'.*list.*reminders.*'],
            'show_goals': [r'.*show.*goals.*', r'.*my.*goals.*', r'.*list.*goals.*'],
            'help_command': [r'^help$', r'.*help.*', r'.*commands.*', r'.*what.*can.*do.*'],
            
            # SET commands come after SHOW commands
            'add_subject': [r'.*add.*subject.*', r'.*new.*subject.*', r'.*subject.*grade.*'],
            'set_reminder': [r'.*set.*reminder.*', r'.*remind.*me.*'],
            'set_goal': [r'.*set.*goal.*', r'.*^goal.*', r'.*target.*'],
            'cgpa_calculation': [r'.*calculate.*cgpa.*', r'.*cgpa.*calculation.*', r'.*find.*cgpa.*']
        }
        
        # Conversational response patterns - this is the magic!
        self.conversation_patterns = {
            'struggling': {
                'keywords': ['struggling', 'difficult', 'hard', 'trouble', 'challenge', 'problem'],
                'responses': [
                    "I understand you're facing some challenges! 💪 That's completely normal for students. What specific area are you struggling with? I can help with study techniques, time management, or subject-specific advice.",
                    "Everyone struggles sometimes - you're not alone! 🤗 Tell me more about what's difficult for you. Is it a particular subject, time management, or study methods?",
                    "Struggles are part of the learning journey! 🌱 The fact that you're asking for help shows you're on the right track. What would you like to focus on improving?"
                ]
            },
            'motivation': {
                'keywords': ['motivation', 'motivated', 'inspire', 'encourage', 'give up', 'demotivated'],
                'responses': [
                    "🌟 Stay motivated! Remember why you started studying. Every small step counts! Set achievable goals and celebrate your progress. You've got this! 💪",
                    "Motivation comes and goes, but discipline stays! 🔥 Try breaking your big goals into smaller wins. Each completed task is progress!",
                    "You're capable of amazing things! 🚀 Sometimes we just need to remind ourselves of our 'why'. What are you studying towards?"
                ]
            },
            'stress': {
                'keywords': ['stress', 'stressed', 'anxiety', 'pressure', 'overwhelmed', 'worried'],
                'responses': [
                    "😌 Feeling stressed is normal, but let's manage it together! Try: 1) Break tasks into smaller chunks 2) Use the Pomodoro technique (25min study + 5min break) 3) Take regular breaks 4) Get enough sleep. Deep breaths! 🧘",
                    "Stress happens to everyone! 💙 Let's tackle this step by step. What's causing the most stress right now? We can make a plan together.",
                    "Take a deep breath! 🌬️ Stress often comes from feeling overwhelmed. Let's organize your tasks and set some manageable study reminders."
                ]
            },
            'improvement': {
                'keywords': ['improve', 'better', 'get good', 'enhance', 'upgrade', 'boost'],
                'responses': [
                    "📈 Great mindset! To improve: 1) Track your current performance 2) Set specific goals 3) Use active study techniques 4) Regular practice 5) Get feedback. What subject would you like to focus on?",
                    "Love the growth mindset! 🌱 Improvement comes from consistent effort. Let's identify your current level and create a plan to level up!",
                    "The fact that you want to improve shows you're already on the right path! 🎯 Let's set some specific goals and track your progress."
                ]
            },
            'study_methods': {
                'keywords': ['how to study', 'study methods', 'study techniques', 'learn better', 'memorize'],
                'responses': [
                    "📚 Great study techniques: 1) Active recall (test yourself) 2) Spaced repetition 3) Pomodoro technique 4) Teach others 5) Make summaries 6) Practice problems. Which subject are you studying?",
                    "Effective studying is about quality, not quantity! 🎯 Try the Feynman technique: explain concepts in simple terms. If you can't explain it simply, you don't understand it well enough.",
                    "Smart study tips: 1) Study in chunks, not marathons 2) Use multiple senses 3) Connect new info to what you know 4) Take breaks 5) Stay hydrated! 💧"
                ]
            },
            'time_management': {
                'keywords': ['time management', 'schedule', 'organize time', 'procrastination', 'deadline'],
                'responses': [
                    "⏰ Time management tips: 1) Use a planner 2) Prioritize with the Eisenhower Matrix 3) Time blocking 4) Eliminate distractions 5) Set deadlines before the real ones. What's your biggest time challenge?",
                    "Time is your most valuable resource! ⌛ Try the 2-minute rule: if something takes less than 2 minutes, do it now. For bigger tasks, break them down.",
                    "Procrastination killer tips: 1) Start with 5 minutes 2) Remove barriers 3) Use the 'Swiss cheese' method (poke holes in big tasks) 4) Reward yourself! 🎉"
                ]
            },
            'exams': {
                'keywords': ['exam', 'test', 'preparation', 'exam prep', 'nervous about exam'],
                'responses': [
                    "🎯 Exam prep strategy: 1) Start early 2) Create a study schedule 3) Practice with past papers 4) Study in exam conditions 5) Get enough sleep 6) Eat brain food 7) Stay calm and confident!",
                    "Exam success formula: Preparation + Practice + Positive mindset! 📝 Focus on understanding concepts, not just memorizing. How long until your exam?",
                    "Exam nerves are normal! 😊 Channel that energy into focused preparation. Create a realistic study plan and stick to it. You've got this! 💪"
                ]
            },
            'grades': {
                'keywords': ['grades', 'marks', 'score', 'gpa', 'cgpa', 'performance'],
                'responses': [
                    "📊 Grades reflect effort, not worth! Focus on learning and improvement. Track your progress with 'show my progress' and set goals with 'set goal [target]'. What subject would you like to improve in?",
                    "Remember: grades are feedback, not judgment! 🎯 Use them to identify areas for improvement. I can help you track your academic progress!",
                    "Good grades come from good habits! 📈 Consistent study, active participation, and seeking help when needed. Let's work on building those habits together!"
                ]
            }
        }
        
        # Start reminder monitoring
        self.start_reminder_monitoring()
    
    def get_conversational_response(self, user_input):
        """
        Generate natural conversational responses based on keywords and context
        """
        user_lower = user_input.lower()
        
        # Check each conversation pattern
        for pattern_name, pattern_data in self.conversation_patterns.items():
            # Check if any keywords match
            if any(keyword in user_lower for keyword in pattern_data['keywords']):
                # Get a random response from this category
                response = random.choice(pattern_data['responses'])
                
                # Add some personalization based on their data
                if pattern_name == 'improvement' and self.student_data.get('subjects'):
                    subjects = list(self.student_data['subjects'].keys())
                    response += f"\n\n💡 I see you're tracking: {', '.join(subjects[:3])}. Pick one to focus on improving!"
                
                if pattern_name == 'time_management':
                    response += "\n\n⏰ Tip: Try 'set reminder take break in 25 minutes' for Pomodoro!"
                
                if pattern_name == 'stress':
                    response += "\n\n💙 Remember: You can set study reminders to pace yourself better!"
                
                return response
        
        # Check for greeting patterns
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in user_lower for greeting in greetings):
            return random.choice([
                "Hello! 👋 I'm here to help with your studies! What's on your mind today?",
                "Hi there! 😊 Ready to tackle some academic challenges together?",
                "Hey! 🎓 How can I help you with your studies today?",
                "Hello! 🌟 What academic goal are you working on today?"
            ])
        
        # Check for gratitude
        thanks = ['thank', 'thanks', 'appreciate', 'helpful']
        if any(thank in user_lower for thank in thanks):
            return random.choice([
                "You're very welcome! 😊 That's what I'm here for! Any other questions?",
                "Happy to help! 🌟 Keep up the great work with your studies!",
                "Glad I could help! 💪 You're doing great - keep going!",
                "My pleasure! 🎯 Remember, I'm always here when you need study support!"
            ])
        
        # Default conversational fallback
        return f"That's an interesting point about '{user_input}'! 🤔 I'm here to help with your studies. What specific aspect would you like to explore? I can help with study strategies, time management, goal setting, or track your academic progress!"
    
    def is_structured_command(self, user_input):
        """
        Check if the input is a structured command rather than conversational
        """
        user_input = user_input.lower().strip()
        
        # Check for command patterns
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    return True, intent
        
        # Check for grade calculations
        if re.search(r'calculate.*\d+', user_input) or re.search(r'grades.*\d+', user_input):
            return True, 'cgpa_calculation'
        
        return False, None
    
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
                            print("💬 Chat with me: ", end="", flush=True)
                            
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
            'subjects': {},
            'reminders': [],
            'goals': [],
            'study_sessions': []
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
        Extract subject and grade from text
        """
        pattern = r'.*subject\s+([a-zA-Z\s]+)\s+grade\s+(\d+(?:\.\d+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            subject = match.group(1).strip().title()
            grade = float(match.group(2))
            
            if subject not in self.student_data['subjects']:
                self.student_data['subjects'][subject] = []
            
            self.student_data['subjects'][subject].append(grade)
            self.save_student_data()
            
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
                'target': 100
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
        return """🤖 CONVERSATIONAL Student Helper Commands:

🗣️ NATURAL CONVERSATION:
• "I'm struggling with time management, help me"
• "What's the best way to study for exams?"
• "I feel stressed about my studies"
• "How can I improve my grades?"
• "I need motivation to study"
• Chat naturally about any study topic!

📚 STRUCTURED COMMANDS:
• 'add subject [name] grade [grade]' - Add a subject grade
• 'show subjects' or 'show progress' - View all subjects

⏰ REMINDERS (WITH NOTIFICATIONS!):
• 'set reminder [task] at [time]' - Set timed reminder
• 'set reminder [task] in [X] minutes' - Set quick reminder
• 'show reminders' - View all reminders

🎯 GOALS:
• 'set goal [goal]' - Set a study goal
• 'show goals' - View all goals

📊 CALCULATIONS:
• 'calculate cgpa with grades X, Y, Z' - Calculate CGPA

💾 DATA:
Your data is automatically saved in 'student_data.json'

🔔 NOTIFICATIONS:
Reminders will automatically notify you when due!

🌟 NEW: I can now chat naturally about studying topics!"""
    
    def extract_grades_from_text(self, text):
        """
        Extract grades from text
        """
        grades = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        return [float(grade) for grade in grades if 0 <= float(grade) <= 10]
    
    def get_response(self, user_input):
        """
        Main response handler - chooses between structured commands and conversational AI
        """
        # Check if it's a structured command
        is_command, intent = self.is_structured_command(user_input)
        
        if is_command:
            # Handle structured commands
            if intent == 'add_subject':
                return self.add_subject_grade(user_input)
            elif intent in ['show_subjects', 'show_progress']:
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
            elif intent == 'cgpa_calculation':
                grades = self.extract_grades_from_text(user_input)
                if grades:
                    cgpa = sum(grades) / len(grades)
                    return f"🎯 CGPA: {cgpa:.2f} from grades {grades}\n💡 Add these to tracking: 'add subject [name] grade [grade]'"
                else:
                    return "🧮 CGPA Calculator ready! Format: 'calculate cgpa with grades 8, 9, 7, 8'"
        
        # Use conversational responses for natural questions
        return self.get_conversational_response(user_input)
    
    def shutdown(self):
        """
        Properly shutdown the bot
        """
        self.running = False

def main_conversational_chat():
    """
    Main chat loop for the conversational student chatbot
    """
    greet_student()
    bot = ConversationalStudentBot()
    
    print("✅ CONVERSATIONAL mode activated! Natural chat + structured commands!")
    print("💡 Try saying: 'I'm struggling with time management, can you help?'")
    
    try:
        while True:
            user_input = input("\n💬 Chat with me: ")
            
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

# Start the conversational chatbot
if __name__ == "__main__":
    print("🚀 Starting CONVERSATIONAL Student Helper...")
    main_conversational_chat()
