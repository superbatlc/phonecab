var Profile = {

    edit : function(id){
        requestData("POST", "html", '/profiles/edit/', {id : id}, function(response){
            var title = "Nuovo Utente";
            if (id) title = "Modifica Utente";
            var dict = {
                title : title,
                content : response,
                onSave : Profile.save,
                onRemove : null,
            }
            Modal.open(dict);

        });
    },

    check : function(isNew,callback){
        // async check
        // chiama il callback con {success:bool} al termine
        var ok = true;

        ok &= checkEmptyField("#profile-first-name");
        ok &= checkEmptyField("#profile-last-name");
        ok &= checkEmptyField("#profile-username");

        console.log("check");
        console.log(isNew,ok);

        if(isNew && ok){
          checkUniqueUsername("#profile-username", callback);
        } else {
          callback({success:ok}); return;
        }
    },

    save : function(callback){
        // async action
        // chiama il callback con {success:bool} al termine
        var data = {};
        var isNew = false;
        data.profile_id = $('#profile-id').val();
        console.log(data.profile_id);
        if (data.profile_id == "None" || data.profile_id == ''){
            data.profile_id = "0";
            isNew = true;
        }

        var postCheck = function(callback_return){
            // async post save
            // chiama il callback di save con {success:bool} al termine
            if (!callback_return.success) { callback({success:false}); return; }

            
            data.is_admin = 0
            if($("input[type=radio]#profile-type-ad").is(':checked')){
                data.is_admin = 1
            }

            data.first_name = $("#profile-first-name").val()
            data.last_name = $("#profile-last-name").val()
            data.username = $("#profile-username").val()
            data.password = $("#profile-password").val()

            data.priv_anagrafica = 1
            data.priv_whitelist = 0
            data.priv_credit = 0
            data.priv_cdr = 0
            data.priv_record = 0

            if(!data.is_admin){
                // Recuperiamo i privilegi
                if($("input[type=checkbox]#priv-ana-write").is(':checked')){
                    data.priv_anagrafica = 3
                }
                if($("input[type=checkbox]#priv-white-read").is(':checked')){
                    data.priv_whitelist = 1
                }
                if($("input[type=checkbox]#priv-white-write").is(':checked')){
                    data.priv_whitelist = 3
                }
                if($("input[type=checkbox]#priv-credit-read").is(':checked')){
                    data.priv_credit = 1
                }
                if($("input[type=checkbox]#priv-credit-write").is(':checked')){
                    data.priv_credit = 3
                }
                if($("input[type=checkbox]#priv-cdr-read").is(':checked')){
                    data.priv_cdr = 1
                }
                if($("input[type=checkbox]#priv-record-read").is(':checked')){
                    data.priv_record = 1
                }

            }

            //data.vipaccount = 0
            //if($("input[type=checkbox]#vipaccount").is(':checked')){
            //    data.vipaccount = 1
            //}
            //

            requestData("POST", "html", '/profiles/save/', {data : data},
                function(response){
                  if(isNew) {
                    updateDOM('#profiles', response); 
                  }
                  else updateDOM('#profiles', response);
                  callback({success:true}); return;
                },
                function(error){
                  callback({success:false}); return;
                }
            );
        }

        // chiama postCheck al termine del check (passando {success:bool})
        Profile.check(isNew,postCheck);
    },

    changeStatus : function(id, newstatus){
        var data = {};
        data.id = id;
        data.is_active = newstatus;

        requestData("POST", "html", '/profiles/changestatus/', {data : data},
            function(response){
                updateDOM('#profiles', response);
                showMessageBox("Conferma", "Utente aggiornato con successo.", "green");
            }, 
            function(error){
                showMessageBox("Errore", "Errore aggiornamento utente.", "alert-danger");
            
            });
    },

    changeType : function(show){
        console.log('changeType ', show);
        if(show){
            $('#privileges').fadeIn('slow');
            $('#privileges').removeClass("hide");
        } else{
            $('#privileges').fadeOut('slow');
        }
    },
}
