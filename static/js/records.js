var Record = {

    showWarning : function() {
        requestData("POST", "html", '/records/show_warning/', {}, 
            function(response){
                var title = "Eliminazione registrazioni";
                var dict = {
                    title : title,
                    content : response,
                    onSave : Record.check,
                    saveButton : 'Conferma',
                    onRemove : null,
                }
            Modal.open(dict);
            }, function(error){
                showMessageBox("Errore", "Errore apertura maschera di eliminazione.", "alert-danger");
            }
        );
    },

    check : function(callback) {
        if($('#confirm-delete').is(':checked')) {
            Record.delete(callback);
        } else {
            showMessageBox("Errore", "Per eliminare &egrave; necessario confermare la propria scelta.", "alert-danger");
            callback({success: false});
        }
    },

    delete : function(callback){
        data = {}
        data.start_date = $('#start-date').val()
        data.end_date = $('#end-date').val()
        data.start_time = $('#start-time').val()
        data.end_time = $('#end-time').val()
        data.dst = $('#dst').val()
        data.pincode = $('#pincode').val()

        requestData("POST", "html", '/records/remove/', {data: data},
        function(response){
            var with_filter = (window.location.href.indexOf('?') > -1 ? '&':'?');
            window.location.href += with_filter + "ok=1&msg=Registrazioni eliminate con successo.";
            callback({success: true}); // inutile se facciamo cambio pagina
        },
        function(error){
            showMessageBox("Errore", "Errore eliminazione registrazioni.", "alert-danger");
            callback({success: false});
        })
    },
}