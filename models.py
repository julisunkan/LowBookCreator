import random

def generate_random_title():
    adjectives = ["Mindful", "Daily", "Creative", "Productive", "Simple", "Elegant", "Serene", "Focused"]
    nouns = ["Journal", "Notebook", "Planner", "Logbook", "Tracker", "Diary", "Sketchbook", "Companion"]
    themes = ["for Success", "of Gratitude", "for Beginners", "Daily Routine", "Personal Growth", "Ideas"]
    
    parts = [random.choice(adjectives), random.choice(nouns)]
    if random.random() > 0.5:
        parts.append(random.choice(themes))
        
    return " ".join(parts)
