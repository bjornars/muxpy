Muxpy
=====

A light-weight python tmux session handler, for saving and
restoring potentially elaborate tmux session setups.

Usage
=====

1. Save your current awesome setup to ``foobar``. Assuming uid 1000, replace as neccessary.

   ``./muxy -S /tmp/tmux-1000/default create foo``

   This will create a file called ``~/.muxpy/profiles/foo.json``.

2. Edit the file to fine-tune names and such.

   ``./muxpy edit foo``

3. Start the new session.

   ``./muxpy start foo``


TODO
====
* Better code quality
* requirements.txt and pip-packaging and stuff.
* Support more profile formats, like YAML and XML (just kidding). Autodetect format for reading.
* Add more fields to the profile for restoring, such as working directories, virtual env setups and program execution (might have to be implemented with send-keys to the tmux-pane).
* ???
* Profit!
