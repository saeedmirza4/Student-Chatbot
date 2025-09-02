# 🧪 COMPLETE TESTING GUIDE FOR YOUR STUDENT CHATBOT
# Test every feature systematically to see your chatbot's full potential!

print("🧪 STUDENT CHATBOT - COMPLETE TESTING GUIDE")
print("=" * 60)

print("""
🎯 TESTING STRATEGY:
1. Test each feature category systematically
2. Try edge cases and different phrasings
3. Verify data persistence
4. Test error handling
5. Explore AI-like behavior

📋 COPY AND PASTE THESE COMMANDS ONE BY ONE:
""")

print("🔥 PHASE 1: BASIC FUNCTIONALITY TESTS")
print("-" * 40)
print("""
# Basic help and navigation
help
what can you do
show me commands

# Test case sensitivity and variations
HELP
Help Me
what are all the commands
""")

print("\n📚 PHASE 2: SUBJECT TRACKING TESTS")
print("-" * 40)
print("""
# Add different subjects with various grades
add subject Mathematics grade 8.5
add subject Physics grade 9.2
add subject Chemistry grade 7.8
add subject Computer Science grade 9.5
add subject English grade 8.0

# Test different formats
add subject biology grade 6.5
ADD SUBJECT History GRADE 7.2
add subject Art grade 10.0

# View progress after each addition
show my progress
show subjects
list my subjects
my academic progress

# Test edge cases
add subject grade 8.5
add subject Math
add subject Python Programming grade 11.0
add subject Test Subject grade -1.0
add subject Another Subject grade 0.0
""")

print("\n⏰ PHASE 3: REMINDER SYSTEM TESTS")
print("-" * 40)
print("""
# Quick reminders (1-2 minutes to see notifications)
set reminder test notification in 1 minute
set reminder study break in 2 minutes

# Different time formats
set reminder review Physics in 5 minutes
set reminder homework deadline in 10 minutes
set reminder exam prep at 9:00pm
set reminder study group at 2:30pm tomorrow

# Natural language variations
remind me to study Math in 3 minutes
set reminder call professor at 4:00pm
remind me about assignment in 15 minutes

# View reminders
show reminders
my reminders
list all reminders

# Test edge cases
set reminder 
set reminder study
set reminder in 5 minutes
set reminder study at
""")

print("\n🎯 PHASE 4: GOAL SETTING TESTS")
print("-" * 40)
print("""
# Set various goals
set goal study 3 hours daily
set goal complete all assignments this week
set goal improve CGPA to 8.5
set goal read 2 chapters per day
set goal exercise 30 minutes daily

# Different phrasings
goal: finish project by Friday
my goal is to get better grades
target: study consistently

# View goals
show goals
my goals
list my goals
show my targets
""")

print("\n🧮 PHASE 5: CALCULATION TESTS")
print("-" * 40)
print("""
# CGPA calculations with different formats
calculate cgpa with grades 8, 9, 7, 8.5
calculate my cgpa: 8.2, 9.1, 7.8, 8.9, 9.5
find cgpa for grades 6.5, 7.0, 8.5, 9.0
compute cgpa with 9, 8, 7, 6, 8, 9

# Edge cases
calculate cgpa with grades
calculate cgpa with grades 15, 20, 30
calculate cgpa with grades 0, 1, 2
cgpa calculation

# Mixed with subjects
calculate cgpa with grades 8.5, 9.2, 7.8, 9.5, 8.0
""")

print("\n🧠 PHASE 6: AI KNOWLEDGE TESTS")
print("-" * 40)
print("""
# GPA/CGPA knowledge
what is gpa
explain gpa to me
gpa meaning
what does gpa stand for
what is cgpa
difference between gpa and cgpa
explain cgpa

# Study advice
study tips
how to study effectively
give me study advice
best study methods
how can I study better
effective study techniques

# Time management
time management tips
how to manage time
organize my schedule
time management advice
help me with time management

# Exam preparation
exam preparation tips
how to prepare for exams
exam study strategies
test preparation advice
exam tips
""")

