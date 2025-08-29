import pygame
from game.core.settings import ROOM_WIDTH, ROOM_HEIGHT, ROOM_COLORS

class Room:
    def __init__(self, room_x_index, room_y_index, color):
        self.room_x_index = room_x_index # Grid index, not pixel
        self.room_y_index = room_y_index # Grid index, not pixel
        self.color = color
        # Calculate the room's bounds in world coordinates
        self.world_rect = pygame.Rect(
            room_x_index * ROOM_WIDTH,
            room_y_index * ROOM_HEIGHT,
            ROOM_WIDTH,
            ROOM_HEIGHT
        )

    def draw(self, surface, camera_offset_x, camera_offset_y):
        # Adjust draw position based on camera
        # This room's top-left corner in screen coordinates
        screen_x = self.world_rect.x - camera_offset_x
        screen_y = self.world_rect.y - camera_offset_y
        
        # Only draw if the room is visible on the screen
        # This is a basic visibility check; more complex culling could be added
        if screen_x < surface.get_width() and screen_x + ROOM_WIDTH > 0 and \
           screen_y < surface.get_height() and screen_y + ROOM_HEIGHT > 0:
            pygame.draw.rect(surface, self.color, (screen_x, screen_y, ROOM_WIDTH, ROOM_HEIGHT))
            # Optional: Draw a border to distinguish rooms
            pygame.draw.rect(surface, (0,0,0), (screen_x, screen_y, ROOM_WIDTH, ROOM_HEIGHT), 1)
            
            # Draw house walls if this is the first room
            self.draw_house_walls(surface, screen_x, screen_y)

    def draw_house_walls(self, surface, screen_x, screen_y):
        """Draw house-like walls in top-down view for the first room (top left)"""
        if self.room_x_index == 0 and self.room_y_index == 0:
            # House wall colors
            wall_color = (139, 69, 19)  # Brown
            floor_color = (210, 180, 140)  # Tan/beige floor
            door_color = (160, 82, 45)  # Saddle brown
            
            # House dimensions
            house_width = 300
            house_height = 200
            house_x = screen_x + 50  # Move closer to left edge
            house_y = screen_y + 50  # Move closer to top edge
            
            # Draw the four walls of the house
            wall_thickness = 15
            
            # Top wall
            pygame.draw.rect(surface, wall_color, 
                           (house_x, house_y, house_width, wall_thickness))
            
            # Bottom wall (with door opening)
            # Left part of bottom wall
            door_width = 50
            door_x = house_x + (house_width - door_width) // 2
            left_wall_width = door_x - house_x
            pygame.draw.rect(surface, wall_color, 
                           (house_x, house_y + house_height - wall_thickness, left_wall_width, wall_thickness))
            
            # Right part of bottom wall
            right_wall_x = door_x + door_width
            right_wall_width = (house_x + house_width) - right_wall_x
            pygame.draw.rect(surface, wall_color, 
                           (right_wall_x, house_y + house_height - wall_thickness, right_wall_width, wall_thickness))
            
            # Left wall
            pygame.draw.rect(surface, wall_color, 
                           (house_x, house_y, wall_thickness, house_height))
            
            # Right wall
            pygame.draw.rect(surface, wall_color, 
                           (house_x + house_width - wall_thickness, house_y, wall_thickness, house_height))
            
            # Draw the floor inside the house
            floor_x = house_x + wall_thickness
            floor_y = house_y + wall_thickness
            floor_width = house_width - (2 * wall_thickness)
            floor_height = house_height - (2 * wall_thickness)
            pygame.draw.rect(surface, floor_color, 
                           (floor_x, floor_y, floor_width, floor_height))
            
            # Interior room divisions (optional - making it look more like a house)
            # Vertical divider creating two rooms
            divider_x = house_x + house_width // 2
            pygame.draw.rect(surface, wall_color, 
                           (divider_x - wall_thickness // 2, house_y, wall_thickness, house_height))
            
            # Small room on the left
            small_room_width = house_width // 2 - wall_thickness // 2
            small_room_height = house_height // 2 - wall_thickness // 2
            small_room_x = house_x + wall_thickness
            small_room_y = house_y + wall_thickness
            
            # Horizontal divider in the left room
            pygame.draw.rect(surface, wall_color, 
                           (small_room_x, small_room_y + small_room_height - wall_thickness // 2, 
                            small_room_width, wall_thickness // 2))
            
            # Draw door frame/arch to make the opening more visible
            door_frame_thickness = 3
            door_frame_color = (101, 67, 33)  # Darker brown
            
            # Door frame top
            pygame.draw.rect(surface, door_frame_color, 
                           (door_x - door_frame_thickness, house_y + house_height - wall_thickness - door_frame_thickness, 
                            door_width + (2 * door_frame_thickness), door_frame_thickness))
            
            # Door frame left
            pygame.draw.rect(surface, door_frame_color, 
                           (door_x - door_frame_thickness, house_y + house_height - wall_thickness, 
                            door_frame_thickness, wall_thickness))
            
            # Door frame right
            pygame.draw.rect(surface, door_frame_color, 
                           (door_x + door_width, house_y + house_height - wall_thickness, 
                            door_frame_thickness, wall_thickness))

if __name__ == '__main__':
    # Example usage (requires a Pygame screen setup to run)
    pygame.init()
    screen = pygame.display.set_mode((ROOM_WIDTH, ROOM_HEIGHT))
    pygame.display.set_caption("Room Test")
    
    # Create a sample room
    test_room = Room(0, 0, ROOM_COLORS[0])
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255,255,255)) # White background
        test_room.draw(screen, 0, 0) # Draw room with no camera offset
        pygame.display.flip()
        
    pygame.quit()
