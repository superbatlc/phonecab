var Cdr = {

    changeValid : function(id, newstatus){
        var msg = "Attenzione! L\'abilitazione/disabilitazione di una chiamata influisce sul calcolo complessivo.\nSei sicuro di voler continuare?";
    
        if(confirm(msg)){

            var data = {};
            data.id = id;
            data.custom_valid = newstatus;

            requestData("POST", "html", '/cdrs/changevalid/', {data : data},
                function(response){
                    updateDOM('.cdrs', response);
                    showMessageBox("Conferma", "Modifica stato chiamata effettuata con successo.", "green");
                },
                function(error){
                    showMessageBox("Errore", "Modifica stato non effettuata.", "alert-danger");
                });
        }

        return;
    },





}



