# yeectl
Yeectl is a Python TUI for controlling Yeelights. It uses the [Yeelight Python library](https://gitlab.com/stavros/python-yeelight) to control the lights, and [py-cui](https://github.com/jwlodek/py_cui) to create an interface.
!(.github/picture.png)

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

### Importing Colours from XResources
`yeectl` will import any colours from `~/.xresources` that are set as `*.color` followed by anything.

### Importing Custom Colours
`yeectl` will import any custom colours from `~/.config/yeectl/colours` `~/.config/yeectl/colors`. Colour names should be seperated from their hexadecimal value by a colon and a space.

Example:
```
Red: #ff0000
Green: #00ff00
Blue: #0000ff
```

## Todo

* Add a hotkey to show the IP address of a light
* Allow the user to manually name lights using a configuration file
* Load colours from `$XDG_CONFIG_HOME` instead of `~/.config`

## License
`yeectl` is licensed under the MIT license.