print("\n🤪 PHASE 7: EDGE CASES & ERROR HANDLING")
print("-" * 40)
print("""
# Empty inputs
[Press Enter without typing anything]

# Random/unknown inputs
hello there
what's the weather
tell me a joke
how are you
random question
asdfghjkl
12345
!@#$%

# Partial commands
add subject
show
set
goal
reminder

# Wrong formats
add grade subject Math 8.5
subject add Math 8.5 grade
set 5 minutes reminder study

# Boundary testing
add subject VeryLongSubjectNameThatShouldStillWork grade 8.5
set reminder very long reminder text that goes on and on in 1 minute
""")

print("\n🔄 PHASE 8: DATA PERSISTENCE TESTS")
print("-" * 40)
print("""
# After adding data, quit and restart to test persistence
quit

# Then restart with: python final_chatbot.py
# And check if data is still there:
show my progress
show reminders
show goals
""")

print("\n⚡ PHASE 9: STRESS & PERFORMANCE TESTS")
print("-" * 40)
print("""
# Add many subjects quickly
add subject Subject1 grade 8.1
add subject Subject2 grade 8.2
add subject Subject3 grade 8.3
add subject Subject4 grade 8.4
add subject Subject5 grade 8.5

# Set multiple reminders
set reminder task1 in 1 minute
set reminder task2 in 2 minutes
set reminder task3 in 3 minutes
set reminder task4 in 4 minutes

# Rapid commands
show progress
show reminders
show goals
help
study tips
time management
show progress
""")

print("\n🎭 PHASE 10: NATURAL LANGUAGE TESTS")
print("-" * 40)
print("""
# Test conversational ability
Hi, can you help me with my studies?
I need advice on studying
Can you calculate my grades?
What should I do to improve my CGPA?
I'm struggling with time management
How do I prepare for my exams?
Give me some motivation
I want to set some academic goals
Can you remind me about important tasks?
What's the best way to study mathematics?
""")

print("\n🏆 PHASE 11: INTEGRATION TESTS")
print("-" * 40)
print("""
# Combine multiple features
add subject Advanced Math grade 9.0
set reminder review Advanced Math in 3 minutes
set goal master Advanced Math this semester
show my progress
calculate cgpa with grades 9.0, 8.5, 9.2, 8.8
study tips
show reminders
show goals

# Real-world scenarios
add subject Database Systems grade 8.7
set reminder complete DB assignment at 6:00pm
set goal finish all CS courses with 8+ CGPA
show my progress
time management tips
exam preparation tips
""")

print("\n📊 EXPECTED RESULTS CHECKLIST:")
print("-" * 40)
print("""
✅ Subjects should be added and tracked correctly
✅ CGPA should calculate accurately
✅ Reminders should notify at the right time
✅ Data should persist after restart
✅ Goals should be stored and displayed
✅ Help command should show all features
✅ Error messages should be helpful
✅ Natural language should be understood
✅ Edge cases should be handled gracefully
✅ Performance should be smooth
""")

print("\n🎯 BONUS CHALLENGES:")
print("-" * 40)
print("""
# Try to break the system (in a good way!)
- What happens with very long subject names?
- Can you add 100 subjects?
- What if you set reminders for past times?
- How does it handle special characters?
- What about decimal grades like 8.75?
- Can you mix languages? "add subject Math grade 8.5"

# Test the limits
- Set 20 reminders
- Add 50 subjects
- Set 10 goals
- Test with extreme values
""")

print("\n🚀 FINAL CHALLENGE:")
print("-" * 40)
print("""
Try to use it like a real student for 10 minutes:
1. Add your actual subjects and grades
2. Set real study reminders
3. Set genuine academic goals
4. Ask for study advice
5. Calculate your real CGPA
6. Test the reminder notifications

This will show you how useful your chatbot really is! 🎓
""")

print("\n💡 TESTING TIPS:")
print("-" * 40)
print("""
- Copy each command exactly as written
- Wait for responses before next command
- Note any bugs or improvements needed
- Test reminder notifications by waiting
- Try variations of each command
- Check if data saves properly
- Test restart functionality
""")

print("\n🎉 CONGRATULATIONS!")
print("You've built a comprehensive student helper chatbot!")
print("Complete this testing to see your creation's full power! 🚀")
