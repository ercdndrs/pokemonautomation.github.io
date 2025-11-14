# Shiny Hunt - Bench Sit

See also: [Shiny Hunting Recommendations](ShinyHuntRecommendations.md)

## Program Description

Shiny hunt by repeatedly sitting on a bench. This will shiny hunt all spawns within 50m of the bench.

While the primary mechanic of this method relies on the fact the game will save the last 10 shinies, this program will be also be able detect nearby shinies that play the shiny sound. Thus this program will be able to notify on a shiny and alternatively either stop the program or keep running in an attempt to spawn more shinies.

Because the shiny sound has a much smaller audible radius than the spawn radius, the vast majority of shinies will not be detected by the program. Likewise, shinies that spawn next to you will repeatedly play their shiny sound each time they respawn after a day reset. Therefore, this program will (by default) only notify and record a video on the first shiny that it hears to avoid spamming.

<img src="images/ShinyHunt-BenchSit.jpg">


### Setup of Settings

**Switch Settings:**

1. Screen size: Must be 100% within the Switch settings
2. [Switch 2: All HDR options must be disabled.](../NintendoSwitch/Switch2Notes.md#switch-2-hdr-may-be-problematic)

**Program Settings:**

1. Video Resolution: 1080p or higher

**Game Settings:**

1. Text Speed: Fast


### Instructions

1. Face a bench such that the A button is visible.
2. Start the program in the game.

## Options

### Shiny Sound Detected Action

When a shiny sound is heard, perform one of the following actions:

- Stop program and go Home. Send notification.
- Keep running. Notify on first shiny sound only. (default)
- Keep running. Notify on all shiny sounds.

The 3rd option is not advised as a shiny spawning next to you will lead to notification spam.

### Take a Video

Record a video of the encounter. This will happen each time a notification is sent. So be careful if you are notifying on all shiny sounds as this may lead a lot of recorded videos of the same shiny.

### Screenshot Delay

When a shiny is detected, wait this long before you take a screenshot and record a video. This will allow the screen to completely load before taking the screenshot.


## Credits

- **Author:** Kuroneko/Mysticial


<hr>

**Discord Server:** 

[<img src="https://canary.discordapp.com/api/guilds/695809740428673034/widget.png?style=banner2">](https://discord.gg/cQ4gWxN)






