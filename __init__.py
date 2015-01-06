# coding=utf-8
from __future__ import absolute_import

__author__ = "Pim Rutgers <pim.rutgers@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"

import octoprint.plugin
import logging
import time

class ActionTriggerPlugin(octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.AssetPlugin):
        def __init__(self):
                self._logger = logging.getLogger("octoprint.plugin.actiontrigger")

        ##~~ TemplatePlugin
        def get_template_folder(self):
                import os
                return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        ##~~ AssetsPlugin
    	def get_asset_folder(self):
    		import os
    		return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

    	def get_assets(self):
    		return {
    			"js": ["js/actiontrigger.js"],
    			"css": ["css/actiontrigger.css"]
    		}
