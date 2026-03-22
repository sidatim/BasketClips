def filterSelected(playerEvents, filter, teamEvents):
    filteredEvents = []
    for event in playerEvents:
        if  'shot missed' in filter and event['actionType'] == 'Missed Shot':
            filteredEvents.append(event)
        elif 'shot made' in filter and event['actionType'] == 'Made Shot':
            filteredEvents.append(event)
        elif  'foul' in filter and event['actionType'] == 'Foul':
            filteredEvents.append(event)
        elif 'steal' in filter and "STEAL" in event['description']:
            filteredEvents.append(event)
        elif  'turnover'in filter and event['actionType'] == 'Turnover':
            filteredEvents.append(event)
        elif  'free throw' in filter and event['actionType'] == 'Free Throw':
            filteredEvents.append(event)
    return filteredEvents