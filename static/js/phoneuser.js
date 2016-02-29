var Phoneuser = {

        edit : function(id){
            requestData("POST", "html", '/phoneusers/edit/', {id : id},
                function(response){
                    var title = "Nuova Anagrafica";
                    if (id) title = "Modifica Anagrafica";
                    var dict = {
                        title : title,
                        content : response,
                        onSave : Phoneuser.save,
                        onRemove : null,
                    }
                Modal.open(dict);
                }, function(error){
                    showMessageBox("Errore", "Errore apertura maschera di modifica.", "alert-danger");
                }
            );
        },

        check : function(isNew,callback){
            // async check
            // chiama il callback con {success:bool} al termine
            var ok = true;

            ok &= checkEmptyField("#first-name");
            ok &= checkEmptyField("#last-name");
            ok &= checkEmptyField("#serial-no");

            if(isNew && ok){
              checkUniquePincode("#pincode", callback);
            } else {
              callback({success:ok}); return;
            }
        },

        save : function(callback){
            // async action
            // chiama il callback con {success:bool} al termine
            var data = {};
            var isNew = false;
            data.phoneuser_id = $('#phoneuser-id-modal').val();
            if (data.phoneuser_id == "None" || data.phoneuser_id == ''){
                data.phoneuser_id = "0";
                isNew = true;
            }

            var postCheck = function(callback_return){
                // async post save
                // chiama il callback di save con {success:bool} al termine
                if (!callback_return.success) { callback({success:false}); return; }

                data.enabled = 0
                if($("input[type=checkbox]#enabled").is(':checked')){
                    data.enabled = 1
                }

                data.first_name = $("#first-name").val()
                data.last_name = $("#last-name").val()
                data.serial_no = $("#serial-no").val()
                data.pincode = $("#pincode").val()
                data.language = $("#language").val()

                data.four_bis_limited = 0
                if($("input[type=checkbox]#four-bis-limited").is(':checked')){
                    data.four_bis_limited = 1
                }

                data.listening_enabled = 0
                if($("input[type=checkbox]#listening-enabled").is(':checked')){
                    data.listening_enabled = 1
                }
                data.recording_enabled = 0
                if($("input[type=checkbox]#recording-enabled").is(':checked')){
                    data.recording_enabled = 1
                }

                //data.vipaccount = 0
                //if($("input[type=checkbox]#vipaccount").is(':checked')){
                //    data.vipaccount = 1
                //}
                //

                requestData("POST", "html", '/phoneusers/save/', {data : data},
                    function(response){
                      if(isNew) {
                        updateDOM('#phoneusers', response); // ricarichiamo la lista
                      }
                      else updateDOM('#phoneuser', response); // ricarichiamo il dettaglio
                      showMessageBox("Conferma", "Salvataggio anagrafica effettuato con successo.", "green");
                      callback({success:true}); return;
                    },function(error){
                      showMessageBox("Errore", "Errore salvataggio.", "alert-danger");
                      callback({success:false}); return;
                    }
                );
            }

            // chiama postCheck al termine del check (passando {success:bool})
            Phoneuser.check(isNew,postCheck);
        },

        changeStatus : function(id, newstatus){
            var data = {};
            data.phoneuser_id = id;
            data.newstatus = newstatus;

            var action = "Disabilitazione";
            if(newstatus == "1"){
                action = "Abilitazione";
            }

            requestData("POST", "html", '/phoneusers/changestatus/', {data : data},
                function(response){
                    updateDOM('#phoneuser', response);
                    showMessageBox("Conferma", action + " anagrafica effettuata con successo.", "green");
                },
                function(error){
                    showMessageBox("Errore", "Errore " + action + " anagrafica.", "alert-danger");
                });

        },

        archive : function(id){
            var msg = "Attenzione! L\'archiviazione sposterà tutti i dati relativi a questa anagrafica in Archivio.\nÈ un processo irreversibile.\nSei sicuro di voler continuare?";

            if(confirm(msg)){
                phoneuser_id = $('#phoneuser-id').val();

                requestData("POST", "html", '/phoneusers/archive/', {phoneuser_id : phoneuser_id},
                function(response){
                    window.location.href = "/phoneusers/?ok=1&msg=Anagrafica archiviata con successo.";
                },
                function(error){
                    console.log(error);
                    showMessageBox("Errore", "Errore archiviazione anagrafica.", "alert-danger");
                });
            }

            return;
        },
}


