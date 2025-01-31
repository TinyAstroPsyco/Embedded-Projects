import pygame
import sys
import MBTA_Fetcher
import threading
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bus Animation")

# Clock to control FPS
clock = pygame.time.Clock()
FPS = 55

class bus:
    def __init__(self):
    # Bus Properties
        self.bus_width = 120
        self.bus_height = 60
        self.bus_x = -self.bus_width  # Start off-screen (left)
        self.bus_y = SCREEN_HEIGHT // 2 - self.bus_height // 2 + 60 # Changing 60 will change the the height of the bus from the ground
        self.bus_speed = 1  # Speed of the bus

bus_1 = bus() # Creating a bus object

# Using a different thread to fetch the data from the api
fetched_timings = None
# Fetching thread function
def fetch_data_thread():
    global fetched_timings
    while True:
        fetched_data = MBTA_Fetcher.fetch()
        print(f'fetched_data :::::: is >> {fetched_data}')
        if fetched_data:
            fetched_timings = fetched_data     
        time.sleep(10)  # Fetch data every 10 seconds

def map_value_to_range(value, from_min, from_max, to_min, to_max):
    """Maps a value from one range to another."""
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled_value = (value - from_min) / from_range
    return to_min + (scaled_value * to_range)


# Start the fetching thread
fetch_thread = threading.Thread(target=fetch_data_thread, daemon=True)
fetch_thread.start()


total_secs = None
time_map = 0

# Main Loop
while True:
    # time_data = MBTA_Fetcher.fetch()
    screen.fill(WHITE)  # Clear the screen

    if fetched_timings is not None:
        for i in range(len(fetched_timings)):
            img = font.render(str(fetched_timings[i]['h']) +"h " + str(fetched_timings[i]['m']) + "m " + str(fetched_timings[i]['s']) + "s", True, BLUE)
            
            screen.blit(img, (700, 20+i*20))
            total_secs = int(fetched_timings[0]['total_seconds'])
            if total_secs < 0:
                total_secs = int(fetched_timings[1]['total_seconds'])
            print(f'Total sSecs >> {total_secs}')

        time_map = map_value_to_range(total_secs, 0,1400,500,0)
    
    else :
        time_map = 0

    
    print(f'tmemap >> {time_map}')
    # Draw the road
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT // 2 + 100, SCREEN_WIDTH, 100))
    
    # pygame.draw.rect(screen, BLACK, (bus_1.bus_x , bus_1.bus_y, bus_1.bus_width, bus_1.bus_height))

    # Draw the bus body
    pygame.draw.rect(screen, BLUE, (bus_1.bus_x +time_map, bus_1.bus_y, bus_1.bus_width, bus_1.bus_height))
    
    # Draw bus windows
    pygame.draw.rect(screen, WHITE, (bus_1.bus_x + 10+time_map, bus_1.bus_y + 10, 30, 30))
    pygame.draw.rect(screen, WHITE, (bus_1.bus_x + 50+time_map, bus_1.bus_y + 10, 30, 30))
    pygame.draw.rect(screen, WHITE, (bus_1.bus_x + 90+time_map, bus_1.bus_y + 10, 20, 30))

    # Draw wheels
    pygame.draw.circle(screen, BLACK, (bus_1.bus_x + 20+time_map, bus_1.bus_y + 60), 10)
    pygame.draw.circle(screen, BLACK, (bus_1.bus_x + 100+time_map, bus_1.bus_y + 60), 10)

    # Update bus position
    bus_1.bus_x = 100
    # bus_1.bus_x += bus_1.bus_speed
    if bus_1.bus_x > SCREEN_WIDTH:
        bus_1.bus_x = -bus_1.bus_width  # Reset position when off-screen

    font = pygame.font.SysFont(None, 24) #Initilizing the font

     
            
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()  # Update the screen
    clock.tick(FPS)  # Maintain the frame rate
