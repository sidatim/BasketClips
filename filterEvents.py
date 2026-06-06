
import re
def filterSelected(playerEvents, filter, teamEvents):
    filteredEvents = []
    def flatten_team_events(team_events):
        flat = []
        if not team_events:
            return flat
        for item in team_events:
            if isinstance(item, list):
                flat.extend(item)
            elif isinstance(item, dict):
                flat.append(item)
        return flat

    def safe_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _sort_events(events):
        return sorted(
            events,
            key=lambda ev: (
                str(ev.get('gameId', '')),
                safe_int(ev.get('period', 0)),
                safe_int(ev.get('actionNumber') or ev.get('eventId') or 0),
            ),
        )

    if filter and 'assist' in filter:
        assister_name = playerEvents[0]['playerNameI'] if playerEvents else ''
        assister_last = assister_name.split()[-1] if assister_name else ''
        flat_team = flatten_team_events(teamEvents)
        for ev in flat_team:
            if ev.get('actionType') != 'Made Shot':
                continue
            desc = ev.get('description', '')
            if 'AST' not in desc:
                continue
            assister_patterns = re.findall(r"\(([^)]*AST[^)]*)\)", desc)
            for pattern in assister_patterns:
                if assister_name and assister_name in pattern:
                    filteredEvents.append(ev)
                    break
                if assister_last and assister_last in pattern:
                    filteredEvents.append(ev)
                    break

    for event in playerEvents:
        if  'shot missed' in filter and event['actionType'] == 'Missed Shot':
            filteredEvents.append(event)
        elif 'shot made' in filter and event['actionType'] == 'Made Shot':
            filteredEvents.append(event)
        elif  'foul' in filter and event['actionType'] == 'Foul':
            filteredEvents.append(event)
        elif 'steal' in filter and "STEAL" in event.get('description',''):
            filteredEvents.append(event)
        elif  'turnover'in filter and event['actionType'] == 'Turnover':
            filteredEvents.append(event)
        elif 'free throw' in filter and event['actionType'] == 'Free Throw':
            filteredEvents.append(event)
        elif 'rebound' in filter and event['actionType'] == 'Rebound':
            filteredEvents.append(event)

    return _sort_events(filteredEvents)

