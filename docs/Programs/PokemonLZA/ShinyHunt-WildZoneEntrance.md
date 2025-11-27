# Shiny Hunt - Wild Zone Entrance 

See also: [Shiny Hunting Recommendations](ShinyHuntRecommendations.md)

Note: If you have access to the newest beta version of the program, the beta will handle being chased by wild Pokémon reliably. You can ignore the warning of avoiding wild Pokémon below.

## Program Description

Shiny hunt by repeatedly fast traveling to a wild zone entrance. This will shiny hunt all spawns within 50m of the entrance and further if you also set to walk into the zone for a short period of time. Unlike blind macros, this program will tolerate the day/night cycle and will detect audible shinies that are nearby.

Currently the program cannot reliably resolve being chased by wild Pokémon. Therefore it is not appropriate to take a long walk in a zone or even enter at all for some zones (e.g. *Zone 19*).

With the Shiny Charm you will get a shiny Pokémon quite fast if there are many Pokémon spawned around the entrance. Don't let the program run for too long or have old shinies overwritten by new ones.

This program would detect the day/night change. When such change occurs, the program would try to recover after the cutscene.

Shiny sound detection will happen at most once to avoid detecting the same shiny Pokémon over and over.

<img src="images/ShinyHunt-WildZoneEntrance.png">

### Instructions

1. Fast travel to the entrance of a wild zone.
2. Start the program in the game.

### Hunt Guide

Avoid being spotted by wild Pokémon if entering a zone. Even if regular spawns close to the entrance are as peaceful as Slowpoke, they all have a chance to be an aggressive Alpha and cause the program to fail to recover.

Some available Pokémon to hunt:

- Zone 1
    - Fletchling and Bunnelby
- Zone 2
    - Budew, Binacle, Margikarp and Staryu
    - Alpha Magikarp (day) and Alpha Staryu (night)
- Zone 3
    - Pikachu, Flabébé, Skiddo, Espurr
    - Alpha Litleo
- Zone 4
    - Gastly and Honedge
- Zone 5
    - You can hunt both Zone 5 and northeast part of Zone 16 (Alpha Ampharos and Froakie)
- Zone 9
    - Sableye
- Zone 10
    - Slowpoke
- Zone 13
    - Vivillon (day)
    - Alpha Trevenant (night)
- Zone 14
    - Aron
- Zone 16
    - Froakie
- Zone 17
    - Chespin
- Zone 18
    - Alpha Salamence
- Zone 19
    - Kangaskhan
- Zone 20
    - Totodile and Squirtle

For more info regarding Pokémon spawners, check the maps from [Serebii](https://www.serebii.net/pokearth/lumiosecity/) and [game8](https://game8.co/games/Pokemon-Legends-Z-A/archives/557774).

<img src="images/ShinyHunt-WildZoneEntrance-Zone5.png">
<img src="images/ShinyHunt-WildZoneEntrance-ShalphaMagikarp.png">
<img src="images/ShinyHunt-WildZoneEntrance-Salamence.png">

Potentially usefull tip: if a Pokémon that should be spawned within 50m does not spawn when running the program, try first moving closer to this spawner to spawn the Pokémon manually without being chased by wild Pokémon, then fast travel back to the entrance and start the program. This is the trick to enable Beldum teleporter hunting in Lysandre Lab. It could help in wild zones as well.

## Options

### Wild Zone

Pick which Wild Zone you are hunting. This option is important for the program to know how to fast travel to the zone entrance.

### Movement

- **No movement**. Fast travel repeatedly in front of the wild zone entrance. Safe from wild Pokémon.
- **Approach Gate But Don't Enter**. Safe from wild Pokémon.
- **Enter Zone**. Potential danger from wild Pokémon. Pick a safe walk-in distance. Don't choose this on a zone where wild Pokémon notices you when entering.

### Walk Time in Zone

Walk this long in the zone after passing through the gate.

### Running

Running instead of walking while in the zone.

### Shiny Sound Detected Action

When a shiny sound is heard, perform one of the following actions:

- Stop program and go Home. Send notification.
- Keep running. Notify on first shiny sound only. (default)


## Credits

- **Author:** Saͥbͣeͫr👑Ⰰ/naussika, Kuroneko/Mysticial, Gin


<hr>

**Discord Server:** 

[<img src="https://canary.discordapp.com/api/guilds/695809740428673034/widget.png?style=banner2">](https://discord.gg/cQ4gWxN)









