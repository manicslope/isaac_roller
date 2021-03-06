import pyautogui, time, os


def restart_run():
    pyautogui.keyDown('r')
    time.sleep(1)  # Minimum
    pyautogui.keyUp('r')
    time.sleep(1)


def room_direction():
    for direction in ["up", "down", "left", "right"]:
        try:
            pyautogui.locateOnScreen("treasure_room_%s.png" % direction, confidence=.8)
            return direction
        except:
            pass
    return False


def get_from_log():
    log_file = open(u"C:\\Users\\Slope\\Documents\\My Games\\Binding of Isaac Afterbirth+/log.txt", "r")
    items = list()
    # room_type = str()
    for line in log_file.readlines():
        if "Initialized player" in line:
            character = line.split("Subtype ")[1].split()[0]
            if character == "0":
                character = "Isaac"
            elif character == "7":
                character = "Azazel"
        elif "RNG Start Seed" in line:
            items = list()
            curse = False
            # seed = line.split(": ")[1].split(" (")[0]
        elif "Curse of Maze" in line:
            curse = True
        elif "Room " in line and "." in line:
            # print(line)
            room_type = line.split("Room ")[1].split("(")[0]
        elif line not in items and "Adding collectible" in line:
            items.append(line.split("(")[1].split(")")[0])
    log_file.close()
    return {"character": character, "items": set(items),\
            "room_type": room_type, "curse": curse}


