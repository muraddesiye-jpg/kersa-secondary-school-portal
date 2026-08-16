import re
import random
from datetime import datetime

class MuradAI:
    """Murad's AI Assistant - Ethical AI for Education"""
    
    def __init__(self):
        self.name = "Murad's AI"
        self.version = "1.0.0"
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """Load knowledge base for different subjects"""
        return {
            'mathematics': {
                'keywords': ['math', 'mathematics', 'algebra', 'geometry', 'calculus', 'number'],
                'tips': [
                    "Mathematics is about understanding patterns. Focus on concepts, not memorization.",
                    "Practice regularly - solve at least 5 problems daily.",
                    "Draw diagrams for geometry problems.",
                    "Check your work step by step.",
                    "Use real-life examples to understand abstract concepts."
                ],
                'topics': ['Algebra', 'Geometry', 'Trigonometry', 'Calculus', 'Statistics']
            },
            'english': {
                'keywords': ['english', 'grammar', 'writing', 'reading', 'literature', 'essay'],
                'tips': [
                    "Read books, articles, and newspapers daily.",
                    "Practice writing essays regularly.",
                    "Learn 5 new vocabulary words every day.",
                    "Watch English content with subtitles.",
                    "Join English discussion groups."
                ],
                'topics': ['Grammar', 'Composition', 'Comprehension', 'Literature', 'Vocabulary']
            },
            'physics': {
                'keywords': ['physics', 'motion', 'force', 'energy', 'electricity', 'magnet'],
                'tips': [
                    "Understand the fundamental laws first.",
                    "Draw free-body diagrams for force problems.",
                    "Practice numerical problems regularly.",
                    "Connect concepts to real-world phenomena.",
                    "Use simulations to visualize abstract concepts."
                ],
                'topics': ['Mechanics', 'Thermodynamics', 'Optics', 'Electricity', 'Magnetism']
            },
            'chemistry': {
                'keywords': ['chemistry', 'chemical', 'reaction', 'element', 'compound', 'acid'],
                'tips': [
                    "Memorize the periodic table gradually.",
                    "Practice balancing chemical equations daily.",
                    "Understand reaction mechanisms.",
                    "Use mnemonics for memorization.",
                    "Perform safe experiments when possible."
                ],
                'topics': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Analytical Chemistry']
            },
            'biology': {
                'keywords': ['biology', 'cell', 'organism', 'plant', 'animal', 'genetics', 'dna'],
                'tips': [
                    "Draw and label diagrams regularly.",
                    "Create flowcharts for processes.",
                    "Use mnemonics for classification.",
                    "Relate concepts to everyday life.",
                    "Practice with past exam questions."
                ],
                'topics': ['Cell Biology', 'Genetics', 'Ecology', 'Human Anatomy', 'Botany']
            }
        }
    
    def get_response(self, message):
        """Generate response based on user input"""
        msg = message.lower().strip()
        
        # Greetings
        if self._contains_any(msg, ['salam', 'hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return self._greeting_response()
        
        # Motivation
        if self._contains_any(msg, ['motivat', 'encourage', 'inspire', 'hopeless', 'give up', 'tired']):
            return self._motivation_response()
        
        # Study tips
        if self._contains_any(msg, ['study', 'learn', 'focus', 'concentrate', 'revision']):
            return self._study_tips_response()
        
        # Exam preparation
        if self._contains_any(msg, ['exam', 'test', 'assessment', 'prepare']):
            return self._exam_preparation_response()
        
        # Subject-specific responses
        for subject, data in self.knowledge_base.items():
            if self._contains_any(msg, data['keywords']):
                return self._subject_response(subject, data)
        
        # Ethics
        if self._contains_any(msg, ['ethic', 'honest', 'integrity', 'cheat', 'copy', 'plagiar']):
            return self._ethics_response()
        
        # Career guidance
        if self._contains_any(msg, ['career', 'future', 'job', 'profession', 'university']):
            return self._career_response()
        
        # Default response
        return self._default_response()
    
    def answer_question(self, question):
        """Answer specific academic questions"""
        q = question.lower().strip()
        
        # Math questions
        if self._contains_any(q, ['math', 'algebra', 'equation']):
            return "To solve algebraic equations: 1) Identify the variable, 2) Isolate the variable on one side, 3) Perform inverse operations, 4) Check your answer. What specific equation do you need help with?"
        
        # Science questions
        if self._contains_any(q, ['physics', 'chemistry', 'biology', 'science']):
            return "Science is about understanding the natural world. Start with fundamental principles, then apply them to specific problems. What specific topic are you studying?"
        
        # Language questions
        if self._contains_any(q, ['english', 'grammar', 'writing']):
            return "For English improvement: practice reading daily, write regularly, and focus on grammar rules. What specific aspect do you need help with?"
        
        return self.get_response(question)
    
    def _contains_any(self, text, keywords):
        """Check if text contains any of the keywords"""
        return any(keyword in text for keyword in keywords)
    
    def _greeting_response(self):
        greetings = [
            "Wa Alaikum Assalam! 😊 I'm Murad's AI Assistant. How can I help you with your studies today?",
            "Hello! Welcome! I'm here to support your educational journey. What would you like to learn today?",
            "Assalamu Alaikum! It's great to see you! Feel free to ask me anything about your studies."
        ]
        return random.choice(greetings)
    
    def _motivation_response(self):
        motivations = [
            "🌟 Remember: Every expert was once a beginner. Your hard work today will become your success story tomorrow. Keep pushing forward!",
            "💪 You have the power to achieve greatness. Challenges are opportunities in disguise. Believe in yourself!",
            "🎯 Success is not final, failure is not fatal. It's the courage to continue that counts. You've got this!",
            "📚 Education is the most powerful weapon you can use to change the world. Keep learning, keep growing!",
            "✨ Your dreams are valid. Work hard in silence and let your success make the noise."
        ]
        return random.choice(motivations)
    
    def _study_tips_response(self):
        tips = [
            "📚 Effective Study Tips:\n\n1. Use the Pomodoro Technique: 25 minutes study, 5 minutes break\n2. Create a dedicated study space\n3. Review notes within 24 hours\n4. Teach others to reinforce learning\n5. Use active recall techniques\n6. Take regular breaks\n7. Stay hydrated and well-rested\n\nWould you like specific tips for a particular subject?"
        ]
        return random.choice(tips)
    
    def _exam_preparation_response(self):
        return """📝 Exam Preparation Strategy:

1. **Start Early**: Begin preparing at least 2 weeks before
2. **Create a Schedule**: Allocate specific times for each subject
3. **Practice Past Papers**: Understand exam format
4. **Make Summary Notes**: Condense key concepts
5. **Group Study**: Discuss with classmates
6. **Stay Healthy**: Get enough sleep and exercise
7. **Stay Positive**: Believe in your preparation

Remember: Proper preparation prevents poor performance! 💪"""
    
    def _subject_response(self, subject, data):
        tips = random.choice(data['tips'])
        topics = ', '.join(data['topics'][:3])
        return f"""📖 {subject.title()} Study Guide:

**Tips:**
{tips}

**Key Topics:**
{topics}

Would you like detailed help with any specific topic?"""
    
    def _ethics_response(self):
        return """🤝 Academic Integrity Matters:

**Always:**
✅ Do your own work
✅ Give credit to sources
✅ Ask for help when needed
✅ Report academic dishonesty
✅ Support classmates honestly

**Never:**
❌ Cheat on exams
❌ Plagiarize
❌ Copy homework
❌ Share answers during tests

Remember: Your integrity is worth more than any grade!"""
    
    def _career_response(self):
        return """🎯 Career Guidance:

**Steps to Success:**
1. Identify your interests and strengths
2. Research different career paths
3. Focus on relevant subjects
4. Develop soft skills
5. Seek mentorship
6. Set short and long-term goals

**Popular Fields:**
- Medicine & Healthcare
- Engineering & Technology
- Business & Finance
- Education & Teaching
- Law & Public Service
- Computer Science & IT

What field are you interested in?"""
    
    def _default_response(self):
        responses = [
            "That's a great question! I'm here to help you with your studies. Could you please be more specific?",
            "I'd love to help you with that! Could you provide more details about your question?",
            "Interesting topic! Let me help you explore that further. What specifically would you like to know?",
            "I'm here to support your learning journey. Could you elaborate on your question?"
        ]
        return random.choice(responses)
