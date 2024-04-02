# Circuitikz GUI using Tkinter

Quick and dirty project for generating circuitikz LaTeX in a Tkinter GUI.

Place elements and nodes, then press space or any non-shortcut key to print out circuitikz latex to terminal window.

Inspired by:

[Paul Falstad's circuit simulator](https://falstad.com/circuit/)

[Matthew Bellafaire's Java based ciruitikz tool](https://github.com/Bellafaire/CircuiTikZ-Tool)

[Browser Circuitikz generator](https://grex99.gitlab.io/circuitgui/)

## Special Shortcuts
- m: click and drag to move. can drag endpoints of elements or body
- d: click to delete
- R: highlight then press shift-r to rotate. Only works on node labels and ground.
## Element Shortcuts: click and drag to place elements
- r: resistor
- c: capacitor
- l: inductor
- V: voltage source (shift-v)
- I: current source (shift-i)
- B: dependent voltage source (shift-b)
- O: dependent current source (shift-o)
- w: wire
- o: open
## Node Shortcuts: click to place
- g: ground node
- a: op amp. scaled up slightly from usual to allow grid alignment of terminals. input terminals are to the left and output terminal is to the right.
- v: node label / node voltage

# If I had infinite time
- Try to make this something that simulates circuits
- Try to make this something that's like Bret Victor's demo with node voltage and current traces.
