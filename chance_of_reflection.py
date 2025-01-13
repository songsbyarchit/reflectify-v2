import json
import random

# Input JSON data
data = [
    {"topic": "Shadow work and self-reflection", "chance_of_reflection": 0.8},
    {"topic": "Gym routines and progress tracking", "chance_of_reflection": 0.6},
    {"topic": "Calisthenics goals and achievements", "chance_of_reflection": 0.4},
    {"topic": "Cold approach experiences and lessons learned", "chance_of_reflection": 0.3},
    {"topic": "Badminton matches and techniques", "chance_of_reflection": 0.5},
    {"topic": "Local places visited and memorable moments", "chance_of_reflection": 0.7},
    {"topic": "Reflections on friendships and social connections", "chance_of_reflection": 0.75},
    {"topic": "Mindset shifts and personal growth", "chance_of_reflection": 0.9},
    {"topic": "New hobbies explored and impressions", "chance_of_reflection": 0.4},
    {"topic": "Creative writing or storytelling ideas", "chance_of_reflection": 0.25},
    {"topic": "Books read and key takeaways", "chance_of_reflection": 0.5},
    {"topic": "Music practice (singing, instruments) progress", "chance_of_reflection": 0.35},
    {"topic": "Dancing routines or new styles learned", "chance_of_reflection": 0.3},
    {"topic": "Fitness goals and challenges", "chance_of_reflection": 0.6},
    {"topic": "Juggling techniques and progress", "chance_of_reflection": 0.2},
    {"topic": "Whistling techniques or fun experiments", "chance_of_reflection": 0.15},
    {"topic": "Coin flipping tricks mastered or attempted", "chance_of_reflection": 0.1},
    {"topic": "Flexibility or yoga progress and goals", "chance_of_reflection": 0.45},
    {"topic": "Reflections on resilience and overcoming challenges", "chance_of_reflection": 0.8},
    {"topic": "Favorite films or shows and why they resonated", "chance_of_reflection": 0.5},
    {"topic": "Cooking experiments and recipes tried", "chance_of_reflection": 0.35},
    {"topic": "Tech or coding breakthroughs and frustrations", "chance_of_reflection": 0.5},
    {"topic": "Nature walks or hiking experiences", "chance_of_reflection": 0.6},
    {"topic": "Thoughts on relationships and emotional intelligence", "chance_of_reflection": 0.7},
    {"topic": "Meditation or mindfulness practices", "chance_of_reflection": 0.6},
    {"topic": "Work-related achievements or lessons learned", "chance_of_reflection": 0.7},
    {"topic": "Planning and reviewing long-term goals", "chance_of_reflection": 0.75},
    {"topic": "Travel destinations dreamed about or visited", "chance_of_reflection": 0.4},
    {"topic": "Thoughts on society, culture, or philosophy", "chance_of_reflection": 0.6},
    {"topic": "Gratitude journaling and daily highlights", "chance_of_reflection": 0.85},
    {"topic": "Going on a date", "chance_of_reflection": 0.1},
    {"topic": "Flying (flights taken or planned)", "chance_of_reflection": 0.15},
    {"topic": "Hosting or attending events", "chance_of_reflection": 0.2},
    {"topic": "Random acts of kindness experienced or given", "chance_of_reflection": 0.3},
    {"topic": "Dreams and their meanings", "chance_of_reflection": 0.35},
    {"topic": "Pet interactions or funny moments", "chance_of_reflection": 0.3},
    {"topic": "Climbing or bouldering sessions", "chance_of_reflection": 0.15},
    {"topic": "Exploring new restaurants or cafes", "chance_of_reflection": 0.4},
    {"topic": "Playing board games or puzzles", "chance_of_reflection": 0.25},
    {"topic": "Shopping experiences and finds", "chance_of_reflection": 0.3},
    {"topic": "Seasonal changes and weather reflections", "chance_of_reflection": 0.5},
    {"topic": "Family interactions and gatherings", "chance_of_reflection": 0.6},
    {"topic": "Volunteer work or community activities", "chance_of_reflection": 0.2},
    {"topic": "Learning a new language", "chance_of_reflection": 0.25},
    {"topic": "Memories from childhood", "chance_of_reflection": 0.4},
    {"topic": "Random thoughts or epiphanies", "chance_of_reflection": 0.6},
    {"topic": "Art projects or creative endeavors", "chance_of_reflection": 0.3},
    {"topic": "Gardening or plant care", "chance_of_reflection": 0.2},
    {"topic": "Gaming experiences and achievements", "chance_of_reflection": 0.4},
    {"topic": "Reflections on health and wellness", "chance_of_reflection": 0.7},
    {"topic": "Revisiting old journal entries", "chance_of_reflection": 0.3},
    {"topic": "Unexpected challenges faced", "chance_of_reflection": 0.5},
    {"topic": "Online interactions or social media experiences", "chance_of_reflection": 0.35},
    {"topic": "Financial goals and budgeting reflections", "chance_of_reflection": 0.4},
    {"topic": "Photography or videography adventures", "chance_of_reflection": 0.3},
    {"topic": "Spiritual practices or beliefs", "chance_of_reflection": 0.5},
    {"topic": "Learning about history or current events", "chance_of_reflection": 0.4},
    {"topic": "Random curiosities explored", "chance_of_reflection": 0.5},
    {"topic": "Online courses or skills learned", "chance_of_reflection": 0.3},
    {"topic": "Weekend plans or reflections", "chance_of_reflection": 0.55},
    {"topic": "Networking or professional growth", "chance_of_reflection": 0.4},
    {"topic": "Reconnecting with old friends", "chance_of_reflection": 0.3},
    {"topic": "Surprises or serendipitous moments", "chance_of_reflection": 0.4},
    {"topic": "Experimenting with fashion or style", "chance_of_reflection": 0.3},
    {"topic": "First experiences or trying new things", "chance_of_reflection": 0.5},
    {"topic": "Personal victories or achievements", "chance_of_reflection": 0.6},
    {"topic": "Moments of pure joy or laughter", "chance_of_reflection": 0.7},
    {"topic": "Unexpected inspirations or creative ideas", "chance_of_reflection": 0.55},
    {"topic": "Celebrations or special occasions", "chance_of_reflection": 0.3},
    {"topic": "Relaxation or self-care rituals", "chance_of_reflection": 0.6},
    {"topic": "Reflections on gratitude and privilege", "chance_of_reflection": 0.65},
    {"topic": "Late-night thoughts or reflections", "chance_of_reflection": 0.5},
    {"topic": "Journaling about journaling", "chance_of_reflection": 0.2},
    {"topic": "Exploring technology or gadgets", "chance_of_reflection": 0.35},
    {"topic": "Reflections on a recent purchase", "chance_of_reflection": 0.3},
    {"topic": "Thoughts on overcoming fears", "chance_of_reflection": 0.4},
    {"topic": "Reflections on love and intimacy", "chance_of_reflection": 0.5},
    {"topic": "Sustainability efforts or eco-friendly choices", "chance_of_reflection": 0.25},
    {"topic": "Personal struggles and how to address them", "chance_of_reflection": 0.55},
    {"topic": "Travel stories or aspirations", "chance_of_reflection": 0.45},
    {"topic": "Learning from mentors or role models", "chance_of_reflection": 0.4},
    {"topic": "Reflections on productivity habits", "chance_of_reflection": 0.6},
    {"topic": "Reflections on past mistakes and lessons", "chance_of_reflection": 0.7},
    {"topic": "Thoughts on kindness and humanity", "chance_of_reflection": 0.5},
    {"topic": "Dealing with setbacks or failures", "chance_of_reflection": 0.55},
    {"topic": "Reflections on identity and self-discovery", "chance_of_reflection": 0.65},
    {"topic": "Pondering the future and ambitions", "chance_of_reflection": 0.8},
    {"topic": "Navigating complex emotions", "chance_of_reflection": 0.7},
    {"topic": "Reflections on time management", "chance_of_reflection": 0.5},
    {"topic": "Exploring art or visiting galleries", "chance_of_reflection": 0.3},
    {"topic": "Thoughts on family traditions", "chance_of_reflection": 0.4},
    {"topic": "Moments of nostalgia", "chance_of_reflection": 0.5},
    {"topic": "Personal mission or values", "chance_of_reflection": 0.2}
]

# Function to round to 2 significant figures
def round_to_sf(value, sf=2):
    return round(value, sf - int(f"{value:.1e}".split('e')[1]) - 1)

# Process the data
for entry in data:
    original_chance = entry["chance_of_reflection"]
    new_chance = original_chance / 3
    entry["chance_of_reflection"] = round_to_sf(new_chance)

# Save the modified data to a new JSON file
output_file_path = 'chance_of_reflection_2.json'
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)