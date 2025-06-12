from agents.match_event_extractor import (
    get_team_id, get_latest_head_to_head, get_goal_scorers,
    get_key_events, get_player_performance_summary, get_team_statistics
)
from gemini_report_generator import generate_match_report, take_input


def user_head_to_head_query():
    team_a, team_b, date = take_input()
    print(team_a, team_b, date)
    team1_id = get_team_id(team_a)
    team2_id = get_team_id(team_b)

    print(f"Team A ID: {team1_id}, Team B ID: {team2_id}")

    if not team1_id or not team2_id:
        print("One or both team names are invalid.")
        return

    match = get_latest_head_to_head(team1_id, team2_id, date)
    if match:
        f = match['fixture']
        t = match['teams']
        g = match['goals']
        with open("match_info.txt", "w", encoding="utf-8") as f_out:
            f_out.write(f"{t['home']['name']} {g['home']} - {g['away']} {t['away']['name']} on {f['date'][:10]}")

        fixture_id = f['id']
        
                # Fetch goal scorers
        goal_scorers = get_goal_scorers(fixture_id)
        with open("goal_scorer_info.txt", "w", encoding="utf-8") as f_out:
            if goal_scorers:
                f_out.write("Goal Scorers:\n")
                for goal in goal_scorers:
                    f_out.write(f"- {goal['player']} ({goal['team']}) - {goal['minute']} min\n")
                    f_out.write(f"  Type: {goal['detail']}\n")
                    f_out.write(f"  Assist: {goal['assist']}\n")
                    f_out.write(f"  Comment: {goal['comment']}\n\n")
            else:
                f_out.write("No goal scorers found.\n")

    else:
        print("No match found.")

    # Fetch cards and missed events
    key_events = get_key_events(fixture_id)
    with open("key_match_events.txt", "w", encoding="utf-8") as f_out:
        if key_events:
            f_out.write("Important Match Events:\n")
            for event in key_events:
                f_out.write(f"- {event['event_type']} ({event['detail']})\n")
                f_out.write(f"  Player: {event['player']} ({event['team']})\n")
                f_out.write(f"  Minute: {event['minute']}\n")
                f_out.write(f"  Comment: {event['comment']}\n\n")
        else:
            f_out.write("No key match events found.\n")

    
    # Player Performance Summary
    performance = get_player_performance_summary(fixture_id)
    with open("player_performance_summary.txt", "w", encoding='utf-8') as file:
        file.write("Player Performance Summary:\n")
        for p in performance:
            file.write(
                f"{p['name']} ({p['team']}): Rating: {p['rating']}, "
                f"Goals: {p['goals']}, Assists: {p['assists']}, Shots: {p['shots']}, "
                f"Passes: {p['passes']}, Tackles: {p['tackles']}\n"
            )

    # Team Statistics Comparison
    team_stats = get_team_statistics(fixture_id)
    with open("team_stats_comparison.txt", "w", encoding='utf-8') as file:
        file.write("Team Stats Comparison:\n")
        for team in team_stats:
            file.write(f"\n{team['team']['name']}:\n")
            for stat in team['statistics']:
                file.write(f"{stat['type']}: {stat['value']}\n")
    
    generate_match_report(
        "match_info.txt",
        "team_stats_comparison.txt",
        "player_performance_summary.txt",
        "key_match_events.txt")

if __name__ == "__main__":

    while(1):
        user_head_to_head_query()
        