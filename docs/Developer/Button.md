# Send Button Commands (pbf, ssf)

[<img src="https://canary.discordapp.com/api/guilds/695809740428673034/widget.png?style=banner2">](https://discord.gg/cQ4gWxN)

We mostly use a group of functions with prefix `pbf_` to send buttong commands to a micro-controller (like Arduino or Teensy). 
The controller then sends the button commands to a connected Nintendo Switch to control a game.
Those functions are defined in [NintendoSwitch_Commands_PushButtons.h](https://github.com/PokemonAutomation/Arduino-Source/blob/main/SerialPrograms/Source/NintendoSwitch/Commands/NintendoSwitch_Commands_PushButtons.h).
Example button commands are `pbf_press_button()` and `pbf_press_dpad()`.
You can read the comments of those functions to understand how to use them.

Note we use ticks to measure the amount of time a button action is executed. Inside the micro-controller 125 ticks is one second. Access this number via [`TICKS_PER_SECOND`](https://github.com/PokemonAutomation/Arduino-Source/blob/main/SerialPrograms/Source/NintendoSwitch/Controllers/NintendoSwitch_ControllerButtons.h).

An example automation program that uses those functions is [**PokemonLA_BraviaryHeightGlitch**](https://github.com/PokemonAutomation/Arduino-Source/blob/main/SerialPrograms/Source/PokemonLA/Programs/General/PokemonLA_BraviaryHeightGlitch.cpp).

## Button Command Buffer on Micro-Controller

When a `pbf` function is called, the program may not wait for the micro-controller to finish executing the button command.
It may just send the command to the micro-controller and continue executing following lines of code.
Our software that runs on the micro-controller uses a buffer to hold incoming button commands.
The `pbf` function has to wait only when the buffer on the micro-controller is full. It will wait until the micro-controller finishes executing the oldest command in the buffer so that the buffer has space to receive the new command.*

For example, if the micro-controller buffer is empty and a program sends a command of holding button A for 200 ticks and releasing it for 100 ticks,
the program will not wait for 300 ticks during exeuction of `pbf_press_button()`.
The function quickly returns and the program begins executing the next line of code.
At the same time, the micro-controller will start spending 300 ticks to execute the button command.
It will keep pressing button A to the Switch for 200 ticks, then release it and wait for 100 ticks.

This is like the case of asynchronous IO processing in some software systems.

**Important:** You should not *rely* this asynchronous behavior to perform parallelization. The internal buffer sizes are undocumented and may change at any time. And some functions may break into a sequence of instructions that occupy multiple buffer slots. The purpose of the asynchronous buffering is to preserve the exact timing of button sequences across an otherwise high-latency serial bus.

## Wait for Commands to Finish

So in the case like you would want the program to wait for the button commands to finish before doing some other tasks (e.g. reading the video stream),
you need to call `context.wait_for_all_requests()` after the code of button commands.
This function stops the program from doing anything until all the commands sent to the micro-controller have finished.
An example usage is in [**PokemonLA_PokedexTasksReader**](https://github.com/PokemonAutomation/Arduino-Source/blob/main/SerialPrograms/Source/PokemonLA/Programs/General/PokemonLA_PokedexTasksReader.cpp).
The program reads Pokédex tasks. After it sends button commands that tells the game to go to the next Pokédex page,
it calls `context.wait_for_all_requests()` before reading the video stream. In this way, when the program reads the video stream, the game is indeed showing the next page.

## ssf functions
The `ssf` functions are similar to the `pbf` functions, but they allow for button/joystick overlapping. 

However, the `ssf` functions don't always allow for overlapping. As a general rule for ssf overlapping, overlapping only works as long as you are pressing different buttons/components. As soon as an attempted overlap hits a conflict, (e.g. a button overlapping with itself, or mashing a button), the schedule stalls until the previous press finishes and cools down.

For example, the following code allows for pushing the joystick while mashing the A button.

```
// example 1
ssf_press_left_joystick(context, 128, 0, 0ms, 5000ms);
ssf_mash1_button(context, BUTTON_A, 5000ms);
```

But if I reverse the order, they will NOT overlap.

```
// example 2
ssf_mash1_button(context, BUTTON_A, 5000ms);
ssf_press_left_joystick(context, 128, 0, 0ms, 5000ms);
```

In example 1, `ssf_press_left_joystick` immediately returns because it's only one operation that doesn't conflict with anything before or after it, therefore allowing the next command to be run right away.
Example 2 does not overlap because mashing the button results in the button overlapping with itself, which stalls the schedule until it finishes mashing; `ssf_press_left_joystick` only gets run after it finishes mashing.

Consider another example below:

```
// example 3
ssf_press_left_joystick(context, 128, 255, 0ms, 5000ms);
ssf_press_left_joystick(context, 128, 0, 0ms, 5000ms);
ssf_mash1_button(context, BUTTON_A, 5000ms);
```

In example 3, the first two lines moving the joystick conflict. So line 1 goes and finishes, then line 2 and 3 are done simultaneously.

## pbf_controller_state

`pbf_controller_state()` is another function that allows you to hold down multiple buttons at the same time, by exposing the entire controller state.

NOTE: `pbf_controller_state()` will wait until all unfinished `ssf_`commands are finished. `pbf_press_button()` will only wait until the buttons you're trying to use are finished. In other words, `pbf_press_button()` will overlap with `ssf_` while `pbf_controller_state()` will not.
