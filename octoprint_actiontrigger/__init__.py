# coding=utf-8
from __future__ import absolute_import

__author__ = "Pim Rutgers <pim.rutgers@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"

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

__plugin_name__ = "ActionTriggerPlugin"
__plugin_version__ = "0.1"
__plugin_description__ = "Hooks to specific serial commands from the printer. Actions are handled accordingly"

def __plugin_init__():
		global _plugin
		global __plugin_implementations__
		global __plugin_hooks__

		_plugin = ActionTriggerPlugin()
		__plugin_implementations__ = [_plugin]
		__plugin_hooks__ = {'octoprint.comm.protocol.action': _plugin.hook_actiontrigger}

class ActionTriggerPlugin(octoprint.plugin.TemplatePlugin,
						  octoprint.plugin.AssetPlugin,
						  octoprint.plugin.SettingsPlugin):

		##~~ TemplatePlugin
		# this might needs some vars later on
		def get_template_configs(self):
				return [
						dict(type="settings", name="Action Trigger", custom_binding=False)
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
						action_door=s.getBoolean(["action_door"]),
						action_filament=s.getBoolean(["action_filament"])
				)

		def on_settings_save(self, data):
				if "action_door" in data and data["action_door"]:
						s.setBoolean(["action_door"], data["action_door"])
				if "action_filament" in data and data["action_filament"]:
						s.setBoolean(["action_filament"], data["action_filament"])




		##~~ ActionTriggerPlugin
		def hook_actiontrigger(self, comm, line, action_trigger):
				if action_trigger == None:
					return
				elif action_trigger == "door":
						self._send_client_message(action_trigger, dict(line=line))
						comm.setPause(True)
				elif action_trigger == "filament":
						self._send_client_message(action_trigger, dict(line=line))
						comm.setPause(True)

		# Send trigger to front end
		def _send_client_message(self, message_type, data=None):
				self._plugin_manager.send_plugin_message("actiontrigger", dict(type=message_type, data=data))
