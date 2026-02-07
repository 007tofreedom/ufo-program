import os
import time
import pygame
import random
import requests
from colorama import init, Fore, Style
from blessed import Terminal
from beautifultable import BeautifulTable

# Initialize colorama for cross-platform color support
init()

def clear_screen(term):
    print(term.clear, end='')

class UFO:
    def __init__(self):
        self.hull_level = 1
        self.beam_level = 1
        self.sensors_level = 1
        self.beam_on = False
        self.position = 0  # For left-right movement
        self.max_position = 10
        self.resources = 0
        self.animation_frame = 0  # For animated lights and beam
        self.frame_delay = 0.1  # General animation speed (seconds)
        self.beam_delay = 0.1  # Beam loop speed (seconds)
        self.last_beam_update = time.time()  # Track last beam update time
        self.last_sighting_update = 0  # Track last sighting update time
        self.current_sighting = None  # Store current sighting data
        self.sighting_cache = []  # Cache up to 10 recent sightings
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        try:
            self.beam_sound = pygame.mixer.Sound('laser.wav')  # Placeholder: replace with actual WAV file
        except FileNotFoundError:
            print("Warning: laser.wav not found. Sound disabled.")
            self.beam_sound = None
        # List of US states and UFO shapes for API queries
        self.states = ['NY', 'CA', 'TX', 'FL', 'WA']
        self.shapes = ['Oval', 'Triangle', 'Disk', 'Circle', 'Light']
        # Recent years for prioritizing new sightings
        self.recent_years = ['2024', '2025']
        # Fallback dataset for UFO sightings
        self.fallback_sightings = [
            {
                "city": "Sanborn",
                "state": "NY",
                "date": "2016-09-29",
                "shape": "Oval",
                "summary": "3 orbs dancing/chasing each other in circles in Sanborn, NY."
            },
            {
                "city": "Phoenix",
                "state": "AZ",
                "date": "1997-03-13",
                "shape": "Triangle",
                "summary": "Series of lights in V-shape formation over Phoenix."
            },
            {
                "city": "Roswell",
                "state": "NM",
                "date": "1947-07-02",
                "shape": "Disk",
                "summary": "Unidentified craft crashed near Roswell."
            },
            {
                "city": "Seattle",
                "state": "WA",
                "date": "2024-06-15",
                "shape": "Circle",
                "summary": "Bright circular object hovering over Puget Sound."
            },
            {
                "city": "Miami",
                "state": "FL",
                "date": "2025-01-10",
                "shape": "Light",
                "summary": "Pulsating light moving erratically over Miami Beach."
            }
        ]

    def get_ufo_art(self):
        # Animated lights: alternate between '*' and '+' based on animation_frame
        light_char = '*' if self.animation_frame % 2 == 0 else '+'
        hull = [
            # Level 1: Intricate compact disc with energy core and fins
            ["        .-===-.        ",
             f"      /  {light_char}{light_char}{light_char}  \\      ",
             "     /   *****   \\     ",
             "    /=============\\    ",
             "     \\   *****   /     ",
             f"      \\  {light_char}{light_char}{light_char}  /      ",
             "        '-===-'        "],
            # Level 2: Enhanced disc with glowing panels and thrusters
            ["        .-=====-.        ",
             f"      /  {light_char}{light_char}++{light_char}{light_char}  \\      ",
             "     /==| **** |==\\     ",
             "    /===|******|===\\    ",
             "     \\==| **** |==/     ",
             f"      \\  {light_char}{light_char}++{light_char}{light_char}  /      ",
             "        '-=====-'        "],
            # Level 3: Large high-tech disc with detailed core, armor, and energy fields
            ["       .-=======-.       ",
             f"     /  {light_char}{light_char}{light_char}++{light_char}{light_char}{light_char}  \\     ",
             "    /==|  ****  |==\\    ",
             "   /===|********|===\\   ",
             "   \\===|********|===/   ",
             "    \\==|  ****  |==/    ",
             f"     \\  {light_char}{light_char}{light_char}++{light_char}{light_char}{light_char}  /     ",
             "       '-=======-'       "]
        ]
        # Beam patterns with color, cycling every 2 frames to match lights
        beam_colors = [Fore.BLUE, Fore.CYAN]  # Cycle through colors
        beam_patterns = [
            [f"{beam_colors[self.animation_frame % 2]}        |~~|         {Style.RESET_ALL}",  # Full top segment
             "        |  |         ",
             "        |  |         "],
            ["        |~ |         ",  # Partial top fading
             f"{beam_colors[self.animation_frame % 2]}        |~~|         {Style.RESET_ALL}",
             "        |  |         "]
        ]
        beam = [
            "",  # No beam
            beam_patterns[self.animation_frame % 2],  # Level 1: Single line cycling
            [f"{beam_colors[self.animation_frame % 2]}        |~~|         {Style.RESET_ALL}\n{beam_patterns[self.animation_frame % 2][0]}",
             f"{beam_colors[(self.animation_frame + 1) % 2]}        |~~|         {Style.RESET_ALL}\n{beam_patterns[(self.animation_frame + 1) % 2][0]}"],
            [f"{beam_colors[self.animation_frame % 2]}        |~~|         {Style.RESET_ALL}\n{beam_patterns[self.animation_frame % 2][0]}\n{beam_patterns[(self.animation_frame + 1) % 2][0]}",
             f"{beam_colors[(self.animation_frame + 1) % 2]}        |~~|         {Style.RESET_ALL}\n{beam_patterns[(self.animation_frame + 1) % 2][0]}\n{beam_patterns[self.animation_frame % 2][0]}",
             f"{beam_colors[self.animation_frame % 2]}        |~~|         {Style.RESET_ALL}\n{beam_patterns[(self.animation_frame + 1) % 2][0]}\n{beam_patterns[self.animation_frame % 2][0]}"]
        ]
        sensors = [
            "",
            "      [=o  o=]      ",
            "     [=oo  oo=]     "
        ]
        base_art = hull[min(self.hull_level - 1, 2)]
        # Apply sensors
        sensor_line = sensors[min(self.sensors_level - 1, 2)]
        if sensor_line:
            base_art[1] = sensor_line
        # Apply beam
        if self.beam_on:
            # Update beam animation based on beam_delay
            current_time = time.time()
            if current_time - self.last_beam_update >= self.beam_delay:
                self.animation_frame = (self.animation_frame + 1) % 2
                self.last_beam_update = current_time
                # Play sound effect only on full segment
                if self.beam_sound and self.animation_frame % 2 == 0:
                    self.beam_sound.play()
            beam_lines = beam[min(self.beam_level, 3)]
            if isinstance(beam_lines, list):
                beam_lines = "\n".join(beam_lines)
            base_art = base_art + [beam_lines]
        else:
            # Update animation frame for lights when beam is off
            self.animation_frame = (self.animation_frame + 1) % 2
        # Apply position shift with animation
        max_width = max(len(line) for line in base_art)
        shifted_art = []
        shift = self.position % 4  # Cycle through 0, 1, 2, 1 for smooth oscillation
        if shift > 1:
            shift = 2 - (shift - 2)  # Reverse for 2, 1
        for line in base_art:
            padded = line.center(max_width + self.max_position * 2)
            if self.position > 0:
                shifted = ' ' * shift + padded[:-shift]
            elif self.position < 0:
                shifted = padded[-shift:] + ' ' * (-shift)
            else:
                shifted = padded
            shifted_art.append(shifted)
        return shifted_art

    def upgrade(self, component):
        if self.resources < 10:
            return "Need 10 resources to upgrade! Current: " + str(self.resources)
        if component == 'hull' and self.hull_level < 3:
            self.hull_level += 1
            self.resources -= 10
            return "Hull upgraded to level " + str(self.hull_level)
        elif component == 'beam' and self.beam_level < 3:
            self.beam_level += 1
            self.resources -= 10
            return "Beam upgraded to level " + str(self.beam_level)
        elif component == 'sensors' and self.sensors_level < 3:
            self.sensors_level += 1
            self.resources -= 10
            return "Sensors upgraded to level " + str(self.sensors_level)
        else:
            return "Component maxed out or invalid!"

    def toggle_beam(self):
        self.beam_on = not self.beam_on
        self.last_beam_update = time.time()  # Reset beam update timer
        return "Beam " + ("ON" if self.beam_on else "OFF")

    def speed_up(self):
        if self.beam_on:
            if self.beam_delay > 0.05:  # Minimum beam delay
                self.beam_delay = max(0.05, self.beam_delay - 0.05)
            return f"Beam speed increased! Beam delay: {self.beam_delay:.2f}s"
        else:
            if self.frame_delay > 0.05:  # Minimum frame delay
                self.frame_delay = max(0.05, self.frame_delay - 0.05)
            return f"Animation speed increased! Frame delay: {self.frame_delay:.2f}s"

    def speed_down(self):
        if self.beam_on:
            if self.beam_delay < 0.3:  # Maximum beam delay
                self.beam_delay = min(0.3, self.beam_delay + 0.05)
            return f"Beam speed decreased! Beam delay: {self.beam_delay:.2f}s"
        else:
            if self.frame_delay < 0.3:  # Maximum frame delay
                self.frame_delay = min(0.3, self.frame_delay + 0.05)
            return f"Animation speed decreased! Frame delay: {self.frame_delay:.2f}s"

    def move_left(self):
        if self.position > -self.max_position:
            self.position -= 1
        return "Moved left!"

    def move_right(self):
        if self.position < self.max_position:
            self.position += 1
        return "Moved right!"

    def fetch_sighting(self):
        # Try cached sighting first
        if self.sighting_cache:
            return random.choice(self.sighting_cache)
        # Try API call with recent year
        try:
            state = "NY"  # Known valid state
            shape = "Oval"  # Known valid shape
            year = random.choice(self.recent_years)  # Prioritize recent years
            url = f"https://ufo-api.herokuapp.com/api/sightings/search?state={state}&shape={shape}&year={year}&limit=1"
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx
            data = response.json()
            if data.get("status") == "OK" and data.get("sightings"):
                sighting = data["sightings"][0]
                sighting_data = {
                    "city": sighting.get("city", "Unknown"),
                    "state": state,
                    "date": sighting.get("date", "Unknown").split("T")[0],
                    "shape": sighting.get("shape", "Unknown"),
                    "summary": sighting.get("summary", "No details available"),
                    "source": "API"
                }
                # Cache the sighting
                if len(self.sighting_cache) < 10:
                    self.sighting_cache.append(sighting_data)
                return sighting_data
            else:
                # Fallback to random state/shape without year
                state = random.choice(self.states)
                shape = random.choice(self.shapes)
                url = f"https://ufo-api.herokuapp.com/api/sightings/search?state={state}&shape={shape}&limit=1"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                if data.get("status") == "OK" and data.get("sightings"):
                    sighting = data["sightings"][0]
                    sighting_data = {
                        "city": sighting.get("city", "Unknown"),
                        "state": state,
                        "date": sighting.get("date", "Unknown").split("T")[0],
                        "shape": sighting.get("shape", "Unknown"),
                        "summary": sighting.get("summary", "No details available"),
                        "source": "API"
                    }
                    # Cache the sighting
                    if len(self.sighting_cache) < 10:
                        self.sighting_cache.append(sighting_data)
                    return sighting_data
                else:
                    # Fallback to static dataset
                    sighting = random.choice(self.fallback_sightings)
                    return {**sighting, "source": "Local"}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Fallback to static dataset for 404 error
                sighting = random.choice(self.fallback_sightings)
                return {
                    **sighting,
                    "source": f"Local (404: {url})"
                }
            else:
                # Fallback to static dataset for other HTTP errors
                sighting = random.choice(self.fallback_sightings)
                return {
                    **sighting,
                    "source": f"Local (HTTP Error: {str(e)})"
                }
        except (requests.exceptions.RequestException, ValueError) as e:
            # Fallback to static dataset for network or JSON errors
            sighting = random.choice(self.fallback_sightings)
            return {
                **sighting,
                "source": f"Local (Error: {str(e)})"
            }

    def scan(self):
        resources_found = self.sensors_level * 2
        self.resources += resources_found
        sighting = self.fetch_sighting()
        return (
            f"Scanned! Gained {resources_found} resources. Total: {self.resources}\n"
            f"Detected UFO sighting in {sighting['city']}, {sighting['state']} on {sighting['date']}: "
            f"{sighting['shape']} shape - {sighting['summary']} ({sighting['source']})"
        )