var Whitelist = {

    edit : function(id, phoneuser_id){
        if(id == 0){
            phoneuser_id = $('#phoneuser-id').val();
        }
        data = {
            id: id,
            phoneuser_id: phoneuser_id
        }

        requestData("POST", "html", '/whitelists/edit/', {data : data}, function(response){
            var title = "Nuova Autorizzazione";
            if (id) title = "Modifica Autorizzazione";
            var dict = {
                title : title,
                content : response,
                onSave : Whitelist.save,
                onRemove : null,
            }
            Modal.open(dict);

        });
    },

    check : function(whitelist_id, callback){
        // async check
        // chiama il callback con {success:bool} al termine
        var ok = true;

        ok &= checkEmptyField("#whitelist-label");
        ok &= checkEmptyField("#whitelist-phonenumber");
        ok &= checkEmptyField("#whitelist-duration");

        if(ok){
              phoneuser_id = $('#whitelist-phoneuser-id').val()
              checkUniqueWhitelist("#whitelist-phonenumber", phoneuser_id, whitelist_id, callback);
            } else {
              callback({success:ok}); return;
            }

        return ok;
    },

    save : function(callback){

        // async action
        // chiama il callback con {success:bool} al termine
        var data = {};

        data.whitelist_id = $('#whitelist-id').val();
        if (data.whitelist_id == "None" || data.whitelist_id == ''){
            data.whitelist_id = "0";
        }

        // async post save
        // chiama il callback di save con {success:bool} al termine
        //if (!Whitelist.check(isNew, callback)) { callback({success:false}); return; }
        var postCheck = function(callback_return){
            // chiama il callback di save con {success:bool} al termine
            if (!callback_return.success) { callback({success:false}); return; }

            data.label = $("#whitelist-label").val()
            data.phonenumber = $("#whitelist-phonenumber").val()
            data.duration = $("#whitelist-duration").val()
            data.frequency = $("#whitelist-frequency").val()

            data.real_mobile = 0
            if($("input[type=checkbox]#whitelist-real-mobile").is(':checked')){
                data.real_mobile = 1
            }

            data.phoneuser_id = $("#phoneuser-id").val()

            requestData("POST", "html", '/whitelists/save/', {data : data},
                function(response){
                    updateDOM('#whitelists', response);
                    showMessageBox("Conferma", "Salvataggio effettuato con successo.", "green");
                    callback({success:true}); return;
                },
                function(error){
                  callback({success:false}); return;
                  showMessageBox("Errore", "Salvataggio non effettuata.", "alert-danger");
                }
            );
        }

        Whitelist.check(data.whitelist_id, postCheck);
    },

    changeStatus : function(id, newstatus){
        var data = {};
        data.whitelist_id = id;
        data.newstatus = newstatus;
        data.phoneuser_id = $("#phoneuser-id").val()

        requestData("POST", "html", '/whitelists/changestatus/', {data : data},
            function(response){
                if(response != "-1"){
                    updateDOM('#whitelists', response);
                    showMessageBox("Conferma", "Modifica stato effettuata con successo.", "green");
                }else{
                    showMessageBox("Errore", "Modifica stato non effettuata.", "alert-danger");
                }
            });

    },

    changeOrdinary : function(id, newstatus){
        var data = {};
        data.whitelist_id = id;
        data.newstatus = newstatus;
        data.phoneuser_id = $("#phoneuser-id").val()

        var postAlert = function(callback_return) {
            if (!callback_return.success) { return; }
            requestData("POST", "html", '/whitelists/changeordinary/', {data : data},
                function(response){
                    if(response != "-1"){
                        updateDOM('#whitelists', response);
                        showMessageBox("Conferma", "Modifica tipologia effettuata con successo", "green");
                    }else{
                        showMessageBox("Errore", "Modifica tipologia non effettuata.", "alert-danger");
                    }
                },
                function(error){
                    showMessageBox("Errore", "Modifica tipologia non effettuata.", "alert-danger");
                });
        }

        if(newstatus){
            Whitelist.showAlert(data, postAlert);
        }else{

            postAlert({success: true});
        }


    },

    remove : function(id){

        var msg = "Sei sicuro di voler eliminare il Numero Autorizzato?"

        if(confirm(msg)){
            var data = {};
            data.whitelist_id = id;
            data.phoneuser_id = $("#phoneuser-id").val()

        requestData("POST", "html", '/whitelists/remove/', {data : data},
            function(response){
                if(response != "-1"){
                    updateDOM('#whitelists', response);
                    showMessageBox("Conferma", "Numero autorizzato rimosso con successo.", "green");
                }else{
                    showMessageBox("Errore", "Rimozione numero autorizzato non riuscita.", "alert-danger");
                }
            });
        }

    },

    showAlert : function(data, callback) {
        // mostra quante straordinarie consentite nella settimana e nel mese
        // prosegue sulla successiva conferma
        requestData("POST", "json", '/whitelists/checkextra/', {data : data},
        function(response){
            console.log(typeof(response));
            if(response != "-1"){
                var msg = "Chiamate straordinarie gi\xE0 effettuate:\n";
                msg += '- nella settimana: '+ response.data.weekcalls+'\n';
                msg += '- nel mese: '+ response.data.monthcalls+'\n';
                msg += 'Confermare l\'autorizzazione strordinaria?';

                if(confirm(msg)){
                    callback({success:true}); return;
                }else{
                    callback({success:false}); return;
                }
            }else{
                alert('error');
                callback({success:false}); return;
            }
        });
    },

    switchCell : function() {
        var value = $('#whitelist-frequency').val();
        console.log(value);
        if(value == '0' || value == '1'){
            $('#whitelist-real-mobile-element').hide();
        }else{
            $('#whitelist-real-mobile-element').removeClass('hide');
        }
    }
}


var Credit = {

    new : function(phoneuser_id){

        requestData("POST", "html", '/credits/new/', {phoneuser_id : phoneuser_id}, function(response){
            var title = "Nuova Ricarica";
            var dict = {
                title : title,
                content : response,
                onSave : Credit.save,
                onRemove : null,
            }
            Modal.open(dict);

        });
    },

    check : function(){
        // async check
        // chiama il callback con {success:bool} al termine
        var ok = true;

        ok &= checkEmptyField("#credit-recharge");
        ok &= checkEmptyField("#credit-reason");

        return ok;
    },

    save : function(callback){
        // async post save
        // chiama il callback di save con {success:bool} al termine
        if (!Credit.check()) { callback({success:false}); return; }
        var data = {};
        data.phoneuser_id = $('#phoneuser-id').val();
        data.recharge = $("#credit-recharge").val()
        data.reason = $("#credit-reason").val()


        requestData("POST", "html", '/credits/save/', {data : data},
            function(response){
                updateDOM('#credits', response);
                showMessageBox("Conferma", "Inserimento ricarica effettuato con successo.", "green");
                callback({success:true}); return;
            },
            function(error){
              callback({success:false}); return;
              showMessageBox("Errore", "Inserimento ricarica non effettuato.", "alert-danger");
            }
        );
    },

}

