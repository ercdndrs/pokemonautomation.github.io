# Controller Guide

This is a guide for all the differnet controller types that we support.

## HID: Keyboard

| Image | Description | Supported Devices |
| --- | --- | --- |
| <img src="Images/Controllers/HID-Keyboard.jpg" width="300"> | A USB keyboard. | ESP32-S3<br>Pico W (UART mode) |

The HID keyboard is just a standard USB keyboard. Since it is not a controller, it cannot be used to play the Nintendo Switch. But it can be used to enter text fields include code entries.

**How to Connect:**

Since the HID keyboard is not a game controller, it does connect through the grip menu. Instead, it connects automatically whenever it's physically connected to the Switch.

Just bring up any Switch menu that has a keyboard or a numberpad, and the HID keyboard will work. Programs that do code entry (such as Fast Code Entry) will enter the code right away. If your window has keyboard controls active, just begin typing into your keyboard and it will show up on the Switch's text field.

**Keyboard Layouts:**

The default keyboard layout is the US QWERTY layout. If either your computer or your Switch is not QWERTY, what you type into your keyboard will not be what shows up on the Switch.

If your computer's keyboard layout does is not QWERTY, you will need to change the option in the settings:

- Settings (bottom left corner of the program) -> "System Keyboard Layout"

As of this writing, we only support QWERTY and the French AZERTY. We are open to contributions of other keyboard layouts.



## NS1: Wired Controller

| Image | Description | Supported Devices |
| --- | --- | --- |
| <img src="Images/Controllers/Switch1-Horipad-Wired.jpg" width="300"> | 3rd Party Wired Controller | ESP32-S3<br>Pico W (UART mode) |

This is the standard 3rd party wired controller from the likes of Horipad and Power A. It supports 14 buttons and 2 joysticks. It does not support rumble or gyro. Furthermore, it always shows up as a black controller in the Switch menus.

**How to Connect:**

As a wired controller, you do not need to be in the grip menu to connect. Just press any button and it will connect.

Note that if you are in one player game and you already have a controller connected as the 1st controller slot, you will not be able to connect any other controller until you either disconnect that controller or return to the Switch menus.

<img src="Images/Controllers/NS1-WiredController.png" width="600">



## NS2: Wired Controller

| Image | Description | Supported Devices |
| --- | --- | --- |
| <img src="Images/Controllers/Switch2-PowerA-Wired.jpg" width="300"> | 3rd Party Wired Controller | ESP32-S3<br>Pico W (UART mode)<br>Arduino Uno R3<br>Arduino Leonardo<br>Pro Micro<br>Teensy 2.0<br>Teensy++ 2.0 |

This is the standard 3rd party wired controller for the Switch 2 from the likes of Horipad and Power A. It supports 17 buttons and 2 joysticks and it backwards compatible with the Switch 1. It does not support rumble or gyro. Furthermore, it always shows up as a black controller in the Switch menus.

**How to Connect:**

As a wired controller, you do not need to be in the grip menu to connect. Just press any button and it will connect.

Note that if you are in one player game and you already have a controller connected as the 1st controller slot, you will not be able to connect any other controller until you either disconnect that controller or return to the Switch menus.

<img src="Images/Controllers/NS2-WiredController.png" width="600">




<hr>

**Discord Server:** 


[<img src="https://canary.discordapp.com/api/guilds/695809740428673034/widget.png?style=banner2">](https://discord.gg/cQ4gWxN)





