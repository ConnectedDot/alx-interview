def canUnlockAll(boxes):
    unlocked = [False] * len(boxes)
    unlocked[0] = True
    keys = set(boxes[0])
    
    while keys:
        new_keys = set()
        for key in keys:
            if key < len(boxes) and not unlocked[key]:
                unlocked[key] = True
                new_keys.update(boxes[key])
        keys = new_keys
    
    return all(unlocked)