Muxpy
=====

A light-weight python tmux session handler, for saving and
restoring potentially elaborate tmux session setups.

Usage
=====

1. Save your current awesome setup to ``foobar``. Assuming uid 1000, replace as neccessary.

   ``muxpy -S /tmp/tmux-1000/default create foo``

   This will create a file called ``~/.muxpy/profiles/foo.json``.

2. Edit the file to fine-tune names and such.

   ``muxpy edit foo``

3. Start the new session.

   ``muxpy start foo``

HELP AND SUPPORT AND DEVELOPMENT
================================

The software is hosted and developed at https://github.com/bjornars/muxpy, and there might be some life at #muxpy at freenode.
