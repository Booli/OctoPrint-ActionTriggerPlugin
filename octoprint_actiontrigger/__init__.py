# coding=utf-8
from __future__ import absolute_import

__author__ = "Pim Rutgers <pim.rutgers@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"

import flask
import octoprint.plugin
import logging
import time


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
						  octoprint.plugin.AssetPlugin):
		def __init__(self):
				self._logger = logging.getLogger("octoprint.plugin.actiontrigger")
				self._plugin_manager = None


		@property
		def plugin_manager(self):
			if self._plugin_manager is None:
				self._plugin_manager = octoprint.plugin.plugin_manager()
			return self._plugin_manager

		##~~ TemplatePlugin
		def get_template_folder(self):
				import os
				return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

		##~~ AssetsPlugin
		def get_asset_folder(self):
			import os
			return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

		def get_assets(self):
			return dict(
				js=["js/actiontrigger.js"],
				css=["css/actiontrigger.css"]
			)

		##~~ ActionTriggerPlugin
		def hook_actiontrigger(self, comm, line, action_trigger):
				if action_trigger == "door":
						self._send_client_message(action_trigger, dict(line=line))
						comm.setPause(True)

		# Send trigger to front end
		def _send_client_message(self, message_type, data=None):
				self.plugin_manager.send_plugin_message("actiontrigger", dict(type=message_type, data=data))
