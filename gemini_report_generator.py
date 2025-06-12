import google.generativeai as genai
import json
from config import GEMINI_API_KEY, GEMINI_MODEL

# Initialize the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel(GEMINI_MODEL)

def take_input():
    userInput = input("Enter your query: ")

    prompt = f"""
    Please filter out 3 entities namely football team 1, team 2 and date of the match, from the message below:
    {userInput}
    If there's no date mentioned, consider it NA. Use calendar if required. Your output must contain exactly three entities: team1, team2 and date (in YYYY-MM-DD form), in the format below:
    The football team name should be complete even if there's a short form in user prompt

    team1:
    team2:
    date:
    """

    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().splitlines()

        team1 = ""
        team2 = ""
        date = ""

        for line in lines:
            if line.lower().startswith("team1:"):
                team1 = line.split(":", 1)[1].strip()
            elif line.lower().startswith("team2:"):
                team2 = line.split(":", 1)[1].strip()
            elif line.lower().startswith("date:"):
                date = line.split(":", 1)[1].strip()

        return team1, team2, date

    except Exception as e:
        print("Something went wrong:", e)
        return None, None, None



def generate_match_report(match_info_file, team_stats_file, performance_file, key_events_file):
    # Read the match info, team stats, and performance summary from the text files
    with open(match_info_file, 'r', encoding='utf-8') as f:
        match_info = f.read()

    with open(team_stats_file, 'r', encoding='utf-8') as f:
        team_stats = f.read()

    with open(performance_file, 'r', encoding='utf-8') as f:
        player_performance = f.read()

    with open(key_events_file, 'r', encoding='utf-8') as f:
        key_events = f.read()

    # Combine all the data into a single prompt for the Gemini model
    prompt = f"""
    Please generate a detailed and engaging football match report based on the following data:

    Match Information:
    {match_info}

    Team Statistics:
    {team_stats}

    Player Performance Summary:
    {player_performance}

    Key Events:
    {key_events}

    The report should be concise, precise, and interesting.
    Also, At then end of the report, add the overall scorline and the best player and also the key battle in one line each
    """

    try:
        response = model.generate_content(prompt)

        with open('generated_match_report.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)

        print("Match report generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


generate_match_report(
    "match_info.txt",
    "team_stats_comparison.txt",
    "player_performance_summary.txt",
    "key_match_events.txt")