# Frequently Asked Questions


## General Questions


### Do I need a hacked or modified Switch?

No! This project is intended for retail (unmodified) Switches. You do not need a hacked Switch.

However, if you do have a hacked Switch, you do not need a microcontroller since we support using sys-botbase as the game controller.

Otherwise, having a hacked Switch will not provide any additional functionality. We do not support accessing game or system memory or anything that cannot be done legitimately.

In short, we are not a hacking group nor are we interested in becoming one.


### Does this work on the Switch 2?

Yes! We have had full support for the Switch 2 since version 0.56.


### Is there any ban risk of this project?

To date, there are no known cases of anyone getting banned for using capture cards and 3rd party controllers.


### Are Pokémon caught with this project safe to use?

Yes. Pokémon found with automation are completely indistinguishable from manually found Pokémon. This is because it is done with the same controller inputs that are done with manual game play.

In contrast, hacked Pokémon are not always legal or safe to use. An incorrectly hacked Pokemon can "look legitimate", but may have subtle issues that prove it illegal in the future and get you disqualified from tournaments.


### What platforms and operating systems are supported?

**Supported:**

- **Windows on x64:** This is the preferred platform. It supports all features in the project and is the primary platform for most of the developers.
- **Mac on ARM:** This is the next supported platform. It does lack a few features and releases usually lag behind the Windows releases since it's maintained by a different set of developers. It is a bit messier to get working due to permissions.
- **Mac on x64:** Same as Mac on ARM. But it will eventually be phased out since Macs have migrated to ARM now.

**Not Supported:**

- **Linux on x64:** Not officially supported. The project will compile and run on Linux. But there are numerous issues with the biggest being video capture flicker.
- **Windows on ARM:** Not supported. You may be able to run the x64 binaries via emulation, but it will come with performance issues. Also expect lots of issues involving drivers.
- **Linux on ARM:** Not supported.

Platform/OS support is basically dictated by what the developers use. This project started in Windows. Then some Mac users (who were also developers) joined and made it work for Mac. But this has not happened for Linux yet. If you would like to be that person for Linux, please join us! We are open to contributions!


### Can I use a Raspberry Pi instead of a computer?

(not to be confused with the Raspberry Pi Pico as a controller)

No. Video inference and machine learning are extremely compute intensive and have difficulty running on even slightly old laptops. You will need a powerful computer.

Furthermore, the project is large enough as it is and we need to draw the line somewhere.


### Can I use a phone or a tablet instead of a computer?

No. Same reason as above.


### I'm an old user returning after a long absence. Is my Arduino/Teensy still good?

Yes and no.

We still support the old setups (Arduino/Teensy/Pro Micro), but they are deprecated in favor of the newer controllers (ESP32, ESP32-S3, Raspberry Pi Pico W).

- If you are coming from the old "microcontroller-only" programs, you will need to purchase and setup a UART. But in this case, it's much easier and cheaper to just to abandon your old hardware and get one of the newer controller setups which do not require a UART.
- If you are coming from the older computer-control setups and already have a UART, you can continue using it. But if you have any difficulty setting it up, we are going to tell you to just abandon it and get the newer controllers.

The newer controllers are cheaper, much easier to setup, and more reliable than the old ones with manual UART wiring.

If you are affected by the [Power Glitching](PowerGlitching.md) issue on the Switch 2, you will almost certainly want to upgrade to the new controllers.


## Technical Questions


### What happened to the Microcontroller-only (MC) setup?

Unfortunately, Microcontroller (MC) automation has been discontinued.

Computer Control (CC) has become so powerful and easy to use that it has obsoleted MC to the point that is a waste of time to continuing maintaining and supporting MC automation. We discontinued it only after it had been effectively abandoned for years and we didn't want to keep answering support questions about it.

The old Microcontroller wiki can still be found here:

- [Microcontroller Repo](https://github.com/PokemonAutomation/Microcontroller)
- [Microcontroller Setup Guide](https://github.com/PokemonAutomation/Microcontroller/blob/master/Wiki/SetupGuide/README.md)

However, it already breaks on the latest Switch firmware that added additional icons to the main menu.

If you are dead-set on MC automation without a computer, you will need to look elsewhere.


### Why can't you connect directly to the Switch over USB? Why do you need a microcontroller?

Game controllers are USB *devices*. USB ports on a computer are USB *hosts*.

The USB ports on a computer cannot be reprogrammed from USB host to USB device.


### Why can't you connect directly to the Switch using the computer's Bluetooth? NXBT and joycontrol can do this!

NXBT and joycontrol are both Linux only. Windows and Mac require the use of a VM which is well above the difficulty threshold for our target audience.

Linux is the only operating system that allows the low level access required to reprogram the bluetooth device to act as a wireless game controller. To do this on Windows, you would need a custom driver for the specific Bluetooth device. And we're not in the business of writing (signed) custom drivers for every Bluetooth controller on the market.

Beyond this, there are concerns about timing stability. Unlike microcontrollers, computers have much more noise due to background programs.


## Usage Questions


### Can I use a controller instead of a keyboard?

Unfortunately no. We tried to do this in the past only to have Qt pull the rug from under us by discontinuing the gamepad library. While we haven't given up on this, it's not very high on the priority list.

As an alternative, if you're using a modern controller (ESP32, ESP32-S3, Raspberry Pi Pico), you can manipulate the controller type dropdown to easily switch between the virtual controller and a real (handheld) controller.

**Switch from the virtual controller to a real controller:**

Set the controller type to `None`. This disconnects it from your Switch allowing you to connect your real controller.

**Switch from real controller back to the virtual controller:**

Disconnect your real controller, then change the controller type back to the desired controller. For wired controllers, you will need to press a button (via keyboard) to connect to the Switch. Wireless controllers will connect automatically* if they were previously already paired.

*Due to [issue 800](https://github.com/PokemonAutomation/Arduino-Source/issues/800), this does not work reliably for the ESP32 on the Switch 1. So you will likely need to go back to the grip menu to re-pair.


<hr>

**Discord Server:** 

[<img src="https://canary.discordapp.com/api/guilds/695809740428673034/widget.png?style=banner2">](https://discord.gg/cQ4gWxN)




