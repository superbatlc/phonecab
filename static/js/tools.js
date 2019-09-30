var Tool = {

    editActivation : function(id){
        var data = {};
        data.activation_time = $("#profile-first-name").val()
        data.deactivation_time = $("#profile-last-name").val()

        requestData("PUT", "html", '/tools/' + id + '/', {data : data},
            function(response){
                updateDOM('.application', response);
            },
            function(error){
              callback({success:false}); return;
            }
        );
    },

    removeActivation : function(id){
        requestData("DELETE", "html", '/tools/' + id + '/', {},
            function(response){
                var with_filter = (window.location.href.indexOf('?') > -1 ? '&':'?');
                window.location.href += with_filter + "ok=1&msg=Attivazione eliminata con successo.";
                // callback({success: true}); // inutile se facciamo cambio pagina
            },
            function(error){
                showMessageBox("Errore", "Errore eliminazione attivazione.", "alert-danger");
                callback({success: false});
            }
        );
    }
}
