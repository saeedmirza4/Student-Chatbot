# Student Helper Chatbot - Milestone 2: Smart Pattern-Matching AI
# This version is FREE and doesn't need heavy AI libraries!
# It uses intelligent pattern matching to understand different ways of asking

import re
import random
from datetime import datetime

def greet_student():
    """
    Welcome message for our smart chatbot
    """
    print("🤖 Hello! I'm your Smart Student Helper!")
    print("I understand natural language and can help with various student questions!")
    print("Try asking me:")
    print("- Calculate my CGPA with grades 8, 9, 7, 8")
    print("- How can I manage my time better?")
    print("- Give me tips for studying effectively")
    print("- What's the difference between GPA and CGPA?")
    print("- Type 'quit' to exit")
    print("-" * 60)

class SmartStudentBot:
    def __init__(self):
        # Patterns for understanding different ways to ask questions
        self.patterns = {
            'gpa_question': [
                r'.*what.*gpa.*',
                r'.*explain.*gpa.*',
                r'.*gpa.*mean.*',
                r'.*gpa.*definition.*',
                r'.*define.*gpa.*'
            ],
            'cgpa_question': [
                r'.*what.*cgpa.*',
                r'.*explain.*cgpa.*',
                r'.*cgpa.*mean.*',
                r'.*cgpa.*definition.*',
                r'.*define.*cgpa.*'
            ],
            'cgpa_calculation': [
                r'.*calculate.*cgpa.*',
                r'.*cgpa.*calculation.*',
                r'.*how.*calculate.*cgpa.*',
                r'.*find.*cgpa.*',
                r'.*compute.*cgpa.*',
                r'.*cgpa.*(\d+.*\d+.*\d+.*)',  # Detects numbers in the question
            ],
            'study_tips': [
                r'.*study.*tips.*',
                r'.*how.*study.*',
                r'.*study.*better.*',
                r'.*study.*advice.*',
                r'.*study.*methods.*',
                r'.*effective.*study.*',
                r'.*give.*tips.*study.*'
            ],
            'time_management': [
                r'.*time.*management.*',
                r'.*manage.*time.*',
                r'.*time.*tips.*',
                r'.*organize.*time.*',
                r'.*schedule.*help.*'
            ],
            'exam_prep': [
                r'.*exam.*prep.*',
                r'.*prepare.*exam.*',
                r'.*exam.*tips.*',
                r'.*exam.*study.*',
                r'.*test.*preparation.*'
            ]
        }
        
        # Multiple response variations to sound more natural
        self.responses = {
            'gpa_question': [
                "GPA stands for Grade Point Average! 📊 It's a numerical representation of your academic performance, usually calculated on a scale of 0-4.0 (US system) or 0-10 (some other systems). It helps schools and employers quickly understand your academic standing.",
                "Great question! GPA (Grade Point Average) is like your academic report card in one number. It shows how well you're doing overall in your studies. Higher GPA = better performance! Most systems use either 0-4.0 or 0-10 scales.",
            ],
            'cgpa_question': [
                "CGPA stands for Cumulative Grade Point Average! 🎓 It's your overall academic performance across ALL semesters or years, while GPA might just be for one semester. Think of CGPA as your complete academic journey summed up in one number!",
                "CGPA is your 'lifetime' academic average! While GPA shows one semester's performance, CGPA shows your ENTIRE academic journey. It's what employers and graduate schools really care about!",
            ],
            'cgpa_calculation': [
                "I can help you calculate CGPA! 🧮 Here's how:\n1️⃣ Add all your grade points\n2️⃣ Divide by total number of subjects\n3️⃣ Formula: (Grade1 + Grade2 + ... + GradeN) ÷ N\n\nIf you give me your grades, I can calculate it for you!",
                "CGPA calculation is easy! ✨ Just add all grades and divide by the number of subjects. For example: grades 8,9,7,8 → (8+9+7+8)÷4 = 8.0 CGPA. Share your grades and I'll calculate yours!",
            ],
            'study_tips': [
                "Here are proven study strategies! 📚✨\n🎯 Active Learning: Test yourself instead of just re-reading\n⏰ Pomodoro Technique: 25 min study + 5 min break\n📝 Cornell Notes: Divide notes into sections\n🏠 Dedicated Space: Same spot every time\n😴 Sleep: 7-8 hours for memory consolidation\n🔄 Spaced Repetition: Review material at increasing intervals",
                "Absolutely! Here's what research shows works best! 🧠\n💡 Explain concepts to someone else (even yourself!)\n📊 Use visual aids: diagrams, charts, mind maps\n🎵 Create memory tricks and mnemonics\n⚡ Study during your peak energy hours\n🍎 Take care of your body: exercise, nutrition, hydration\n📱 Minimize distractions: phone away, focus apps",
            ],
            'time_management': [
                "Time management is a superpower! ⚡ Here's how to master it:\n📅 Use a planner (digital or paper)\n🎯 Priority Matrix: Urgent vs Important\n🍎 Eat the frog: Hard tasks first\n⏰ Time blocking: Assign specific hours to tasks\n🚫 Learn to say NO to time-wasters\n🎉 Reward yourself for completing tasks!",
                "Great question! Time management = life management! 🌟\n📝 Brain dump: Write everything down\n🔢 Use the 80/20 rule: Focus on high-impact activities\n⏰ Set realistic deadlines\n🔄 Weekly reviews: What worked? What didn't?\n🧘 Include buffer time for unexpected things\n💪 Build routines to reduce decision fatigue",
            ],
            'exam_prep': [
                "Exam preparation strategy! 🎯\n📚 Start early: No cramming!\n📋 Create a study schedule working backwards from exam date\n🎯 Practice tests: Simulate exam conditions\n👥 Study groups: Teach and learn from others\n🧠 Memory techniques: Flashcards, mnemonics\n😌 Stress management: Exercise, meditation, proper sleep\n🍎 Nutrition: Brain food on exam day!",
                "Let's ace those exams! 🏆\n📖 Active reading: Summarize, question, review\n✍️ Practice writing: If it's a written exam\n⏰ Time management during exams: Don't spend too long on one question\n🔍 Review mistakes: Learn from practice tests\n💤 Rest before exams: Tired brain = poor performance\n🎯 Positive mindset: You've got this!",
            ]
        }
    
    def extract_grades_from_text(self, text):
        """
        Extracts numerical grades from user input
        """
        # Find all numbers in the text (grades)
        grades = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        return [float(grade) for grade in grades if 0 <= float(grade) <= 10]
    
    def calculate_cgpa(self, grades):
        """
        Calculates CGPA from a list of grades
        """
        if not grades:
            return None
        
        cgpa = sum(grades) / len(grades)
        return round(cgpa, 2)
    
    def match_pattern(self, user_input):
        """
        Uses pattern matching to understand what the user is asking
        """
        user_input = user_input.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input):
                    return intent
        
        return 'unknown'
    
    def get_response(self, user_input):
        """
        Generates an intelligent response based on user input
        """
        intent = self.match_pattern(user_input)
        
        # Special handling for CGPA calculation
        if intent == 'cgpa_calculation':
            grades = self.extract_grades_from_text(user_input)
            if grades:
                cgpa = self.calculate_cgpa(grades)
                return f"🎯 Based on your grades {grades}, your CGPA is {cgpa}!\n\nCalculation: ({' + '.join(map(str, grades))}) ÷ {len(grades)} = {cgpa}\n\nThat's a {'excellent' if cgpa >= 8.5 else 'very good' if cgpa >= 7.5 else 'good' if cgpa >= 6.5 else 'satisfactory'} performance! 🌟"
            else:
                return random.choice(self.responses['cgpa_calculation'])
        
        # Regular pattern responses
        if intent in self.responses:
            return random.choice(self.responses[intent])
        
        # Smart fallback for unknown questions
        return self.smart_fallback(user_input)
    
    def smart_fallback(self, user_input):
        """
        Intelligent fallback when we don't recognize the question
        """
        keywords = user_input.lower().split()
        
        suggestions = []
        if any(word in keywords for word in ['grade', 'marks', 'score']):
            suggestions.append("📊 GPA/CGPA calculations")
        if any(word in keywords for word in ['study', 'learn', 'read']):
            suggestions.append("📚 Study tips and techniques")
        if any(word in keywords for word in ['time', 'schedule', 'plan']):
            suggestions.append("⏰ Time management strategies")
        if any(word in keywords for word in ['exam', 'test', 'preparation']):
            suggestions.append("🎯 Exam preparation advice")
        
        if suggestions:
            return f"I think you're asking about {', '.join(suggestions)}! Could you rephrase your question? I can help with academic calculations, study strategies, time management, and exam preparation. 🤖"
        
        return f"That's an interesting question about '{user_input}'! I specialize in helping students with:\n📊 GPA/CGPA calculations\n📚 Study tips and techniques\n⏰ Time management\n🎯 Exam preparation\n\nCould you rephrase your question using these topics? 😊"

def main_smart_chat():
    """
    Main chat loop for our smart pattern-matching chatbot
    """
    greet_student()
    bot = SmartStudentBot()
    
    print("✅ Smart AI ready! Ask me anything about academics!")
    
    while True:
        user_input = input("\n💬 Ask me anything: ")
        
        if user_input.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Goodbye! Keep studying smart, not just hard! 🌟")
            break
        
        if user_input.strip() == "":
            continue
        
        response = bot.get_response(user_input)
        print(f"\n🤖 Smart Assistant: {response}")

# Start the smart chatbot
if __name__ == "__main__":
    print("🚀 Starting Smart Student Helper Chatbot...")
    main_smart_chat()
