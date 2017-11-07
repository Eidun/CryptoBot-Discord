def get_role(invites: int):
    if invites >= 200:
        return 'Command Chief Master Sergeant'
    if invites >= 100:
        return 'Starship Master Sergeant'
    if invites >= 50:
        return 'Senior Astronaut'
    if invites >= 25:
        return 'Astronaut'
    if invites >= 10:
        return 'Pilot'
    if invites >= 1:
        return 'Ground control'
    return None
