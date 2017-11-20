def get_role(invites: int):
    if invites >= 100:
        return 'Rank1'
    if invites >= 50:
        return 'Rank2'
    if invites >= 10:
        return 'Rank3'
    if invites >= 5:
        return 'Rank4'
    if invites >= 3:
        return 'Rank5'
    if invites >= 1:
        return 'Rank6'
    return None


def get_next_role(invites: int):
    if invites < 1:
        return 'Rank6', 1
    if invites < 3:
        return 'Rank5', 3
    if invites < 5:
        return 'Rank4', 5
    if invites < 10:
        return 'Rank3', 10
    if invites < 50:
        return 'Rank2', 50
    if invites < 100:
        return 'Rank1', 100
    return 'Maximum rank', 0
