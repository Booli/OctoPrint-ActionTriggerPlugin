$(function() {
  function ActionTriggerViewModel(parameters) {
    var self = this;

    self.loginState = parameters[0];
    self.printerState = parameters[1];
    self.control = parameters[2];



    self.showActionTriggerDialog = function(data) {
      //Need to figure out of this is only showing, or also some processing
      var actionTriggerDialog = $("#action_trigger_dialog");
      var actionTriggerDialogAck = $(".action_trigger_dialog_acknowledge", actionTriggerDialog);

      $(".action_trigger_title", actionTriggerDialog).text(data.trigger_title)
      $(".action_trigger_dialog_message", actionTriggerDialog).text(data.message);
      actionTriggerDialogAck.unbind("click");
      actionTriggerDialogAck.bind("click", function(e) {
        e.preventDefault();
        $("#action_trigger_dialog").modal("hide");
        //prob going to do some stuff here huh.
      });
      actionTriggerDialog.modal("show");


    }

    self.processActionTrigger = function(data)

    }

    self.onDataUpdaterPluginMessage = function(plugin, data) {
      if (plugin != "actiontrigger") {
        return;
      }

      var messageType = data.type;
      var messageData = data.data;

      switch(messageType) {
        case "pause" {
          //Call pause stuff
        }
        case "resume" {
          //Call resume stuff
        }
        case "disconnect" {
          //Call disconect stuff
        }
        case "filament" {
          //Call filament stuff
        }
        case "door" {
          //Call door stuff
        }
      //Do nothing
      }
    }


  ADDITIONAL_VIEWMODELS.push([ActionTriggerViewModel, ["loginStateViewModel", "printerStateViewModel", "controlViewModel"], document.getElementById("action_trigger_dialog")]);
}
