import random
import json
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
import os
import logging
import re
import unicodedata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("chance_of_reflection.json", "r") as file:
    topics = json.load(file)

categories = {
    "friends": ["Alice", "Jack", "Sophie", "Ryan", "Emily", "Tom", "Lucy", "James"],
    "family": ["Mum", "Dad", "Aunt Mary", "Uncle John", "Grandpa Joe", "Grandma Helen", "Cousin Sarah"],
    "gym_partners": ["Dan", "Jake", "Megan", "Liam", "Zara"],
    "colleagues": ["Michael", "Sarah", "Daniel", "Kate", "Olivia"],
    "neighbours": ["Mr. Smith", "Mrs. Brown", "Andy", "Claire"],
    "hobby_groups": ["Mark", "Emma", "Charlie", "Rebecca", "Tommy"],
    "mentors": ["Dr. Adams", "Professor Green", "Coach Taylor"],
    "pets": ["Buddy the dog", "Mittens the cat", "Goldie the fish"],
    "strangers": ["A kind barista", "A helpful stranger"],
    "online_friends": ["GamerX99", "CraftyCoder", "MusicLover"],
}

category_probabilities = {
    "friends": 0.4,
    "family": 0.3,
    "gym_partners": 0.2,
    "colleagues": 0.2,
    "neighbours": 0.1,
    "hobby_groups": 0.15,
    "mentors": 0.05,
    "pets": 0.1,
    "strangers": 0.1,
    "online_friends": 0.1,
}

start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 1, 31)
current_date = start_date

dataset = []

available_names = [
    "Abigail", "Adeline", "Alexa", "Alexandra", "Alyssa", "Anastasia", "Andrea", "Angelina", 
    "Anna", "Ariana", "Aubrey", "Autumn", "Avery", "Bailey", "Bella", "Brianna", "Brittany", 
    "Brooke", "Camila", "Cassandra", "Catherine", "Cecilia", "Charlotte", "Chloe", "Clara", 
    "Daisy", "Delilah", "Diana", "Eliana", "Elizabeth", "Ella", "Eleanor", "Elena", "Eloise", 
    "Elsa", "Evangeline", "Faith", "Fiona", "Gabriella", "Genevieve", "Georgia", "Gianna", 
    "Grace", "Hadley", "Hailey", "Hannah", "Harper", "Hazel", "Isabelle", "Ivy", "Jade", 
    "Jasmine", "Josephine", "Juliet", "June", "Kaitlyn", "Kayla", "Kennedy", "Kimberly", 
    "Laila", "Layla", "Leah", "Lila", "Liliana", "Lillian", "Lily", "Lola", "London", 
    "Mackenzie", "Madeline", "Madison", "Margaret", "Maria", "Mariah", "Melanie", 
    "Molly", "Naomi", "Natalia", "Natalie", "Nora", "Penelope", "Peyton", "Piper", 
    "Rachel", "Raelynn", "Reagan", "Rosalie", "Ruby", "Savannah", "Scarlett", 
    "Serena", "Sienna", "Skylar", "Sophia", "Stella", "Sydney", "Taylor", 
    "Trinity", "Valeria", "Valerie", "Victoria", "Violet", "Vivian", "Zara", "Zoe"
]

daily_metrics = {
    "relationship_status": {"status": "single", "partner_name": None}
}

