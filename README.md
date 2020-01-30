# xbg
## X11 Background Image Interface

## Index

## Brief

## Usage

 - `xbg some.png`

#### Looping and scrolling through images

> The difference between looping and scrolling is given a set of images:
>  - scrolling makes a single pass over the set,
>  - looping makes multiple or infinite passes.

 - `xbg ./path/to/images/ --action random`
 - `xbg ./path/to/images/ --action scroll`
 - `xbg ./image.png --action loop --delay 2`

## Installation

 - `pip install --user https://github.com/mental32/xbg`
