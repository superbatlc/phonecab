var Realtime = {

    active: null,

    init: function(actualMode) {
        // Set active as the server said
        Realtime._setActive(!!actualMode);

        // Login to AMI
        Ami.init();
        window.setInterval(Realtime._updateActiveLoop, Config.ami.loopInterval);
    },

    _updateActiveLoop() {
        console.log('LOOP ACTIVE');
        requestData("GET", "json", '/daynight', {}, function(response) {
            Realtime._setActive(!!response.daynight);
        });
    },

    _setActive: function(active) {
        if (Realtime.active === active) return;
        Realtime.active = active;
        $('#rt-modo-giorno').parent().removeClass('green red').addClass((active ? 'green' : 'red'));
        $('#rt-modo-' + (active ? 'notte' : 'giorno')).hide();
        $('#rt-modo-' + (active ? 'giorno' : 'notte')).show();
        Ami.manageLoops(Realtime.active);
    },

    toggleActive: function() {
        var newActive = !Realtime.active;
        requestData("POST", "html", '/daynight/', {
                active: newActive
            },
            function(response) {
                Realtime._setActive(newActive);
            },
            function(error) {
                console.log('ERRORE', error);
                showMessageBox("Errore", "Errore " + (newActive ? "attivazione linee" : "disattivazione linee") + ".", "alert-danger");
            }
        );
    },
}



