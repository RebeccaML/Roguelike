import tcod as libtcod
from entity import Entity
from render_functions import clear_all, render_all
from input_handlers import handle_keys
from map_objects.game_map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150)
    }

    # Create the player and an npc using the Entity class
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", libtcod.purple)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", libtcod.green)
    entities = [npc, player]

    # Telling libtcod which file to use, second argument is file type
    libtcod.console_set_custom_font("arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # This is what creates the screen, sets the game name and specifies fullscreen boolean
    libtcod.console_init_root(screen_width, screen_height, "TBD", False)

    # Creating the console
    con = libtcod.console_new(screen_width, screen_height)

    #Initialize map
    game_map = GameMap(map_width, map_height)

    # Variables for holding keyboard/mouse input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Loops that continues until the game window is closed
    # Checks for key/mouse press
    # Specifies character colour, where to put them, what they'll be represented by
    # and the background. The 0 is the console we're drawing to.
    # console_flush() draws everything
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        libtcod.console_flush()

        clear_all(con, entities)

        # This calls the handle_keys function to determine what should be done
        # depending on which key was pressed.
        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        # takes the x/y move amounts and applies them to player's position
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == "__main__":
    main()