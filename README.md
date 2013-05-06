# pattirc

## Setup

### Dependencies

Install ```appdotnet``` from https://github.com/simondlr/Python-App.net-API-Wrapper:

```
$ git clone git://github.com/simondlr/Python-App.net-API-Wrapper.git
$ sudo setup.py install
```

### Get access token

Now get an access token via Jonathan Duerig's DevLite and copy it into ```config.cfg``` (You'll know where)

That's it. You're ready to go.

## Invocation

```
$ ./pattirc.py
```

## Usage

### "Normal mode"

You start in "normal mode". You can scroll through your buffer with ```j``` and  ```k``` and change buffers with ```h``` and ```l```.

### Command mode

Press ```:``` to go into command mode. You can now enter a command and press enter.

Currently supported commands:

  * ```q```: Quit pattirc

### Message mode

Press ```i``` to enter message mode. type a message and press enter. This message will be sent to the currently selected channel.
