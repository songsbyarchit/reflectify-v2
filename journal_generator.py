import random
import json
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
import os
import logging
import re

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
end_date = datetime(2020, 1, 2)
current_date = start_date

dataset = []

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
                mentioned_names.append(random.choice(names))

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

        prompt = (
            f"You MUST write a transcript in British English, as if spoken by a 22-year-old man living in Sheffield, UK. The language MUST reflect the natural tone and reading level of someone navigating early adulthood, balancing work, hobbies like badminton and fitness, and maintaining relationships with friends, family, and colleagues, in first person.\n\n"
            f"The date is {timestamp.strftime('%A, %d %B %Y')}. Take into consideration British Weather at this time of year.\n\n"
            f"The entry MUST follow these tone instructions: {' '.join(tone_sentence)}. "
            f"Integrate interactions into the narrative with the following people. Ensure their actions, conversations, or significance to the day are contextually woven into the story, without necessarily mentioning their role directly: {', '.join(mentioned_names)}. "
            f"The entry must be exactly {word_count} words long."
        )
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
            journal_entry = journal_entry.replace('\u2019', "'")  # Replace smart apostrophe
            journal_entry = journal_entry.replace('\u201c', '"').replace('\u201d', '"')  # Handle smart double quotes
            journal_entry = journal_entry.replace('\u2014', '—')  # Replace em dash
            journal_entry = journal_entry.replace('\u2013', '-')  # Replace en dash
            journal_entry = journal_entry.replace('\u2026', '...')  # Replace ellipsis
            journal_entry = re.sub(r'(?<=[a-zA-Z0-9]),', ', ', journal_entry)  # Ensure space after commas
            journal_entry = re.sub(r'(?<=[a-zA-Z0-9])\.(?=[a-zA-Z])', '. ', journal_entry)  # Ensure space after periods
            journal_entry = re.sub(r'\s+', ' ', journal_entry).strip()  # Normalize whitespace
            print(f"Generated Transcript: {journal_entry}\n")  # Print transcript to console
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