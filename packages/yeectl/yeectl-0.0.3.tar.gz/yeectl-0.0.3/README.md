# yeectl
Yeectl is a Python TUI for controlling Yeelights. It uses the [Yeelight Python library](https://gitlab.com/stavros/python-yeelight) to control the lights, and [py-cui](https://github.com/jwlodek/py_cui) to create an interface.
![](https://github.com/Bean499/yeectl/blob/main/.github/picture.png)

## Installation
To install remotely using `pip`:
```
pip install yeectl
```

To install from source using using `pip`:
```
git clone https://github.com/Bean499/yeectl
cd yeectl
pip install .
```

## Usage
Run `python -m yeectl`.

The colours displayed in the bottom right will be loaded from `~/.xresources` and `~/.config/yeectl/`.

The names of each light will be determined by the custom name set for their IP addresses. If a light does not have a custom name, it will be given a default name based on its model. If there is no set name for its model, it will simply be called "Yeelight".

### Setting Custom Names for Lights
`yeectl` reads the file `~/.config/yeectl/lights` to check for custom light names. Light IP addresses should be seperated from their name by a colon and a space.

Example `~/.config/yeectl/lights`:
```
0.0.0.0: Bedroom light
0.0.0.1: Desk lightstrip
```

### Importing Colours from XResources
`yeectl` will import any colours from `~/.xresources` that are set as `*.color` followed by anything.

### Importing Custom Colours
`yeectl` will import any custom colours from `~/.config/yeectl/colours` `~/.config/yeectl/colors`. Colour names should be seperated from their hexadecimal value by a colon and a space.

Example `~/.config/yeectl/colours`:
```
Red: #ff0000
Green: #00ff00
Blue: #0000ff
```

## Todo
* Add a hotkey to show the IP address of a light
* ~~Allow the user to manually name lights using a configuration file~~
* Load colours from `$XDG_CONFIG_HOME` instead of `~/.config`

## License
`yeectl` is licensed under the MIT license.

## Changelog

### 0.0.3
* Added ability to set custom light names
* Fixed a crash that would occur when a model doesn't have a set display name
### 0.0.2
* Fixed a few crashes
### 0.0.1
* First release
