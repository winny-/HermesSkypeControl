import json
import subprocess
import os


class HermesRemote(object):

	def __init__(self, script=None):
		"""
		Initialize a HermesRemote object

		script -- path to the script file
		"""
		if script is None:
			directory = os.path.dirname(os.path.realpath(__file__))
			script = os.path.join(directory, 'HermesRemote/api/_scripts/status.applescript')
		self.script = script

	def __call__(self, command=None):
		"""
		Get status and send commands to Hermes

		command -- the command to send to Hermes. Defaults to None.
		"""
		command = [command] if command is not None else []
		invocation = ['osascript', self.script] + command
		process = subprocess.Popen(invocation, stdout=subprocess.PIPE)
		output, error = process.communicate()
		if process.returncode != 0:
			raise HermesRemoteException('Bad exit code ({})'.format(process.returncode))
		if error:
			raise HermesRemoteException('Standard error is not empty. "{}"'.format(error))
		if not command:
			try:
				parsed = json.loads(output)
			except ValueError as ex:
				raise HermesRemoteException('Bad JSON "{}"'.format(output))
			return json.loads(output)


class HermesRemoteException(Exception):
	pass


