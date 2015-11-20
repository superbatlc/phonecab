var Realtime = {

    mode : false,

    init : function(actualMode) {
        console.log(actualMode);
        Realtime.setMode(!!actualMode);
    },

    setMode : function(mode) {
        Realtime.mode = mode;

        $('#rt-modo-giorno').parent().removeClass('green red').addClass((mode ? 'green' : 'red'));
        $('#rt-modo-' + (mode ? 'notte' : 'giorno')).hide();
        $('#rt-modo-' + (mode ? 'giorno' : 'notte')).show();
    },

    toggleMode : function() {
        var newMode = !Realtime.mode;
        requestData("POST", "html", '/daynight/', {mode : newMode},
            function(response){
                Realtime.setMode(newMode);
            },
            function(error){
                showMessageBox("Errore", "Errore " + (newMode? "disattivazione linee" : "attivazione linee") + ".", "alert-danger");
            }
        );
    }

}