var Ami = {

    // $('call-'+uniqueid+' .recording') // Selettore BOTTONE REGISTRAZIONE

    authenticated: false, // flag if logged in
    callsLoop: null, //interval calls update loop reference (to stop it)
    durationLoop: null, // interval duration loop reference (to stop it)
    active: false, // sync with Realtime.active thru manageLoops

    /**************************** ACTIONS *************************************/

    init: function() {
        Ami._login();
    },

    manageLoops: function(active) {
        Ami.active = active;

        clearInterval(Ami.durationLoop);
        clearInterval(Ami.callsLoop);
        if (active && Ami.authenticated) {
            Ami.durationLoop = window.setInterval(Ami._updateDurationLoop, 1000);
            Ami.callsLoop = window.setInterval(Ami._updateCallsLoop, Config.ami.loopInterval);
            Ami._updateCallsLoop();
        } else {
            Ami._noCalls();
        }
    },

    hangUpCall: function(channel) {
        if (!Ami._checkAuthenticated) return;
        requestData("GET", "xml", Config.ami.url + '?action=hangup&channel=' + channel, {},
            function(response) {
                showMessageBox("Conferma", 'Chiamata interrotta con successo.', "green");
            },
            function(error) {
                // console.log('ERRORE', error);
                showMessageBox("Errore", "Impossibile riagganciare la chiamata.", "alert-danger");
            }
        );
    },

    recordCall: function(channel, file) {
        if (!Ami._checkAuthenticated) return;

        var errorAction = function(error) {
            // console.log('ERRORE', error);
            showMessageBox("Errore", "Impossibile registrare la chiamata.", "alert-danger");
        }

        requestData("GET", "xml", Config.ami.url + '?action=monitor&channel=' + channel + '&file=' + file + '&mix=1', {}, function(response) {
            requestData("GET", "xml", Config.ami.url + '?action=setvar&channel=' + channel + '&variable=CALLFILENAME&value=' + file, {}, function(response) {
                requestData("GET", "xml", Config.ami.url + '?action=setvar&channel=' + channel + '&variable=RECORDING_ENABLED&value=1', {}, function(response) {

                    showMessageBox("Conferma", 'Registrazione avviata con successo', "green");

                }, errorAction);
            }, errorAction);
        }, errorAction);
    },

    linkCall: function(channel) {
        if (!Ami._checkAuthenticated) return;
        // TODO
        /*var channel = jQuery(this).attr("data-channel");
        var accountcode = jQuery('#realtime-accountcode').val();
        // intanto settiamo il data-file per la registrazione
        var calldate = d.getUTCFullYear().toString() + twoDigitsNum(d.getUTCMonth() + 1) + twoDigitsNum(d.getUTCDate());
        var calltime = twoDigitsNum(d.getHours()) + twoDigitsNum(d.getMinutes()) + twoDigitsNum(d.getSeconds());
        var data_file = accountcode + '_' + calldate + '_' + calltime + '_' + dst;
        jQuery('.record-call').attr('data-file', data_file);

        // poi inviamo ad asterisk la variabile di canale per l'accountcode

        requestData("GET", "xml", Config.ami.url + '?action=hangup&channel=' + channel, {},
            function(response) {
                showMessageBox("Conferma", 'Chiamata interrotta con successo.', "green");
            },
            function(error) {
                // console.log('ERRORE', error);
                showMessageBox("Errore", "Impossibile riagganciare la chiamata.", "alert-danger");
            }
        );
        */
    },

    /****************************** UTILS *************************************/

    _checkAuthenticated: function() {
        if (!Ami.authenticated) {
            showMessageBox("Errore", "Autenticazione AMI fallita.<br><br><strong>Ricaricare la pagina per riprovare.</strong>", "alert-danger");
            return false;
        }
        return true;
    },


    // _getCallInfo: function(channel) {
    //
    //     if (Ami.channel.channel) {
    //         return Ami.channel.channel;
    //     } else {
    //         // richiesta al server da implementare
    //     }
    //
    //
    // },

    /****************************** LOGIN *************************************/


    _login: function() {
        requestData("GET", "xml", Config.ami.url + '?action=login&username=' + Config.ami.username + '&secret=' + Config.ami.secret, {},
            function(response) {
                Ami.authenticated = true;
                Ami.manageLoops(Ami.active); // start the loops
            },
            function(error) {
                // console.log('ERRORE', error);
                showMessageBox("Errore", "Impossibile effettuare login al sitema AMI.<br><br><strong>Ricaricare la pagina per riprovare.</strong>", "alert-danger");
                Ami.authenticated = false;
            }
        );
    },

    /****************************** LOOPS *************************************/

    _updateDurationLoop: function() {
        console.log('LOOP DURATION');
        $('#realtime-table .duration').each(function(i) {
            var time = $(this).html().split(':');
            if (time.length!=3) { return; }
            time[2] = parseInt(time[2])+1;
            if (time[2]==60) { time[2] = 0; time[1] = parseInt(time[1])+1; }
            if (time[1]==60) { time[1] = 0; time[0] = parseInt(time[0])+1; }
            $(this).html(time[0]+':'+("0"+time[1]).slice(-2)+':'+("0"+time[2]).slice(-2));
        })
    },

    _updateCallsLoop: function() {
        console.log('LOOP CALLS');
        if (!Ami._checkAuthenticated) return;

        requestData("GET", "xml", Config.ami.url + '?action=coreshowchannels', {}, function(response) {

            var channels = [];
            var uniqueid_relation = [];
            var calls = [];

            jQuery.each(jQuery.xml2json(response).response, function(idx, response) {
                if (response.generic.event == 'CoreShowChannelsComplete' &&
                    response.generic.eventlist == "Complete" &&
                    response.generic.listitems == "0") {
                    // nessuna chiamata
                    Ami._noCalls();
                }
                if (response.generic.event == 'CoreShowChannel') channels.push(response);
            }); // END each channels.response

            // No calls, no reason to continue
            if (channels.length == 0) return;

            channels.forEach(function(response) {

                var channel = response.generic.channel;
                var channel_uniqueid = response.generic.uniqueid;
                var channel_bridgeduniqueid = response.generic.bridgeduniqueid;

                //console.log("channel_uniqueid: " + channel_uniqueid + " - channel_bridgeduniqueid: " + channel_bridgeduniqueid);

                if (calls.length > 0 && (uniqueid_relation.indexOf(channel_uniqueid) >= 0 || uniqueid_relation.indexOf(channel_bridgeduniqueid) >= 0)) {
                    // don't add call if there is already the uniqueid
                    // add it anyway if it is the first one
                    return;
                }
                calls.push({
                    channel: channel,
                    src: '',
                    dst: '',
                    accountcode: '',
                    name: '',
                    duration: '',
                    uniqueid: channel_uniqueid,
                    bridgeduniqueid: channel_bridgeduniqueid,
                });
                uniqueid_relation.push(channel_uniqueid);
            }); // END each channel

            Ami._clearCalls();

            calls.forEach(function(acall) {
                var incoming = 0;
                var call_exists = false;
                channels.forEach(function(response) {
                    if (acall.uniqueid == response.generic.uniqueid || acall.uniqueid == response.generic.bridgeduniqueid) {
                        call_exists = true;
                        var d = new Date(response.generic.uniqueid * 1000);
                        var startcall = d.toLocaleTimeString();
                        acall.startcall = startcall;
                        if (response.generic.context == 'from-cabs') {
                            acall.accountcode = response.generic.accountcode;
                            if (!incoming) {
                                acall.src = response.generic.calleridnum;
                            }
                            incoming = 0;
                            acall.duration = response.generic.duration;
                        }
                        if (response.generic.context == 'outgoing-operator-dial-number') {
                            acall.dst = response.generic.calleridnum;
                            incoming = 0;
                        }
                        if (response.generic.context == 'incoming-operator-dial-number') {
                            incoming = 1;
                            acall.src = response.generic.calleridnum;
                            acall.dst = response.generic.exten;
                        }
                        if (response.generic.context == 'cabs-dial-number') {
                            acall.accountcode = response.generic.accountcode;
                            acall.src = response.generic.calleridnum;
                            acall.dst = response.generic.exten;
                            acall.duration = response.generic.duration;
                        }
                        if (response.generic.context == 'from-trunk') {
                            acall.src = response.generic.connectedlinenum;
                            acall.dst = response.generic.calleridnum;
                        }
                    }
                });

                if (!call_exists) {
                    // rimuovi la chiamata
                    calls.pop(acall);
                } else {
                    // costruiamo la tabella se abbiamo tutti i dati
                    if (acall.src != '' && acall.dst != '' && acall.accountcode != '') {

                        requestData("GET", "json", '/phoneusers/name/' + acall.accountcode, {}, function(response) {
                                acall.name = response.data.name;
                                Ami._addCall(acall, response.data.recording);
                            },
                            function(error) {
                                console.log('Dati di link fra call<->db non recuperati');
                            });
                    }
                };
            }); // END call each
        }, function(error) {
            // console.log('ERRORE', error);
            showMessageBox("Errore", "Impossibile aggiornare la lista chiamate.", "alert-danger");
        }); // main request mxml
    },


    /*********************** DOM MANIPULATION *********************************/

    _clearCalls: function() {
        $('#realtime-table tbody').empty();
    },

    _noCalls: function() {
        Ami._clearCalls();
        $('#realtime-table tbody').append('<tr><td colspan="7" align="center"><h3>Non ci sono chiamate in corso</h3></td></tr>');
    },

    _addCall: function(acall, recording) {

        // var acall = {
        //     channel: 'canale',
        //     src: 'sorgente',
        //     dst: 'destinazione',
        //     accountcode: 'codice',
        //     name: 'nome',
        //     duration: '20',
        //     uniqueid: 'univoco',
        //     bridgeduniqueid: 'univocobridge',
        // }

        var d = new Date()
        calldate = d.getUTCFullYear().toString() + twoDigitsNum(d.getUTCMonth() + 1) + twoDigitsNum(d.getUTCDate());
        calltime = twoDigitsNum(d.getHours()) + twoDigitsNum(d.getMinutes()) + twoDigitsNum(d.getSeconds());
        filename = acall.accountcode + '_' + calldate + '_' + calltime + '_' + acall.dst;

        var actions = '';
        if (recording) {
            actions += '<button class="recording btn btn-warning" disabled><i class="zmdi zmdi-rotate-right zmdi-hc-spin zmdi-hc-lg"></i> In registrazione</button>';
        } else {
            actions += '<button class="recording btn btn-warning record-call" onclick="Ami.recordCall(\'' + acall.channel + '\',\'' + filename + '\')">Registra</button>';
        }
        actions += '&nbsp;<button class="hangup btn btn-danger hangup-call" onclick="Ami.hangUpCall(\'' + acall.channel + '\')">Riaggancia</button>';

        $('#realtime-table tbody').append(
            $(document.createElement('tr'))
            .addClass("realtime-table-row")
            .attr('id', 'call-' + acall.uniqueid)
            .append([
                $(document.createElement('td')) // Anagrafica
                .addClass('text-center')
                .html(acall.name),

                $(document.createElement('td')) // Codice
                .addClass('text-center')
                .html(acall.accountcode),

                $(document.createElement('td')) // Sorgente
                .addClass('text-center')
                .html(acall.src),

                $(document.createElement('td')) // Destinazione
                .addClass('text-center')
                .html(acall.dst),

                $(document.createElement('td')) // Ora inizio
                .addClass('text-center')
                .html(acall.startcall),

                $(document.createElement('td')) // Durata
                .addClass('text-center duration')
                .html(acall.duration),

                // $(document.createElement('td')) // Credito residuo
                // .addClass('text-center')
                // .html(''),

                $(document.createElement('td')) // Azioni
                .addClass('text-center')
                .html(actions),
            ]));
    }


}


function twoDigitsNum(num) {
    num = num.toString();
    if (num.length == 1) {
        return "0" + num;
    }
    return num;
}
