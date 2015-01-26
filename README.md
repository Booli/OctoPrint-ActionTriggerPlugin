OctoPrint-ActionTriggerPlugin
=============================


Plugin for OctoPrint that handles serial commands send out by the printer. These action triggers should be manually added to your firmware if you want to use this add-on.  Basic handler code is:

---


    // action:somevariable


Plugin reacts to two different situations, door open/close and filament deteciton.

    action:door_open
    action:door_closed

``action:door_open`` will pause the print and home the X-axis. Pop-up dialog will notify the user, they can decide to accept the pop-up and use the controls. Closing the door will trigger ``action:door_closed`` resume the print and close the dialog

    action:filament

This trigger will pause the print and home the X and Y axis, giving the user the opportunity to change out the filament. The print needs to be resumed manually through the UI.

Addon-on slogan:

    Its gun do some serial trigger handling yo
