from maschinenschreiben.ui import UserInterface


if __name__ == '__main__':
    # Set up the UI:
    ui = UserInterface()

    # Display a menu:
    ui.welcome_message()
    ui.choose_level()

    # Start the lecture-loop:
    ui.lecture_loop()
