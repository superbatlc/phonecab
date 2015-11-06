var Phoneuser = {

        edit : function(id){
            requestData("POST", "html", '/phoneusers/edit/', {id : id}, function(response){
                var title = "Nuova Anagrafica";
                if (id) title = "Modifica Anagrafica";
                var dict = {
                    title : title,
                    content : response,
                    onSave : Phoneuser.save,
                    onRemove : null,
                }
                Modal.open(dict);

            });
        },

        check : function(isNew){
            var ok = true;

            ok &= checkEmptyField("#first-name");
            ok &= checkEmptyField("#last-name");
            ok &= checkEmptyField("#serial-no");
            if(isNew){
                ok &= checkUniquePincode("#pincode");
            }

            return ok
        },

        save : function(){
            var data = {};
            var isNew = false;
            data.phoneuser_id = $('#phoneuser-id-modal').val();
            if (data.phoneuser_id == "None" || data.phoneuser_id == ''){
                data.phoneuser_id = "0";
                isNew = true;
            }

            if(!Phoneuser.check(isNew)) return false;

            var postCheck = function(data){
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
                    phoneuser.recording_enabled = 1
                }

                //data.vipaccount = 0
                //if($("input[type=checkbox]#vipaccount").is(':checked')){
                //    data.vipaccount = 1
                //}       
                
                requestDataDjango("POST", "html", '/phoneusers/save/', {data : data}, function(response){
                    if(isNew) alert('update list');
                    else Phoneuser.updateDOM('#phoneuser', response));
                });
            }

            return true;
        },

        enable : function(id){

        },

        archive : function(id){

        }, 
        /*
        checkPincode : function(pincode){
            requestData("POST", "html", '/phoneusers/check/', {pincode : pincode}, function(response){Phoneuser.updateDOM('#ballyhoos-active', response)});

        },
        */ 

        updateDOM : function(selector, content) {
            $(selector).html(content);
        },


}