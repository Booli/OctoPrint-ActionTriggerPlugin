# coding=utf-8
from __future__ import absolute_import, unicode_literals

import flask
import logging
import time

import octoprint.plugin
import octoprint.settings

default_settings = {
	"action_door": True,
	"action_filament": True
}

s = octoprint.plugin.plugin_settings("actiontrigger", defaults=default_settings)

##~~ Init Plugin and Metadata

__plugin_name__ = "Action Trigger"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_init__():
		global _plugin
		global __plugin_implementations__
		global __plugin_hooks__

		_plugin = ActionTriggerPlugin()
		__plugin_implementations__ = [_plugin]
		__plugin_hooks__ = {
			'octoprint.comm.protocol.action': _plugin.hook_actiontrigger,
			'octoprint.plugin.softwareupdate.check_config': _plugin.get_update_information
		}

class ActionTriggerPlugin(octoprint.plugin.TemplatePlugin,
						  octoprint.plugin.AssetPlugin,
						  octoprint.plugin.SettingsPlugin,
						  octoprint.plugin.EventHandlerPlugin):
	
		def __init__(self):
			self.filament_action = False

		##~~ TemplatePlugin
		def get_template_configs(self):
				return [
						dict(type="settings", name="Action Trigger", custom_bindings=False)
				]

		##~~ AssetsPlugin
		def get_assets(self):
				return dict(
						js=["js/actiontrigger.js"],
						css=["css/actiontrigger.css"]
				)

		##~ SettingsPlugin
		def on_settings_load(self):
				return dict(
						action_door=s.get_boolean(["action_door"]),
						action_filament=s.get_boolean(["action_filament"])
				)

		def on_settings_save(self, data):
				if "action_door" in data:
						s.set_boolean(["action_door"], data["action_door"])
				if "action_filament" in data:
						s.set_boolean(["action_filament"], data["action_filament"])


		##~~ ActionTriggerPlugin
		def hook_actiontrigger(self, comm, line, action_trigger):
				if action_trigger == None:
					return
				elif action_trigger == "door_open" and s.get_boolean(["action_door"]) and comm.isPrinting():
						self._send_client_message(action_trigger, dict(line=line))
						# might want to put this in separate function
						comm.setPause(True)
						self._printer.home("x")
				elif action_trigger == "door_closed" and s.get_boolean(["action_door"]):
						self._send_client_message(action_trigger, dict(line=line))
						comm.setPause(False)
				elif action_trigger == "filament" and s.get_boolean(["action_filament"]) and self.filament_action == False:
						self._send_client_message(action_trigger, dict(line=line))
						comm.setPause(True)
						self._printer.home("x")
						self.filament_action = True

		def get_update_information(self):
			# Define the configuration for your plugin to use with the Software Update
			# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
			# for details.
			return dict(
				octoprint_actiontrigger=dict(
					displayName="Action Trigger Plugin",
					displayVersion=self._plugin_version,

					# version check: github repository
					type="github_release",
					user="Booli",
					repo="OctoPrint-ActionTriggerPlugin",
					current=self._plugin_version,

					# update method: pip
					pip="https://github.com/Booli/OctoPrint-ActionTriggerPlugin/archive/{target_version}.zip"
				)
			)

		# Send trigger to front end
		def _send_client_message(self, message_type, data=None):
				self._plugin_manager.send_plugin_message("actiontrigger", dict(type=message_type, data=data))

		# Set flags on event
		def on_event(self, event, payload):
			if event == "PrintResumed" or event == "PrintStarted":
				self.filament_action = False
