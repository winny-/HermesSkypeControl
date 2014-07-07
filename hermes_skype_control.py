#!/usr/bin/env python


from hermes_remote import HermesRemote
import Skype4Py
import time
import sys
import argparse


please_resume = None
was_playing = False
remote = HermesRemote()


def attach_hermes_control(resume=True, timeout=5000):
	global please_resume
	please_resume = resume
	skype = Skype4Py.Skype()
	skype.Timeout = timeout
	skype.Attach()

	skype.OnCallStatus = on_call_status

	return skype


def main():
	parser = argparse.ArgumentParser(description='Automatically start/stop Hermes playback on Skype call start/end')
	parser.add_argument('--no-resume', action='store_false', help='Do not resume playback after a Skype call hang up')
	args = parser.parse_args()

	sys.stdout.write('Connecting:')
	sys.stdout.flush()
	skype = None
	while skype is None:
		try:
			skype = attach_hermes_control(resume=args.no_resume)
		except Skype4Py.errors.SkypeAPIError:  # Skype is not running, wait.
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(1)
	print(' connected!')
	print('Skype is attached. Sleeping forever.')
	while True:
		time.sleep(10)


def on_call_status(call, status):
	global please_resume
	global was_playing
	command = None
	message = None

	if status == Skype4Py.clsInProgress:  # Call started
		message = 'Call started'
		was_playing = remote()['info']['state'] == 'playing'
		if was_playing:
			command = 'pause'
	elif status == Skype4Py.clsFinished:  # Call finished
		message = 'Hung up'
		if please_resume and was_playing:
			command = 'play'
		was_playing = False

	if message:
		print('{}{}.'.format(
			message,
			', will '+command if command else '',
		))
	if command:
		remote(command)


if __name__ == '__main__':
	main()
