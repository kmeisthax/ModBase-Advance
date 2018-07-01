ModBase is a template project for split disassemblies of old videogame
software. This particular template targets GBA software using the armips
assembler.

## Requirements

* Latest version of armips
* Python (any version)
* make (probably GNU make)

## Getting started

*If you wish to disassemble a game with multiple versions, please take a look
at the section entitled Multiple Base ROMs.*

First, download this project's .zip file and create a new repository from it.
Do not create a GitHub fork for your repository - new build code committed here
is not guaranteed to be relevant or compatible with your project. Do, however,
create a new Git repository to store your code.

Place your base ROM in base/ and alter lines 12-13 of the Makefile to point at
the file. For example, if your file is base/Tumiki_Fighters.gba, then change

    BASEROM := ${BASE_DIR}/baserom.gba
    BUILDROM := ${BUILD_DIR}/baserom.gba

to

    BASEROM := ${BASE_DIR}/Tumiki_Fighters.gba
    BUILDROM := ${BUILD_DIR}/Tumiki_Fighters.gba

You may now add code to src/ representing your game. As you add code, it will
automatically be included in the project, compiled, and verified against the
base ROM. If you introduce a mistake into your project, you will recieve an
error, such as:

    cmp build/Frozen_Bubble.gba base/Frozen_Bubble.gba
    build/Frozen_Bubble.gba base/Frozen_Bubble.gba differ: char 14, line 23

You can diagnose these errors using hexdump -C, cmp --verbose, or any graphical
hex editor with a compare feature.

### Convention is important!

By our default Makefile configuration, src/ holds all disassembled game code.
Furthermore, standard convention is to store all code and assets within specific
component folders. For example, if your game had a titlescreen with image assets
and UI code, then you would have the following files:

    src/titlescreen/state_machine.asm
    src/titlescreen/resources.asm
    src/titlescreen/background_gfx.png
    src/titlescreen/sprite_gfx.png
    
The purpose of grouping code and coupled assets together in component
directories is to clearly indicate the relationship between the two. For the
same reason, any labels declared in *.asm files should be prefixed with the
name of the component directory the file exists within. This is so that
references from other *.asm files to this symbol will always indicate what
directory a symbol's code is. Furthermore, exported labels should be CamelCased
with a single _ separating the component from the rest of the label; while local
labels should be always lowercase with an _ in lieu of spaces between words.
Don't be afraid of long labels.

Avoid long files with large amounts of code. The longer the file, the harder for
people to scan through it. At the same time, a single *.asm file must have a
clearly indicated purpose. If your game has a state machine, then you create a
state_machine.asm file and put the state table and code in there. If your game
has a custom scripting language with 300 opcodes, you may want to split up their
implementations according to purpose. Perhaps something like:

    src/scriptvm/opcodes/arithmetic.asm
    src/scriptvm/opcodes/resource_ldr.asm
    src/scriptvm/opcodes/sprite_choreo.asm
    src/scriptvm/opcodes/playfield.asm

This also demonstrates how you can group files within a subdirectory of a
component. Just as long files are a detriment to readability, so are long
directories. You do not have to prefix labels with both directories, however.

Code within an *.asm file must be formatted correctly. Labels should be always
indicated; there should be no memory locations scattered throughout the code.
All code should be indented with four spaces. An empty line should be added
after every string of instructions that write memory or alter control flow.
Conditional branches should include a label for the branch not taken. Don't be
afraid to rename labels or do other sweeping refactors if the current set of
labels don't accurately describe the function of the code. Use comments, but
only to explain the purpose of an exported label, or where the behavior of the
code isn't obvious from the labels and instructions in use.

What looks more readable to you?

    .gba
    .open "build/Gunroar.gba", 0x80000000
    start:
    bl 0x802B3710
    bl statemachine
    ldr r1, =0x0300C420
    beq @@nothing_todo
    bl linktx
    @@nothing_todo:
    bx R0
    .pool
	 .close
    
Or?

    .gba
    .open "build/Gunroar.gba", 0x80000000
    GameLoop:
        bl LCDC_ExecuteDMA
        bl Game_StateMachine
        ldr r1, =I_SIO_Connected
        beq @@no_link_connection
        
    @@link_connection:
        bl SIO_RunLinkTxDriver
        
    @@no_link_connection:
        bx R0
    .pool
	 .close

### Multiple Base ROMs

Some games may share code across multiple ROM images. For example, the game may
have a 1.1 revision, or was released in multiple versions, or have multiple
translations. In this case, you will need to modify the build system to be aware
of multiple builds of the ROM image.

First, you will need to declare a BASEROM and BUILDROM for each version of the
game you want to build. Because of some armips quirkiness which we will get to
shortly, this particular iteration of ModBase treats BASEROM and BUILDROM as
lists:

    BASEROM := ${BASE_DIR}/Tumiki_Fighters_(U).gba ${BASE_DIR}/Tumiki_Fighters_(E).gba
    BUILDROM := ${BUILD_DIR}/Tumiki_Fighters_(U).gba ${BUILD_DIR}/Tumiki_Fighters_(E).gba

No further modification to the Makefile is necessary, because armips is an
overlay assembler. asm files directly reference whichever files they intend to
modify, and there's no object format. Hence, we don't need to modify the
Makefile to include or ignore specific asm files in different ROMs. The asm
files will include or ignore themselves.

## Adding image resources

**To be determined.**