def generate_status_context(daily_metrics):
    status_contexts = []
    relationship_status = daily_metrics.get("relationship_status", {}).get("status", "single")
    # Default to "single" if no previous status exists
    prompt_output = ""

    # Relationship Status (70% chance to be mentioned)
    if random.random() < 0.7:
        if relationship_status == "dating":
            # Assign a partner name if not already assigned
            partner_name = daily_metrics.get("relationship_status", {}).get("partner_name")
            if not partner_name:
                partner_name = random.choice(available_names)
                available_names.remove(partner_name)

            went_on_date = random.random() < 0.15  # 15% chance of going on a date today
            if went_on_date:
                date_went_well = random.random() < 0.6  # 60% chance the date went well
                if date_went_well:
                    future_date_planned = random.random() < 0.6  # 60% chance of planning another date
                    prompt_output = f"You went on a date with {partner_name} today, and it went well! You might plan another soon. Be sure to write about how the date went in your transcript. You MUST mention {partner_name}'s name in the transcript."
                else:
                    breakup = random.random() < 0.65  # 65% chance of a breakup after a bad date
                    if breakup:
                        relationship_status = "single"
                        partner_name = None
                        prompt_output = f"You went on a date with {partner_name} today, but it didn't go well, and you decided to move on. Reflect on what happened and include it in your journal. You MUST mention {partner_name}'s name in the transcript."
                    else:
                        prompt_output = f"You went on a date with {partner_name} today, but it didn't go as expected. No hard feelings. Include how you felt in your transcript. You MUST mention {partner_name}'s name in the transcript."
            else:
                actively_dating = random.random() < 0.5  # 50% chance of actively dating
                if actively_dating:
                    prompt_output = f"You didn't go on a date today, but you're still seeing {partner_name} and spent time chatting or swiping. Reflect on your thoughts about this in your journal. You MUST mention {partner_name}'s name in the transcript."
                else:
                    prompt_output = f"You didn't go on a date today and aren't actively looking right now. You're still seeing {partner_name}. Be sure to reflect on your feelings in your journal. You MUST mention {partner_name}'s name in the transcript."

        elif relationship_status == "single":
            partner_name = None  # Explicitly set partner_name to None
            start_dating = random.random() < 0.2  # 20% chance of starting to date
            if start_dating:
                relationship_status = "dating"
                prompt_output = "You've decided to start dating again! Today, you set up a profile or reached out to someone."
            else:
                prompt_output = "You spent some time reflecting on being single and enjoying your independence."

        elif relationship_status == "in a relationship":
            # Assign a partner name if not already assigned
            partner_name = daily_metrics.get("relationship_status", {}).get("partner_name")
            if not partner_name:
                partner_name = random.choice(available_names)
                available_names.remove(partner_name)
            had_conflict = random.random() < 0.3  # 30% chance of conflict today
            if had_conflict:
                breakup = random.random() < 0.2  # 20% chance of a breakup after conflict
                if breakup:
                    relationship_status = "single"
                    partner_name = None
                    prompt_output = f"You had a significant conflict with {partner_name} today, and it ended your relationship. Reflect on how this happened and write about it in your journal. You MUST mention {partner_name}'s name in the transcript."
                else:
                    prompt_output = f"You had a disagreement with {partner_name} today, but you resolved it and moved forward. Write about how you handled this conflict in your transcript. You MUST mention {partner_name}'s name in the transcript."
            else:
                special_moment = random.random() < 0.4  # 40% chance of a special moment
                if special_moment:
                    prompt_output = f"You shared a meaningful moment with {partner_name} today. Write about what made it special in your transcript. You MUST mention {partner_name}'s name in the transcript."
                else:
                    prompt_output = f"It was a calm day in your relationship with {partner_name}, with no major events. Reflect on how you feel about your partner in your journal. You MUST mention {partner_name}'s name in the transcript."

        # Update daily_metrics with a defined partner_name
        daily_metrics["relationship_status"] = {"status": relationship_status, "partner_name": partner_name}
        status_contexts.append(prompt_output)
    
    else:
        pass

        # Physical Health (70% chance to be mentioned)
    if random.random() < 0.7:
        physical_health = random.choice(["excellent", "good", "okay", "poor"])
        prompt_output = f"Today, your physical health was {physical_health}. Reflect on how this affected your day in your journal."
        status_contexts.append(prompt_output)
        daily_metrics["physical_health"] = {"status": physical_health}
    else:
        pass

    # Emotional State (70% chance to be mentioned)
    if random.random() < 0.7:
        emotional_state = random.choice(["happy", "calm", "anxious", "sad", "excited", "stressed"])
        if emotional_state in ["happy", "calm", "excited"]:
            reason_for_emotion = random.choice(["good news", "achievement", "positive interaction", "pleasant surprise", "feeling appreciated"])
        elif emotional_state in ["anxious", "sad", "stressed"]:
            reason_for_emotion = random.choice(["workload", "personal concerns", "negative feedback", "conflict with someone", "disappointment"])
        prompt_output = f"Emotionally, you felt {emotional_state} today due to {reason_for_emotion}. Write about how this emotion shaped your day in your journal."
        status_contexts.append(prompt_output)
        daily_metrics["emotional_state"] = {"state": emotional_state, "reason": reason_for_emotion}
    else:
        pass        

    return status_contexts

def clean_text(text):
    # Normalize text to replace Unicode characters with ASCII equivalents
    text = unicodedata.normalize("NFKD", text)
    # Replace smart quotes, dashes, and ellipses
    text = text.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2014', '—').replace('\u2013', '-').replace('\u2026', '...')
    # Normalize spaces
    text = ' '.join(text.split())  # Removes extra spaces and normalizes whitespace
    return text

