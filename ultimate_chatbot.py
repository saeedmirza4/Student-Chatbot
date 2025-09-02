# Student Helper Chatbot - ULTIMATE VERSION with Conversational AI
# This version adds natural conversation capabilities while keeping all existing features!

import re
import random
import json
import os
from datetime import datetime, timedelta
import threading
import time

# Check if transformers is available for conversational AI
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    CONVERSATIONAL_AI_AVAILABLE = True
    print("🧠 Conversational AI libraries loaded successfully!")
except ImportError:
    CONVERSATIONAL_AI_AVAILABLE = False
    print("⚠️ Conversational AI not available. Install with: pip install transformers torch")

def greet_student():
    """
    Welcome message for our ultimate conversational chatbot
    """
    print("🎓 Welcome to your ULTIMATE Student Helper!")
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
    print("- Or use commands: 'add subject Math grade 8.5'")
    print("- Type 'help' for all commands or 'quit' to exit")
    print("-" * 70)

class UltimateStudentBot:
    def __init__(self):
        self.data_file = "student_data.json"
        self.student_data = self.load_student_data()
        self.reminder_thread = None
        self.running = True
        self.conversation_context = []
        
        # Initialize conversational AI if available
        self.conversational_ai = None
        if CONVERSATIONAL_AI_AVAILABLE:
            self.setup_conversational_ai()
        
        # Enhanced patterns for structured commands
        self.command_patterns = {
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
        
        # Start reminder monitoring
        self.start_reminder_monitoring()
    
    def setup_conversational_ai(self):
        """
        Set up the conversational AI model for natural conversations
        """
        try:
            print("🔄 Loading conversational AI... (this may take a moment)")
            
            # Use a lightweight conversational model
            model_name = "microsoft/DialoGPT-small"
            
            self.conversational_ai = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                pad_token_id=50256,
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            
            print("✅ Conversational AI ready! I can now chat naturally!")
            
        except Exception as e:
            print(f"⚠️ Conversational AI setup failed: {e}")
            self.conversational_ai = None
    
    def get_conversational_response(self, user_input):
        """
        Generate a natural conversational response using AI
        """
        if not self.conversational_ai:
            return None
        
        try:
            # Create a student-focused prompt
            student_prompt = f"""You are a helpful study assistant chatbot for students. You give friendly, encouraging advice about studying, academics, and student life. Keep responses concise and practical.

Student: {user_input}
Assistant:"""
            
            # Generate response
            response = self.conversational_ai(
                student_prompt,
                max_length=len(student_prompt.split()) + 50,
                num_return_sequences=1,
                pad_token_id=50256
            )
            
            # Extract the assistant's response
            full_text = response[0]['generated_text']
            assistant_response = full_text.split("Assistant:")[-1].strip()
            
            # Clean up the response
            if len(assistant_response) > 10 and assistant_response != user_input:
                return f"🤖 {assistant_response}"
            else:
                return None
                
        except Exception as e:
            print(f"⚠️ Conversational AI error: {e}")
            return None
    
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
    
    def get_smart_fallback(self, user_input):
        """
        Intelligent fallback responses for conversational queries
        """
        user_lower = user_input.lower()
        
        # Study-related conversational responses
        if any(word in user_lower for word in ['struggling', 'difficult', 'hard', 'trouble']):
            return "I understand you're facing some challenges! 💪 That's totally normal for students. What specific area are you struggling with? I can help with study techniques, time management, or subject-specific advice. You can also track your progress with 'add subject [name] grade [grade]' to see improvements over time!"
        
        if any(word in user_lower for word in ['motivation', 'motivated', 'inspire']):
            return "🌟 Stay motivated! Remember why you started studying. Every small step counts! Set achievable goals with 'set goal [your goal]' and celebrate your progress. You've got this! 💪"
        
        if any(word in user_lower for word in ['stress', 'stressed', 'anxiety', 'pressure']):
            return "😌 Feeling stressed is normal, but let's manage it together! Try: 1) Break tasks into smaller chunks 2) Use the Pomodoro technique 3) Take regular breaks 4) Get enough sleep. I can set study reminders to help you pace yourself: 'set reminder take break in 25 minutes'"
        
        if any(word in user_lower for word in ['improve', 'better', 'get good']):
            return "📈 Great mindset! To improve: 1) Track your current performance with 'show my progress' 2) Set specific goals with 'set goal [target]' 3) Use active study techniques 4) Regular practice. What subject would you like to focus on improving?"
        
        # Default conversational fallback
        return f"That's an interesting question about '{user_input}'! 🤔 I'm here to help with your studies. Try asking about study tips, time management, exam prep, or use commands like 'add subject Math grade 8.5' to track your progress. What would you like to focus on?"
    
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
        help_text = """🤖 ULTIMATE Student Helper Commands:

🗣️ CONVERSATIONAL MODE:
• Ask natural questions like "How can I study better?"
• "I'm struggling with time management, help me"
• "What's the best way to prepare for exams?"
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
• 'what is gpa/cgpa' - Get explanations

💾 DATA:
Your data is automatically saved in 'student_data.json'

🔔 NOTIFICATIONS:
Reminders will automatically notify you when due!

🌟 NEW: I can now chat naturally about studying!"""
        
        if CONVERSATIONAL_AI_AVAILABLE:
            help_text += "\n\n🧠 Conversational AI: ACTIVE ✅"
        else:
            help_text += "\n\n🧠 Conversational AI: Install transformers for natural chat"
        
        return help_text
    
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
            elif intent in ['gpa_question', 'cgpa_question', 'study_tips', 'time_management', 'exam_prep']:
                # Use conversational AI for these if available, otherwise fallback
                if self.conversational_ai:
                    ai_response = self.get_conversational_response(user_input)
                    if ai_response:
                        return ai_response
                return self.get_smart_fallback(user_input)
        
        # Try conversational AI for natural questions
        if self.conversational_ai:
            ai_response = self.get_conversational_response(user_input)
            if ai_response:
                return ai_response
        
        # Fallback to smart pattern-based responses
        return self.get_smart_fallback(user_input)
    
    def shutdown(self):
        """
        Properly shutdown the bot
        """
        self.running = False

def main_ultimate_chat():
    """
    Main chat loop for the ultimate conversational student chatbot
    """
    greet_student()
    bot = UltimateStudentBot()
    
    if CONVERSATIONAL_AI_AVAILABLE:
        print("✅ ULTIMATE mode activated! Natural conversations + structured commands!")
    else:
        print("✅ Advanced mode activated! Smart responses + structured commands!")
    
    print("💡 Try asking: 'I'm struggling with time management, can you help?'")
    
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

# Start the ultimate chatbot
if __name__ == "__main__":
    print("🚀 Starting ULTIMATE Student Helper with Conversational AI...")
    main_ultimate_chat()
