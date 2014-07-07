# HermesSkypeControl

Python scripts to control Hermes playback when Skype recieves and hangs up a call.

It's not organized as a real module and is subject to change.

## Usage

Make sure to clone using submodules: `git clone --recursive git@github.com:winny-/HermesSkypeControl.git`

See [HermesApp/Hermes#183 Feature Request: Pause Hermes When Skype Call Starts](https://github.com/HermesApp/Hermes/issues/183) for more information on how to configure your Python so it doesn't segfault.

Once your Python is configured, invoke the script `hermes_skype_control.py`.

## Limitations

Can not automatically reconnect to Skype when Skype is restarted.