while current_date <= end_date:
    logger.info(f"Processing date: {current_date.strftime('%Y-%m-%d')} ({len(dataset) + 1}/{(end_date - start_date).days + 1})")
    num_entries = max(0, min(5, int(random.gauss(2, 1))))
    entries = []

    for _ in range(num_entries):
        timestamp = current_date + timedelta(
            hours=random.randint(6, 22),
            minutes=random.randint(0, 59)
        )
        included_topics = [
            topic["topic"]
            for topic in topics
            if random.random() < topic["chance_of_reflection"]
        ]

        mentioned_names = []

        for category, names in categories.items():
            if random.random() < category_probabilities[category]:
                # Start by adding one name
                mentioned_names.append(random.choice(names))
                
                # Continue adding more names with decreasing probability
                additional_probability = category_probabilities[category]
                while random.random() < additional_probability:
                    # Avoid duplicates by selecting from the remaining names
                    remaining_names = [name for name in names if name not in mentioned_names]
                    if not remaining_names:
                        break  # Exit if no more names are available
                    mentioned_names.append(random.choice(remaining_names))
                    additional_probability *= category_probabilities[category]  # Reduce the probability

        tone_assignment = {
            topic: random.choice(["positive", "negative", "mixed"])
            for topic in included_topics
        }

        word_count = max(50, min(500, int(random.gauss(200, 75))))
        tone_details = "\n".join(
            [f"- {topic}: {tone}" for topic, tone in tone_assignment.items()]
        )

        negative_topics = [topic for topic, tone in tone_assignment.items() if tone == "negative"]
        positive_topics = [topic for topic, tone in tone_assignment.items() if tone == "positive"]
        mixed_topics = [topic for topic, tone in tone_assignment.items() if tone == "mixed"]

        tone_sentence = []
        if negative_topics:
            tone_sentence.append(
                f"On this day, you MUST speak NEGATIVELY about: {', '.join(negative_topics)}. Examples include feelings of frustration, disappointment, sadness, or regret regarding these topics."
            )
        if positive_topics:
            tone_sentence.append(
                f"On this day, you MUST speak POSITIVELY about: {', '.join(positive_topics)}. Examples include moments of joy, pride, excitement, or gratitude regarding these topics."
            )
        if mixed_topics:
            tone_sentence.append(
                f"On this day, you MUST speak with MIXED EMOTIONS about: {', '.join(mixed_topics)}. Examples include feeling worried or anxious at first but relieved later, appreciating something while regretting another aspect, or balancing feelings of gratitude with mild disappointment."
            )

        status_contexts = generate_status_context(daily_metrics)
        status_descriptions = " ".join(status_contexts) if status_contexts else "\n"

        prompt = (
            f"You MUST write a transcript in British English, as if spoken by a 22-year-old man living in Sheffield, UK. The language MUST reflect the natural tone and reading level of someone navigating early adulthood, balancing work, hobbies like badminton and fitness, and maintaining relationships with friends, family, and colleagues, in first person.\n\n"
            f"The date is {timestamp.strftime('%A, %d %B %Y')}. Take into consideration British Weather at this time of year.\n\n"
            f"Start by reflecting on the following personal metrics: {status_descriptions}\n\n"
            f"The entry MUST follow these tone instructions: {' '.join(tone_sentence)}. "
            f"Integrate interactions into the narrative with the following people. Ensure their actions, conversations, or significance to the day are contextually woven into the story, without necessarily mentioning their role directly: {', '.join(mentioned_names)}. "
            f"The entry must be exactly {word_count} words long."
        )

        if random.random() < 0.2:
            day_inclusion = "DO mention the day of the week in the transcript."
        else:
            day_inclusion = "DON'T mention the day of the week in the transcript."
        # Append the decision to the prompt
        prompt += f" {day_inclusion}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant helping generate casual, natural journal transcripts for a 22-year-old. Use conversational, voice-memo-like language instead of formal writing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            journal_entry = response["choices"][0]["message"]["content"].strip()
            journal_entry = clean_text(journal_entry)
            print(f"Generated Transcript: {journal_entry}\n")
        except Exception as e:
            journal_entry = f"Error generating entry: {e}"

        entries.append({"timestamp": timestamp.isoformat(), "entry": journal_entry})
        logger.info(f"Generating entry {_ + 1}/{num_entries} for {current_date.strftime('%Y-%m-%d')}")

    dataset.append({"date": current_date.isoformat(), "entries": entries})
    current_date += timedelta(days=1)

output_file = "journal_dataset_with_tone.json"
with open(output_file, "w") as file:
    json.dump(dataset, file, indent=4)

print(f"Dataset generated and saved to {output_file}")