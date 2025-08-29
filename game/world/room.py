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
        # Store wall rectangles for collision detection
        self.wall_rects = []
        self._create_wall_rects()

    def _create_wall_rects(self):
        """Create wall rectangles for collision detection"""
        if self.room_x_index == 0 and self.room_y_index == 0:
            # House dimensions
            house_width = 300
            house_height = 200
            house_x = 50  # Relative to room
            house_y = 50  # Relative to room
            
            # Wall thickness
            wall_thickness = 15
            
            # Convert to world coordinates
            world_house_x = self.world_rect.x + house_x
            world_house_y = self.world_rect.y + house_y
            
            # Top wall
            top_wall = pygame.Rect(world_house_x, world_house_y, house_width, wall_thickness)
            self.wall_rects.append(top_wall)
            
            # Bottom wall (split into two parts due to door)
            door_width = 50
            door_x = world_house_x + (house_width - door_width) // 2
            
            # Left part of bottom wall
            left_wall_width = door_x - world_house_x
            left_bottom_wall = pygame.Rect(world_house_x, world_house_y + house_height - wall_thickness, 
                                         left_wall_width, wall_thickness)
            self.wall_rects.append(left_bottom_wall)
            
            # Right part of bottom wall
            right_wall_x = door_x + door_width
            right_wall_width = (world_house_x + house_width) - right_wall_x
            right_bottom_wall = pygame.Rect(right_wall_x, world_house_y + house_height - wall_thickness, 
                                          right_wall_width, wall_thickness)
            self.wall_rects.append(right_bottom_wall)
            
            # Left wall
            left_wall = pygame.Rect(world_house_x, world_house_y, wall_thickness, house_height)
            self.wall_rects.append(left_wall)
            
            # Right wall
            right_wall = pygame.Rect(world_house_x + house_width - wall_thickness, world_house_y, 
                                   wall_thickness, house_height)
            self.wall_rects.append(right_wall)

    def check_wall_collision(self, player_rect):
        """Check if player collides with any walls in this room"""
        for wall_rect in self.wall_rects:
            if player_rect.colliderect(wall_rect):
                return True
        return False

    def get_collision_response(self, player_rect, old_rect):
        """Get the corrected position when player collides with walls"""
        # Try to resolve collision by moving player back
        corrected_rect = player_rect.copy()
        
        for wall_rect in self.wall_rects:
            if corrected_rect.colliderect(wall_rect):
                # Calculate overlap
                overlap_x = min(corrected_rect.right - wall_rect.left, 
                              wall_rect.right - corrected_rect.left)
                overlap_y = min(corrected_rect.bottom - wall_rect.top, 
                              wall_rect.bottom - corrected_rect.top)
                
                # Resolve collision by moving player in the direction of least overlap
                if overlap_x < overlap_y:
                    if corrected_rect.centerx < wall_rect.centerx:
                        corrected_rect.right = wall_rect.left
                    else:
                        corrected_rect.left = wall_rect.right
                else:
                    if corrected_rect.centery < wall_rect.centery:
                        corrected_rect.bottom = wall_rect.top
                    else:
                        corrected_rect.top = wall_rect.bottom
        
        return corrected_rect

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
            
            # Draw checkered floor inside the house
            self.draw_checkered_floor(surface, house_x, house_y, house_width, house_height, wall_thickness)
            
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

    def draw_checkered_floor(self, surface, house_x, house_y, house_width, house_height, wall_thickness):
        """Draw a checkered black and white floor pattern"""
        # Floor area (inside walls)
        floor_x = house_x + wall_thickness
        floor_y = house_y + wall_thickness
        floor_width = house_width - (2 * wall_thickness)
        floor_height = house_height - (2 * wall_thickness)
        
        # Checker size
        checker_size = 20
        
        # Colors
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)
        
        # Draw checkered pattern
        for y in range(0, int(floor_height), checker_size):
            for x in range(0, int(floor_width), checker_size):
                # Determine color based on position
                if (x // checker_size + y // checker_size) % 2 == 0:
                    color = white_color
                else:
                    color = black_color
                
                # Calculate actual checker position
                checker_x = floor_x + x
                checker_y = floor_y + y
                
                # Draw the checker square
                pygame.draw.rect(surface, color, 
                               (checker_x, checker_y, checker_size, checker_size))

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
