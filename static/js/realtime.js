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
                showMessageBox("Errore", "Errore " + (newMode? "attivazione linee" : "disattivazione linee") + ".", "alert-danger");
            }
        );
    },
}



var Ami = {


    test : function(){

        acall = {};
        acall.name = "Gino";
        acall.accountcode = "1425712457";
        acall.src = "201";
        acall.dst = "010283574";
        acall.startcall = "15:37";
        acall.duration = "37";
        var recording = true;
        var row = '<tr class="realtime-table-row"><td style="text-align:left">' + acall.name + '</td>';
        row += '<td style="text-align:center">' + acall.accountcode + '</td>';
        row += '<td style="text-align:center">' + acall.src + '</td>';
        row += '<td style="text-align:center">' + acall.dst + '</td>';
        row += '<td style="text-align:center">' + acall.startcall  + '</td>';
        row += '<td style="text-align:center">' + acall.duration + '</td>';

        var d = new Date()
        calldate = d.getUTCFullYear().toString()+twoDigitsNum(d.getUTCMonth()+1)+twoDigitsNum(d.getUTCDate());
        calltime = twoDigitsNum(d.getHours())+twoDigitsNum(d.getMinutes())+twoDigitsNum(d.getSeconds());
        filename = acall.accountcode + '_' + calldate + '_' + calltime + '_' + acall.dst;
        row += '<td style="text-align:center">';
        if(recording){
            row += '<button class="btn btn-warning disabled" disabled><i class="zmdi zmdi-rotate-right zmdi-hc-spin zmdi-hc-lg"></i> In registrazione</button>&nbsp;';                                                      
        }else{
            row += '<button class="btn btn-warning record-call" data-channel="' + acall.channel +'" data-file="' + filename + '">Registra</button>&nbsp;';
        }
        row += '<button class="btn btn-danger hangup-call" data-channel="' + acall.channel + '">Riaggancia</button>';
        row += '</td></tr>';
        //console.log(row);
        $('#realtime-table').append(row);
    } 
}


function twoDigitsNum(num){

        num = num.toString();
        if(num.length == 1){
                return "0" + num;
        }
        return num;
}