def main():
    term = Terminal()
    ufo = UFO()
    message = "Controls: A (left), D (right), L (speed up), R (speed down), B (beam), S (scan), U (upgrade), Q (quit)"
    sighting_update_interval = 5  # Update sighting every 5 seconds
    with term.cbreak(), term.hidden_cursor():
        while True:
            clear_screen(term)
            # Update sighting periodically
            current_time = time.time()
            if current_time - ufo.last_sighting_update >= sighting_update_interval or ufo.current_sighting is None:
                ufo.current_sighting = ufo.fetch_sighting()
                ufo.last_sighting_update = current_time
            # Create table for structured display
            table = BeautifulTable(maxwidth=80)
            table.set_style(BeautifulTable.STYLE_NONE)
            # Add UFO and beam
            ufo_art = ufo.get_ufo_art()
            table.rows.append(["\n".join(ufo_art)])
            # Add status
            table.rows.append([f"Resources: {ufo.resources} | Hull: {ufo.hull_level} | Beam: {ufo.beam_level} | Sensors: {ufo.sensors_level} | Frame: {ufo.frame_delay:.2f}s | Beam: {ufo.beam_delay:.2f}s"])
            # Add sighting info
            if ufo.current_sighting:
                sighting = ufo.current_sighting
                table.rows.append([
                    f"Sighting: {sighting['city']}, {sighting['state']} on {sighting['date']}: "
                    f"{sighting['shape']} shape - {sighting['summary']} ({sighting['source']})"
                ])
            else:
                table.rows.append(["Sighting: No data available"])
            # Add controls and message
            table.rows.append([message])
            print(table)
            print("Action (A/D/L/R/B/S/U/Q): ", end="", flush=True)
            action = term.inkey(timeout=ufo.frame_delay).lower()
            message = "Controls: A (left), D (right), L (speed up), R (speed down), B (beam), S (scan), U (upgrade), Q (quit)"
            if action == 'a':
                message = ufo.move_left()
            elif action == 'd':
                message = ufo.move_right()
            elif action == 'l':
                message = ufo.speed_up()
            elif action == 'r':
                message = ufo.speed_down()
            elif action == 'b':
                message = ufo.toggle_beam()
            elif action == 's':
                message = ufo.scan()
            elif action == 'u':
                print("Upgrade (1=Hull, 2=Beam, 3=Sensors): ", end="", flush=True)
                choice = term.inkey(timeout=None)
                if choice == '1':
                    message = ufo.upgrade('hull')
                elif choice == '2':
                    message = ufo.upgrade('beam')
                elif choice == '3':
                    message = ufo.upgrade('sensors')
                else:
                    message = "Invalid upgrade choice!"
            elif action == 'q':
                print(f"\n{term.normal}UFO has returned to the mothership!")
                break
            if not ufo.beam_on:
                # Update animation frame for lights when beam is off
                ufo.animation_frame = (ufo.animation_frame + 1) % 2
            time.sleep(ufo.frame_delay)  # General animation speed

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUFO has returned to the mothership!")