# bgi
### *"Background Image Interface"*

> *DISCLAIMER: This tool is designed to work with the rest of my personal ecosystem.*
>
> It does detect and disable gimmicks that apply to my environment and has
> a design generialized appropriately to be used in other linux environments well.

This tool supports:

 - feh enabled wm's: `i3wm`, `dwm`, `awesomewm`, `xmonad`
 - `sway` is also supported.

## Usage

#### Setting the background

It's as simple as! `bgi some.png`

#### Looping and scrolling through images

> The difference between looping and scrolling is given a set of images,
> scrolling makes a single pass over the set and looping makes multiple or infinite passes.

 - `bgi scroll -L path/to/images/`
 - `bgi loop -L path/to/images/`
 - `bgi loop --speed 2 --iter 12 a.png b.png c.jpg`

## Installation

### pip

 - `pip install https://github.com/mental32/bgi`
