Uses the dshot600 protocol to communicate with the a blheli32 ESC and receive telemetry.  Telemetry data is used to calculate KV and all info is displayed on the OLED.

Great for testing hand wound motors KV or new/troublesome motors.

Optional loadcell can be added to the pin header highlighted with the orange circle below.  Data is printed via serial every 2-3ms.

20 second demo video https://www.youtube.com/watch?v=VLMNEdSz4wI

Schematics and PCB https://easyeda.com/jyesmith/kv-meter

<img src="/images/top loadcell.jpg" width="300"> <img src="/images/bottom.jpg" width="300">

Results form a rewound emax 2306 stator.  Left is with 8 turns and the right images is with 9 turns.

<img src="/images/8turn.jpg" width="300"> <img src="/images/9turn.jpg" width="300">

**WARNING - If `#define MINIQUADTESTBENCH` is uncommented the test sequence used by https://www.miniquadtestbench.com/ will automatically start!!!**  Below shows the results of testing an original EMAX RS2306 2400KV motor against the same motor wound with 0.5mm wire 8 & 9 turns per tooth.

<img src="/data/EMAX RS2306 2400KV/comparison plots 4s.png" width="600">

<img src="/data/EMAX RS2306 2400KV/comparison plots 4s zoomed.png" width="600">

## BOM

- Upload the gerber zip in the pcb folder to jlcpcb.com, select 1.6mm PCB thickness, and your favourite colour.
- ESP32 development board.  Get the same one as in the images above to be sure it mounts correctly.  I removed the black plastic standoff on the pins so that it sits flat on the PCB and gives enough headroom for the upper PCB and regulator.
- You favourite blheli32 esc.  Make sure it has telemetry out and ideally a current sensor.
- OLED 128*64.  There are 2 common version but the Vcc and GND pins are swapped.  This PCB has been designed to take both and you select which pin receives Vcc/GND by soldering the jumpers.
- A 3V3 or 5V regulator.  Either can be used and solder the jumper to which ever voltage you have used.  This makes sure the ESP32 is powered correctly.
- Optional loadcell for measuring thrust.

<img src="/pcb/pcb.png" width="600">

## If you make one I would love to see it.  Please post your pics as an issue or add them to this readme :)