def reach_room(direction):
    """
    Possible teleport to another room
    """

    if get_from_log()["curse"]:
        print("Curse")
        return
    params = {"up": "w", "down": "s", "left": "a", "right": "d"}
    if direction in ["up", "down"]:
        while get_from_log()["room_type"].split(".")[0] != "4":
            pyautogui.keyDown(params[direction])
        pyautogui.keyUp(params[direction])
    else:
        while get_from_log()["room_type"].split(".")[0] != "4":
            pyautogui.keyDown(params[direction])
            pyautogui.keyDown("w")
            time.sleep(.1)
            pyautogui.keyUp("w")
        pyautogui.keyUp(params[direction])

    # In the room
    # time.sleep(.5)
    info = get_from_log()
    current_items = info["items"]
    character = info["character"]
    print("Room Type: %s" % info["room_type"])
    """
    Room types
    [+]4.1 sides evade(like)
    [~]4.2 sides fire(half a heart of damage)
    4.3 sides fire
    [~]4.4 evade, fire in corners, damage on fire
    4.7 evade
    4.9 sides evade
    [+]4.12 sides unreachable
    [~]4.15 four fires(half a heart of damage)
    [+]4.16 sides, have to evade
    [+]4.21 two items, left with spikes
    4.25 two items on sides of machine in the center
    [~]4.26 up, sides, a little bit higher than center
    [~]4.27 right, maybe evade
    4.33 four enemies, damage
    4.35, 4.36(1.5 hearts) two enemies, damage
    4.38 two items, a small strafe to the right
    """
    if info["room_type"] in ["4.15", "4.33", "4.35", "4.36"]:
        return
    elif    direction in ["up", "down"] and\
            info["room_type"] in ["4.21", "4.27", "4.38"]:
        strafe = .2
        if info["room_type"] == "4.21":
            strafe = .5
        pyautogui.keyDown("d")
        time.sleep(strafe)  # Depends on a character
        pyautogui.keyUp("d")
        while current_items == get_from_log()["items"]:
            pyautogui.keyDown(params[direction])
        pyautogui.keyUp(params[direction])
        return
    if character == "Isaac":
        if  direction in ["left", "right"] and\
            info["room_type"] in ["4.2", "4.3", "4.5", "4.4", "4.7", "4.9"] or\
            direction == "right" and info["room_type"] == "4.27":
            pyautogui.keyDown("s")
            time.sleep(.3)  # Depends on a character
            pyautogui.keyUp("s")

            pyautogui.keyDown(params[direction])
            time.sleep(.85)  # Depends on a character
            pyautogui.keyUp(params[direction])

            pyautogui.keyDown("w")
            time.sleep(.3)  # Depends on a character
            pyautogui.keyUp("w")

            while current_items == get_from_log()["items"]:
                pyautogui.keyDown(params[direction])
            pyautogui.keyUp(params[direction])
            return
        elif info["room_type"] == "4.12":
            return
        # elif info["room_type"] == "4.15":
        #     pyautogui.keyDown(direction)  # Suppressing fire!!!
            # time.sleep(.3)
        elif    direction in ["left", "right"] and\
                info["room_type"] in ["4.1", "4.16"]:
            pyautogui.keyDown("s")
            time.sleep(.5)  # Depends on a character
            pyautogui.keyUp("s")

            pyautogui.keyDown(params[direction])
            time.sleep(.85)  # Depends on a character
            pyautogui.keyUp(params[direction])
            while current_items == get_from_log()["items"]:
                pyautogui.keyDown("w")
            pyautogui.keyUp("w")
            return
        # elif direction in ["up", "down"] and info["room_type"] == "4.21":
        elif direction in ["left", "right"] and info["room_type"] == "4.26":
            pyautogui.keyDown("w")
            time.sleep(.1)  # Depends on a character
            pyautogui.keyUp("w")
        # For most rooms(if it doesn't have obstacles)
    elif character == "Azazel":
        if direction in ["left", "right"] and\
            info["room_type"] in ["4.2", "4.3"] or\
            direction == "right" and info["room_type"] == "4.27":
            pyautogui.keyDown("s")
            time.sleep(.3)  # Depends on a character
            pyautogui.keyUp("s")

            pyautogui.keyDown(params[direction])
            time.sleep(.7)  # Depends on a character
            pyautogui.keyUp(params[direction])

            pyautogui.keyDown("w")
            time.sleep(.3)  # Depends on a character
            pyautogui.keyUp("w")
            if info["room_type"] != "4.2":
                while current_items == get_from_log()["items"]:
                    pyautogui.keyDown(params[direction])
                pyautogui.keyUp(params[direction])
            return
        elif direction in ["left", "right"] and info["room_type"] == "4.26":
            pyautogui.keyDown("w")
            time.sleep(.1)  # Depends on a character
            pyautogui.keyUp("w")
        elif    direction in ["up", "down"] and\
                info["room_type"] in ["4.21", "4.25", "4.27"]:
            strafe = .2
            if info["room_type"] == "4.21":
                strafe = .5
            elif info["room_type"] == "4.25":
                strafe = .7
            pyautogui.keyDown("d")
            time.sleep(strafe)  # Depends on a character
            pyautogui.keyUp("d")
            while current_items == get_from_log()["items"]:
                pyautogui.keyDown(params[direction])
            pyautogui.keyUp(params[direction])
            return
    while current_items == get_from_log()["items"]:
        pyautogui.keyDown(params[direction])
    pyautogui.keyUp(params[direction])


delay = 3
item_list = ["Mom's Knife", "Magic Mushroom", "Cricket's Head", "Proptosis", "20/20", "Tech X", "Epic Fetus"]
items = {   "Isaac": ["Polyphemus", "Death's Touch"],\
            "Azazel": ["The Ludovico Technique", "Tiny Planet"]}
character = get_from_log()["character"]
item_list += items[character]


def main():
    os.system('mode con: lines=20')
    print("Character: %s\n" % character)
    number_of_runs = 1
    time.sleep(delay)
    while True:
        restart_run()
        print("Run #%s" % number_of_runs)
        direction = room_direction()
        if direction:
            print("Going %s" % direction)
            reach_room(direction)
            picked_items = set(get_from_log()["items"])
            print("Items: %s\n" % picked_items)
            if picked_items.intersection(set(item_list)):
                break
        else:
            print("Nope\n")
        number_of_runs += 1
    pyautogui.keyDown('esc')


main()
# time.sleep(delay)
# reach_room("down")
# print(room_direction())
