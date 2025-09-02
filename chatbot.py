# Student Helper Chatbot - Milestone 1: Simple FAQ Bot
# This is our main chatbot file where all the magic happens!

def greet_student():
    """
    This function shows a welcome message to the student.
    A function is like a recipe - it does a specific task when called.
    """
    print("🎓 Hello! I'm your Student Helper Chatbot!")
    print("I can help you with common student questions.")
    print("Ask me things like:")
    print("- What is GPA?")
    print("- How to calculate CGPA?")
    print("- What are study tips?")
    print("- Type 'quit' to exit")
    print("-" * 50)

def get_faq_response(user_question):
    """
    This function takes a student's question and returns an answer.
    It uses a dictionary (like a phone book) to match questions with answers.
    """
    
    # Convert the question to lowercase so "GPA" and "gpa" both work
    question = user_question.lower().strip()
    
    # This is our FAQ database - a dictionary that stores question-answer pairs
    # Now with multiple ways to ask the same question!
    faq_database = {
        # GPA Questions
        "what is gpa": "GPA stands for Grade Point Average. It's a number that shows your overall academic performance, usually on a scale of 0-4 or 0-10 depending on your school system.",
        "explain gpa": "GPA stands for Grade Point Average. It's a number that shows your overall academic performance, usually on a scale of 0-4 or 0-10 depending on your school system.",
        "gpa meaning": "GPA stands for Grade Point Average. It's a number that shows your overall academic performance, usually on a scale of 0-4 or 0-10 depending on your school system.",
        
        # CGPA Questions  
        "what is cgpa": "CGPA stands for Cumulative Grade Point Average. It's your overall academic performance across all semesters or terms.",
        "explain cgpa": "CGPA stands for Cumulative Grade Point Average. It's your overall academic performance across all semesters or terms.",
        "cgpa meaning": "CGPA stands for Cumulative Grade Point Average. It's your overall academic performance across all semesters or terms.",
        "how to calculate cgpa": "CGPA (Cumulative Grade Point Average) is calculated by adding all your grade points and dividing by the number of subjects. For example: (8+9+7+8)/4 = 8.0 CGPA",
        "cgpa calculation": "CGPA (Cumulative Grade Point Average) is calculated by adding all your grade points and dividing by the number of subjects. For example: (8+9+7+8)/4 = 8.0 CGPA",
        
        # Study Tips Questions
        "what are study tips": "Here are some great study tips: 1) Create a study schedule 2) Take regular breaks 3) Find a quiet study space 4) Use active learning techniques 5) Get enough sleep!",
        "give me study tips": "Here are some great study tips: 1) Create a study schedule 2) Take regular breaks 3) Find a quiet study space 4) Use active learning techniques 5) Get enough sleep!",
        "study tips": "Here are some great study tips: 1) Create a study schedule 2) Take regular breaks 3) Find a quiet study space 4) Use active learning techniques 5) Get enough sleep!",
        "how to study": "Here are some great study tips: 1) Create a study schedule 2) Take regular breaks 3) Find a quiet study space 4) Use active learning techniques 5) Get enough sleep!",
        
        # Time Management Questions
        "how to manage time": "Time management tips: 1) Use a planner or calendar 2) Prioritize important tasks 3) Break big tasks into smaller ones 4) Avoid procrastination 5) Set realistic goals",
        "time management": "Time management tips: 1) Use a planner or calendar 2) Prioritize important tasks 3) Break big tasks into smaller ones 4) Avoid procrastination 5) Set realistic goals",
        "time management tips": "Time management tips: 1) Use a planner or calendar 2) Prioritize important tasks 3) Break big tasks into smaller ones 4) Avoid procrastination 5) Set realistic goals",
        
        # Attendance Questions
        "what is attendance": "Attendance is the percentage of classes you attend. Most schools require at least 75% attendance to be eligible for exams.",
        "attendance meaning": "Attendance is the percentage of classes you attend. Most schools require at least 75% attendance to be eligible for exams.",
        "attendance requirements": "Attendance is the percentage of classes you attend. Most schools require at least 75% attendance to be eligible for exams."
    }
    
    # Check if the question exists in our database
    if question in faq_database:
        return faq_database[question]
    else:
        return """I'm sorry, I don't know the answer to that question yet. I'm still learning! 
        
Try asking me about:
• GPA (what is gpa, explain gpa)
• CGPA (what is cgpa, how to calculate cgpa) 
• Study tips (study tips, how to study)
• Time management (time management tips)
• Attendance (what is attendance)

You can ask in different ways - I understand multiple phrasings!"""

def main_chat_loop():
    """
    This is the main part of our chatbot - it keeps the conversation going!
    It's called a 'loop' because it repeats until the student says 'quit'.
    """
    
    # Start with a greeting
    greet_student()
    
    # This loop keeps running until the student wants to quit
    while True:
        # Get input from the student (input() waits for them to type something)
        user_input = input("\n💬 Ask me a question: ")
        
        # Check if they want to quit
        if user_input.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Goodbye! Good luck with your studies!")
            break
        
        # Get the answer for their question
        response = get_faq_response(user_input)
        
        # Show the answer to the student
        print(f"\n🤖 Chatbot: {response}")

# This is where our program starts running
if __name__ == "__main__":
    print("Starting Student Helper Chatbot...")
    main_chat_loop()
