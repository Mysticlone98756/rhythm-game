import pygame
import json
import math

# Pygame Initialization
pygame.init()
pygame.mixer.init()

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chart Editor")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
LANES = 4
LANE_WIDTH = SCREEN_WIDTH // LANES
NOTES = []
UNDO_STACK = []
REDO_STACK = []
TIMELINE_POSITION = 0
SCROLL_SPEED = 2  # Decrease the value to make notes appear faster

# Chart Data
chart = {
    "song": {
        "title": "Custom Song",
        "artist": "Unknown",
        "bpm": 300,  # Increased BPM for faster charting
        "offset": 0  # In milliseconds
    },
    "notes": []
}

# BPM Synchronization
BPM = chart["song"]["bpm"]
MS_PER_BEAT = 60000 / BPM  # Milliseconds per beat

# Audio Playback
pygame.mixer.music.load("song.mp3")  # Replace with your song file
pygame.mixer.music.play(-1)  # Loop indefinitely
SONG_START_TIME = pygame.time.get_ticks() + chart["song"]["offset"]

# Helper Functions
def get_song_time():
    """Get current playback time in milliseconds."""
    return pygame.time.get_ticks() - SONG_START_TIME

def align_to_beat(ms):
    """Align a time value (ms) to the nearest beat."""
    return round(ms / MS_PER_BEAT) * MS_PER_BEAT

def undo():
    """Undo the last note action."""
    if NOTES:
        last_note = NOTES.pop()
        REDO_STACK.append(last_note)
        chart["notes"].remove(last_note)

def redo():
    """Redo the last undone note action."""
    if REDO_STACK:
        note = REDO_STACK.pop()
        NOTES.append(note)
        chart["notes"].append(note)

# Draw Grid and Notes
def draw_grid():
    screen.fill(BLACK)
    for i in range(LANES):
        pygame.draw.rect(screen, GRAY, (i * LANE_WIDTH, 0, LANE_WIDTH - 5, SCREEN_HEIGHT), 0)
    
    # Draw red line for the timeline (current song position)
    pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT - TIMELINE_POSITION), (SCREEN_WIDTH, SCREEN_HEIGHT - TIMELINE_POSITION), 2)

    # Draw notes
    for note in NOTES:
        x = (note["lane"] - 1) * LANE_WIDTH
        y = SCREEN_HEIGHT - note["time"] + TIMELINE_POSITION
        if 0 < y < SCREEN_HEIGHT:  # Draw only visible notes
            if note["type"] == "hold":
                end_y = SCREEN_HEIGHT - note["end_time"] + TIMELINE_POSITION
                pygame.draw.rect(screen, BLUE, (x + 10, end_y, LANE_WIDTH - 20, y - end_y))
            else:
                pygame.draw.rect(screen, WHITE, (x + 10, y - 20, LANE_WIDTH - 20, 20))

# Add Note
def add_note(lane, start_time, hold_time=None):
    if hold_time:
        note = {"time": start_time, "lane": lane + 1, "type": "hold", "end_time": start_time + hold_time}
    else:
        note = {"time": start_time, "lane": lane + 1, "type": "regular"}
    NOTES.append(note)
    chart["notes"].append(note)
    UNDO_STACK.append(note)  # Add to undo stack

# Save Chart
def save_chart():
    with open("chart.json", "w") as f:
        json.dump(chart, f, indent=2)
    print("Chart saved as chart.json!")

# Update Metadata UI
def update_metadata_ui():
    font = pygame.font.Font(None, 30)
    title_text = font.render(f"Song Title: {chart['song']['title']}", True, WHITE)
    artist_text = font.render(f"Artist: {chart['song']['artist']}", True, WHITE)
    bpm_text = font.render(f"BPM: {chart['song']['bpm']}", True, WHITE)
    offset_text = font.render(f"Offset: {chart['song']['offset']} ms", True, WHITE)
    
    screen.blit(title_text, (20, SCREEN_HEIGHT - 150))
    screen.blit(artist_text, (20, SCREEN_HEIGHT - 120))
    screen.blit(bpm_text, (20, SCREEN_HEIGHT - 90))
    screen.blit(offset_text, (20, SCREEN_HEIGHT - 60))

# Handle Metadata Editing
def handle_metadata_edit(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_t:
            chart["song"]["title"] = input("Enter Song Title: ")
        elif event.key == pygame.K_a:
            chart["song"]["artist"] = input("Enter Artist Name: ")
        elif event.key == pygame.K_b:
            new_bpm = input("Enter BPM: ")
            chart["song"]["bpm"] = int(new_bpm)
            global MS_PER_BEAT
            MS_PER_BEAT = 60000 / chart["song"]["bpm"]
        elif event.key == pygame.K_o:
            new_offset = input("Enter Offset (in ms): ")
            chart["song"]["offset"] = int(new_offset)
            global SONG_START_TIME
            SONG_START_TIME = pygame.time.get_ticks() + chart["song"]["offset"]

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keybindings for Adding Notes (D, F, J, K for different lanes)
        if event.type == pygame.KEYDOWN:
            current_time = align_to_beat(get_song_time())
            if event.key == pygame.K_d:
                add_note(0, current_time)
            elif event.key == pygame.K_f:
                add_note(1, current_time)
            elif event.key == pygame.K_j:
                add_note(2, current_time)
            elif event.key == pygame.K_k:
                add_note(3, current_time)

            # Undo/Redo Keys
            elif event.key == pygame.K_u:  # Undo
                undo()
            elif event.key == pygame.K_r:  # Redo
                redo()

            # Save Chart with "S" Key
            elif event.key == pygame.K_s:
                save_chart()

            handle_metadata_edit(event)

    # Update Timeline
    TIMELINE_POSITION = get_song_time() // SCROLL_SPEED

    draw_grid()
    update_metadata_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
