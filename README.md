# ufo-program
🛸 ASCII UFO simulator for the terminal! Command an animated disc with pulsing lights, upgradable beam/hull/sensors, movable position, speed controls &amp; toggleable energy beam (pygame sound). Scan to collect resources + fetch real UFO sightings from API (with fallback data). Retro-style TUI adventure built with blessed, colorama &amp; more.
# UFO Interactive - Super Advanced Disc with Real-time API

A fun, retro-style terminal-based UFO simulator game with ASCII art animation, upgrades, resource collection, beam effects, and real-time UFO sighting reports (via API + fallback data).

Features include:
- Animated UFO disc with glowing lights & upgradeable components (hull, beam, sensors)
- Tractor beam toggle with sound effect (if WAV file present)
- Move left/right, speed up/down animation
- "Scan" to gain resources and fetch real UFO sightings
- Fetches from a public UFO sightings API (when available) or uses fallback dataset
- BeautifulTable + blessed + colorama for nice terminal UI

<video controls width="100%">
  <source src="demo.gif" type="image/gif"> <!-- replace with actual demo if you record one -->
  Your browser does not support the video tag.
</video>

## Requirements

- **Python** ≥ 3.8 (developed and tested on 3.10–3.12)
- Terminal that supports ANSI colors and cursor control (most modern terminals do)

### Python Dependencies

```bash
pip install pygame requests colorama blessed beautifultable
