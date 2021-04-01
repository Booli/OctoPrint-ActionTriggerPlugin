# coding=utf-8
from __future__ import absolute_import, unicode_literals

import octoprint.plugin


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

    def get_settings_defaults(self):
        return {
            "action_door": True,
            "action_filament": True
        }

    ##~~ ActionTriggerPlugin

    def hook_actiontrigger(self, comm, line, action_trigger, *args, **kwargs):
        if action_trigger is None:
            return
        elif action_trigger == "door_open" and self._settings.get_boolean(["action_door"]) and comm.isPrinting():
            self._send_client_message(action_trigger, dict(line=line))
            # might want to put this in separate function
            comm.setPause(True)
            self._printer.home("x")
        elif action_trigger == "door_closed" and self._settings.get_boolean(["action_door"]):
            self._send_client_message(action_trigger, dict(line=line))
            comm.setPause(False)
        elif action_trigger == "filament" and self._settings.get_boolean(["action_filament"]) and self.filament_action is False:
            self._send_client_message(action_trigger, dict(line=line))
            comm.setPause(True)
            self._printer.home("x")
            self.filament_action = True

    # Send trigger to front end
    def _send_client_message(self, message_type, data=None):
        self._plugin_manager.send_plugin_message("actiontrigger", dict(type=message_type, data=data))

    # Set flags on event
    def on_event(self, event, payload):
        if event == "PrintResumed" or event == "PrintStarted":
            self.filament_action = False

    # Software Update Hook
    def get_update_information(self):
        return dict(
            octoprint_actiontrigger=dict(
                displayName="Action Trigger Plugin",
                displayVersion=self._plugin_version,
                type="github_release",
                user="Booli",
                repo="OctoPrint-ActionTriggerPlugin",
                current=self._plugin_version,
                stable_branch=dict(
                    name="Stable", branch="master", comittish=["master"]
                ),
                prerelease_branches=[
                    dict(
                        name="Release Candidate",
                        branch="rc",
                        comittish=["rc", "master"],
                    )
                ],
                pip="https://github.com/Booli/OctoPrint-ActionTriggerPlugin/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "Action Trigger"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = ActionTriggerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        'octoprint.comm.protocol.action': __plugin_implementation__.hook_actiontrigger,
        'octoprint.plugin.softwareupdate.check_config': __plugin_implementation__.get_update_information,
    }
