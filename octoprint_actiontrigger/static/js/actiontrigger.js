$(function() {
  function ActionTriggerViewModel(parameters) {
    var self = this;

    self.loginState = parameters[0];
    self.printerState = parameters[1];
    self.control = parameters[2];
    self.settingsViewModel = parameters[3];

    self.actionTriggerTemplate = ko.observable(undefined);

    self.showActionTriggerDialog = function (data) {
      var actionTriggerDialog = $("#action_trigger_dialog");
      var actionTriggerDialogAck = $(".action_trigger_dialog_acknowledge", actionTriggerDialog);

      $(".action_trigger_title", actionTriggerDialog).text(data.title);
      $(".action_trigger_dialog_message", actionTriggerDialog).text(data.message);
      actionTriggerDialogAck.unbind("click");
      actionTriggerDialogAck.bind("click", function (e) {
        e.preventDefault();
        $("#action_trigger_dialog").modal("hide");
        self.showControls();
        //prob going to do some stuff here huh.
      });
      actionTriggerDialog.modal({
        show: 'true',
        backdrop:'static',
        keyboard: false
      });


    };

    //$('#action_trigger_dialog').on('hidden', function(){
    //  $('#action_trigger_dialog').data('modal', null);
    //});

    self.onBeforeBinding = function() {
      self.settings = self.settingsViewModel.settings;
    };

    self.showControls = function() {
      $('#tabs a[href="#control"]').tab('show')
    };

    self.onDataUpdaterPluginMessage = function (plugin, data) {
      if (plugin != "actiontrigger") {
        return;
      };

      var messageType = data.type;
      var messageData = data.data;

      // Process action_trigger call from plugin
      switch (messageType) {
        case "filament":
          messageData.title = "Attention! Filament stop detected!";
          self.actionTriggerTemplate(messageType);
          self.showActionTriggerDialog(messageData);
          break;
        case "door_open":
          messageData.title = "Attention! Door is open!";
          self.actionTriggerTemplate(messageType);
          self.showActionTriggerDialog(messageData);
          break;
        case "door_closed":
          $("#action_trigger_dialog").modal("hide");
          break;


        //Do nothing
      };
    };

  };
  ADDITIONAL_VIEWMODELS.push([ActionTriggerViewModel, ["loginStateViewModel", "printerStateViewModel", "controlViewModel", "settingsViewModel"], document.getElementById("action_trigger_dialog")]);
});
