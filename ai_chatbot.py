# Student Helper Chatbot - Milestone 2: FREE AI-Powered Version
# This version uses completely FREE AI models that run on your computer!

import warnings
warnings.filterwarnings("ignore")  # Hide technical warnings for cleaner output

def greet_student():
    """
    Shows a welcome message for our AI-powered chatbot
    """
    print("🤖 Hello! I'm your AI-Powered Student Helper!")
    print("I can understand natural language and help with any student questions!")
    print("Ask me anything like:")
    print("- Calculate my CGPA with these grades...")
    print("- Explain photosynthesis in simple terms")
    print("- Give me tips for exam preparation")
    print("- Help me manage my time better")
    print("- Type 'quit' to exit")
    print("-" * 60)

def setup_ai_model():
    """
    Sets up our FREE AI model (this might take a moment the first time)
    """
    try:
        print("🔄 Loading AI brain... (this might take 30 seconds the first time)")
        
        from transformers import pipeline
        
        # This creates our AI "brain" using a free model designed for conversations
        # It's like having a mini ChatGPT running on your computer!
        chatbot_ai = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-small",  # Free conversational AI model
            tokenizer="microsoft/DialoGPT-small"
        )
        
        print("✅ AI brain loaded successfully!")
        return chatbot_ai
        
    except ImportError:
        print("❌ AI libraries not installed yet. Please wait for installation to complete.")
        return None
    except Exception as e:
        print(f"❌ Error loading AI: {e}")
        return None

def get_ai_response(ai_model, user_question, conversation_history=""):
    """
    Gets an intelligent response from our AI model
    """
    if not ai_model:
        return "Sorry, AI is not available right now. Please try again later."
    
    try:
        # Create a student-focused prompt to guide the AI
        student_prompt = f"""You are a helpful student assistant chatbot. Answer student questions clearly and friendly.

Student Question: {user_question}
Answer:"""
        
        # Get AI response
        response = ai_model(student_prompt, max_length=200, num_return_sequences=1, pad_token_id=50256)
        
        # Extract just the answer part
        full_response = response[0]['generated_text']
        answer = full_response.split("Answer:")[-1].strip()
        
        # If the answer is too short or weird, give a fallback response
        if len(answer) < 10 or answer == user_question:
            return get_fallback_response(user_question)
        
        return answer
        
    except Exception as e:
        print(f"AI Error: {e}")
        return get_fallback_response(user_question)

def get_fallback_response(user_question):
    """
    Backup responses when AI isn't working perfectly
    """
    question_lower = user_question.lower()
    
    if "gpa" in question_lower or "grade" in question_lower:
        return "GPA (Grade Point Average) shows your academic performance. To calculate CGPA, add all your grade points and divide by the number of subjects. For example: (8+9+7+8)/4 = 8.0 CGPA"
    
    elif "study" in question_lower or "exam" in question_lower:
        return "Here are proven study tips: 1) Create a study schedule 2) Take breaks every 25-30 minutes 3) Use active recall (test yourself) 4) Study in a quiet environment 5) Get enough sleep before exams!"
    
    elif "time" in question_lower and "manage" in question_lower:
        return "Time management tips: 1) Use a planner 2) Prioritize important tasks 3) Break large tasks into smaller ones 4) Avoid procrastination 5) Set realistic deadlines"
    
    elif "calculate" in question_lower and "cgpa" in question_lower:
        return "To calculate CGPA: 1) Add all your grade points 2) Divide by total number of subjects 3) Example: If you have grades 8, 9, 7, 8 in 4 subjects: (8+9+7+8) ÷ 4 = 8.0 CGPA"
    
    else:
        return f"I understand you're asking about '{user_question}'. While I'm still learning, I can help with GPA calculations, study tips, time management, and academic questions. Could you rephrase your question?"

def main_ai_chat():
    """
    Main chat loop for our AI-powered chatbot
    """
    greet_student()
    
    # Set up the AI (this might take a moment)
    ai_model = setup_ai_model()
    
    if not ai_model:
        print("⚠️ Running in basic mode. AI features will be available once installation completes.")
    
    conversation_history = ""
    
    while True:
        user_input = input("\n💬 Ask me anything: ")
        
        if user_input.lower().strip() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n👋 Goodbye! Keep up the great work with your studies!")
            break
        
        if user_input.strip() == "":
            continue
            
        # Get AI response
        if ai_model:
            response = get_ai_response(ai_model, user_input, conversation_history)
        else:
            response = get_fallback_response(user_input)
        
        print(f"\n🤖 AI Assistant: {response}")
        
        # Keep track of conversation for context
        conversation_history += f"Student: {user_input}\nAssistant: {response}\n"

# Start the chatbot
if __name__ == "__main__":
    print("🚀 Starting AI-Powered Student Helper Chatbot...")
    main_ai_chat()
