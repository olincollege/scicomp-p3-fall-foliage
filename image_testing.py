import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Load the image using Pygame
image_path = "olin_image.png"  # Replace with the path to your image
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (WIDTH, HEIGHT))  # Resize the image to fit the screen

# Convert the image to a NumPy array
image_array = pygame.surfarray.array3d(image)

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Display Image as Surface")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Update the Pygame surface with the image array
    pygame.surfarray.blit_array(screen, image_array)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
