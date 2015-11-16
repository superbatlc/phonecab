var Pref = {

    check : function(isNew,callback){
        // async check
        // chiama il callback con {success:bool} al termine
        /*var ok = true;

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
        */
        callback({success:ok}); return;
    },

    save : function(callback){
        // async action
        // chiama il callback con {success:bool} al termine
        var data = {};
        data.first_name = $("#profile-first-name").val()
        data.last_name = $("#profile-last-name").val()
        data.username = $("#profile-username").val()
        data.password = $("#profile-password").val()

        requestDataDjango("POST", "html", '/prefs/save/', {data : data},
            function(response){
                updateDOM('.application', response); 
            },
            function(error){
              callback({success:false}); return;
            }
        );
        }

        // chiama postCheck al termine del check (passando {success:bool})
        Profile.check(isNew,save);
    },
}
