import pygame
import numpy as np
import random

FPS = 60

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,200,100)
BLUE = (0,0,255)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0],
                   [0,  0, 1] ])
    return R

def Tmat(tx, ty):
    Translation = np.array([ [1, 0, tx],
                             [0, 1, ty],
                             [0, 0,  1] ])
    return Translation


def draw(screen, P, H, color=(100, 200, 200)) :
    R = H[:2, :2]
    T = H[:2,  2]
    Ptransformed = P @ R.T + T
    pygame.draw.polygon(screen, color=color, points=Ptransformed, width=3)
    return


def main():
    pygame.init()
    pygame.display.set_caption("천사은 20221123")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    tick = 0

    w = 150
    h = 40
    REC = np.array([ [0,0], [w,0], [w,h], [0,h] ])

    w2 = 40
    h2 = 5
    GRIP = np.array([ [0,0], [w2,0], [w2,h2], [0,h2] ])
    
    position = [WINDOW_WIDTH/2.4, WINDOW_HEIGHT-100]

    angle1 = 0
    angle2 = 0
    angle3 = 0

    angle_grip = 0
    grip_closed = False
    grip_toggle = False

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        screen.fill((200, 254, 219))

        # Handle keyboard input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            angle1 += 3
            angle2 += 2
            angle3 += 1

        if keys[pygame.K_LEFT]:
            angle1 -= 3
            angle2 -= 2
            angle3 -= 1

        if keys[pygame.K_SPACE]:
            if not grip_toggle:
                grip_closed = not grip_closed
                grip_toggle = True
                if grip_closed:
                    angle_grip = 30
                else:
                    angle_grip = 0
        else:
            grip_toggle = False

        angle1 = max(min(angle1, 90), -90)
        angle2 = max(min(angle2, 90), -90)
        angle3 = max(min(angle2, 90), -90)


        # Base
        pygame.draw.circle(screen, RED, position, radius=3)
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(screen, REC, H0, BLACK)

        # Arm 1
        H1 = H0 @ Tmat(w/2, 0)
        x, y = H1[0,2], H1[1,2] # joint
        pygame.draw.circle(screen, RED, (x,y), radius=3)
        H11 = H1 @ Rmat(-90) @ Tmat(0, -h/2) @ Tmat(0, h/2) @ Rmat(angle1) @ Tmat(0, -h/2)
        draw(screen, REC, H11, BLUE)

        # Arm 2
        H2 = H11 @ Tmat(w, 0) @ Tmat(0, h/2)
        x, y = H2[0,2], H2[1,2] # joint 2
        pygame.draw.circle(screen, RED, (x,y), radius=3)
        H21 = H2 @ Rmat(angle2) @ Tmat (0, -h/2)
        draw(screen, REC, H21, GREEN)

        # Arm 3
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2)
        x, y = H3[0,2], H3[1,2] # joint 3
        pygame.draw.circle(screen, RED, (x,y), radius=3)
        H31 = H3 @ Rmat(angle3) @ Tmat (0, -h/2)
        draw(screen, REC, H31, BLUE)


        # Gripper
        H4 = H31 @ Tmat(w, h/2)
        H41 = H4 @ Tmat (0, -h2/2)
        draw(screen, GRIP, H41, GREEN)

        H5 = H41 @ Tmat(w2, h2/2)
        H51 = H5 @ Rmat(-90) @ Tmat(-w2/2, h2/2)
        draw(screen, GRIP, H51, GREEN)

        H6 = H51 @ Tmat(w2, 0) @ Tmat(0, h2/2)
        x, y = H6[0,2], H6[1,2]
        pygame.draw.circle(screen, RED, (x,y), radius=3)
        H61 = H6 @ Rmat(-90 + angle_grip) @ Tmat (-w2, 0)
        draw(screen, GRIP, H61, GREEN)

        H7 = H6 @ Tmat(-(w2+h2/2), 0)
        x, y = H7[0,2], H7[1,2]
        pygame.draw.circle(screen, RED, (x,y), radius=3)
        H71 = H7 @ Tmat(h2/2, 0) @ Rmat(90 - angle_grip)
        draw(screen, GRIP, H71, GREEN)

    
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()