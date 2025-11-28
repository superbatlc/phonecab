var Cdr = {

    changeValid : function(id, newstatus){
        var msg = "Attenzione! L\'abilitazione/disabilitazione di una chiamata influisce sul calcolo complessivo.\nSei sicuro di voler continuare?";

        if(confirm(msg)){

            var data = {};
            data.id = id;
            data.valid = newstatus;

            var url = '/cdrs/changevalid/';
            // Preserve current filters when refreshing the table after a validity toggle
            if (window.location.search) {
                url += window.location.search;
            }

            // data.params = params; //# TODO pass query params

            requestData("POST", "html", url, {data : data},
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
