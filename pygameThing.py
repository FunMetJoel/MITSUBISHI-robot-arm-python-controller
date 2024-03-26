import pygame
import sys
from gerrard import *
import pyautogui
import time


newRobot = Robot("/dev/ttyUSB0")

newRobot.connect()
pos = [0,90,0,0,0,0]

def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode()
    pygame.display.set_caption("Scroll Wheel Demo")

    # Initialize variables
    scroll_amount = 0
    with newRobot:
        newRobot.end()
        print(newRobot.executeCommand("SERVO ON", True))
        time.sleep(2)
        
        pos = [0,90,0,0,0,0]
        newRobot.setAcceleration(10, 10)
        #newRobot.overrideSpeed(10)
        for i in range(1, 7):
            newRobot.torqueLimit(i, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        scroll_amount += 1
                    elif event.button == 5:  # Scroll down
                        scroll_amount -= 1

            # Gets scroll wheel input and moves the robot accordingly
            pos[0] = 0 + ((pyautogui.position()[0] - 800) / -10)
            pos[1] = 90 + ((pyautogui.position()[1] - 540) / 10)
            pos[2] = 0 + (scroll_amount * 5)

            newRobot.setVariable("NEWPOS", JointPos(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]))
            newRobot.moveTo("NEWPOS")
            # Clear the screen
            screen.fill((255, 255, 255))

            # Display scroll amount
            font = pygame.font.Font(None, 36)
            text = font.render(f"Scroll Amount: {scroll_amount}", True, (0, 0, 0))
            screen.blit(text, (50, 50))

            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    main()
