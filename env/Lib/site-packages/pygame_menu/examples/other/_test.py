"""
General tests.
"""

import pygame_menu
import pygame
import pdb


def show():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    pygame_menu.controls.KEY_BACK = pygame.K_F1

    menu = pygame_menu.Menu("test", 400, 400)  # the main menu
    sub = pygame_menu.Menu("sub", 400, 400)  # sub is nested under menu
    sub2 = pygame_menu.Menu("sub2", 400, 400)  # sub2 is nested under sub

    # Add "sub" as a link within "menu"
    sub_link = menu.add.menu_link(sub)
    sub.add.button("Back", pygame_menu.events.BACK)

    # Add "sub2" as a link within "sub"
    sub2_link = sub.add.menu_link(sub2)
    sub2.add.button("Back", pygame_menu.events.BACK)

    def opensub(menu=menu, sub=sub, sub2=sub2, sub_link=sub_link):
        print(
            f"BEFORE: current={menu.get_current().get_title()} link_menu={sub_link._menu.get_title()} menu: {menu._index}/{len(menu._widgets)}, sub={sub._index}/{len(sub._widgets)}, sub2={sub2._index}/{len(sub2._widgets)})"
        )

        # pdb.set_trace()
        sub_link.open()
        print(
            f"AFTER: current={menu.get_current().get_title()} link_menu={sub_link._menu.get_title()} menu: {menu._index}/{len(menu._widgets)}, sub={sub._index}/{len(sub._widgets)}, sub2={sub2._index}/{len(sub2._widgets)})"
        )

    def opensub2(menu=menu, sub=sub, sub2=sub2, sub2_link=sub2_link):
        print(
            f"BEFORE: current={menu.get_current().get_title()} link_menu={sub2_link._menu.get_title()} menu: {menu._index}/{len(menu._widgets)}, sub={sub._index}/{len(sub._widgets)}, sub2={sub2._index}/{len(sub2._widgets)})"
        )

        # pdb.set_trace()
        sub2_link.open()
        print(
            f"AFTER: current={menu.get_current().get_title()} link_menu={sub2_link._menu.get_title()} menu: {menu._index}/{len(menu._widgets)}, sub={sub._index}/{len(sub._widgets)}, sub2={sub2._index}/{len(sub2._widgets)})"
        )

    menu.add.button("No-op Button")

    # To see logging/breakpoints replace with:
    # menu.add.button("Sub", opensub)
    menu.add.button("Sub", sub_link.open)

    # To see logging/breakpoints replace with:
    # sub.add.button("Sub2", opensub2)
    sub.add.button("Sub2", sub2_link.open)

    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        screen.fill("black")
        menu.update(events)
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    show()
