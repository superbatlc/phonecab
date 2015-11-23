var Realtime = {

    active: false,

    init: function(actualMode) {
        // Set active as the server said
        Realtime._setActive(!!actualMode);

        // Login to AMI
        Ami.init();
    },

    _setActive: function(active) {
        Realtime.active = active;
        $('#rt-modo-giorno').parent().removeClass('green red').addClass((active ? 'green' : 'red'));
        $('#rt-modo-' + (active ? 'notte' : 'giorno')).hide();
        $('#rt-modo-' + (active ? 'giorno' : 'notte')).show();
        console.log('3');
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

    authenticated: false,
    callsLoop: null, //interval loop reference (to stop it)
    durationLoop: null,
    active: false,

    init: function() {
        Ami.login();
    },

    login: function() {
        requestData("GET", "xml", Config.ami.url + 'asterisk/mxml?action=login&username=' + Config.ami.username + '&secret=' + Config.ami.secret, {},
            function(response) {
                console.log('Login efettuato');
                Ami.authenticated = true;
                Ami.manageLoops(Ami.active); // start the loops
            },
            function(error) {
                console.log('ERRORE', error);
                showMessageBox("Errore", "Impossibile effettuare login al sitema AMI.", "alert-danger");
                Ami.authenticated = false;
                Ami.authenticated = true;
                Ami.manageLoops(Ami.active); // start the loops
            }
        );
    },

    manageLoops: function(active) {
        console.log(Ami.authenticated);
        Ami.active = active;

        clearInterval(Ami.durationLoop);
        clearInterval(Ami.callsLoop);
        if (active && Ami.authenticated) {
            Ami.durationLoop = window.setInterval(Ami._updateDurationLoop, 1000);
            Ami.callsLoop = window.setInterval(Ami._updateCallsLoop, Config.ami.loopInterval);
            Ami._updateCallsLoop();
        } else {
            Ami._clearCalls();
        }
    },

    hangUpCall: function(channel) {
        if (!Ami._checkAuthenticated) return;
        requestData("GET", "xml", Config.ami.url + '/asterisk/mxml?action=hangup&channel=' + channel, {},
            function(response) {
                console.log('Chiamata sul canale ' + channel + ' interrotta con successo.');
            },
            function(error) {
                console.log('ERRORE', error);
                showMessageBox("Errore", "Impossibile riagganciare la chiamata.", "alert-danger");
            }
        );
    },

    recordCall: function(channel, file) {
        if (!Ami._checkAuthenticated) return;

        var errorAction = function(error) {
            console.log('ERRORE', error);
            showMessageBox("Errore", "Impossibile registrare la chiamata.", "alert-danger");
        }

        requestData("GET", "xml", Config.ami.url + 'asterisk/mxml?action=monitor&channel=' + channel + '&file=' + file + '&mix=1', {}, function(response) {
            requestData("GET", "xml", Config.ami.url + 'asterisk/mxml?action=setvar&channel=' + channel + '&variable=CALLFILENAME&value=' + file, {}, function(response) {
                requestData("GET", "xml", Config.ami.url + 'asterisk/mxml?action=setvar&channel=' + channel + '&variable=RECORDING_ENABLED&value=1', {}, function(response) {

                    console.log('Chiamata sul canale ' + channel + ' interrotta con successo.');

                }, errorAction);
            }, errorAction);
        }, errorAction);
    },

    linkCall: function() {
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

        jQuery.ajax({
               type: 'GET',
               url: '/asterisk/mxml?action=login&username=youramiuser&secret=youramipw',
               async: true,
               dataType: 'xml',
               success: function(response){
                 jQuery.ajax({
                     type: 'GET',
                     url: '/asterisk/mxml?action=hangup&channel='+channel,
                     async: true,
                     dataType: 'xml',
                     success: function(response){
                       alert('Chiamata interrotta con successo');
                     },
                     error: function(jqXHR, textStatus, errorThrown){
                          //alert('Errore nella trasmissione del dato');
                     },
                 })
               },
               error: function(jqXHR, textStatus, errorThrown){
                    //alert('Errore nella trasmissione del dato')
               },
        })
        */
    },

    _checkAuthenticated: function() {
        if (!Ami.authenticated) {
            showMessageBox("Errore", "Autenticazione AMI fallita. Ricaricare la pagina per riprovare.", "alert-danger");
            return false;
        }
        return true;
    },

    _updateDurationLoop: function() {
        // console.log('LOOP DURATION');
        $('#realtime-table .duration').each(function(i) {
            $(this).html(parseInt($(this).html()) + 1);
        })
    },

    _updateCallsLoop: function() {
        // console.log('LOOP CALLS');
        var errorAction = function(error) {
            console.log('ERRORE', error);
            showMessageBox("Errore", "Impossibile aggiornare la lista chiamate.", "alert-danger");
        }

        requestData("GET", "xml", Config.ami.url + 'asterisk/mxml?action=coreshowchannels', {}, function(response) {

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
                            acall.dst = response.generic.extension;
                        }
                        if (response.generic.context == 'cabs-dial-number') {
                            acall.accountcode = response.generic.accountcode;
                            acall.src = response.generic.calleridnum;
                            acall.dst = response.generic.extension;
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
                            function(error) {});
                    }
                };
            }); // END call each
        }, errorAction); // main request mxml
    },


    _getCallInfo: function(channel) {

        if (Ami.channel.channel) {
            return Ami.channel.channel;
        } else {
            // richiesta al server da implementare
        }


    },

    _clearCalls: function() {
        $('#realtime-table tbody').empty();
    },

    _noCalls: function() {
        Ami._clearCalls();
        $('#realtime-table tbody').append('<tr><td colspan="7" align="center"><h3>Non ci sono chiamate in corso</h3></td></tr>');
    },

    _addCall: function(acall, recording) {

        // var acall = {
        //     channel: 'test',
        //     name: 'nome',
        //     accountcode: 'account',
        //     src: 'sorgente',
        //     dst: 'destinazione',
        //     startcall: '12:30:25',
        //     duration: 10
        // }

        var d = new Date()
        calldate = d.getUTCFullYear().toString() + twoDigitsNum(d.getUTCMonth() + 1) + twoDigitsNum(d.getUTCDate());
        calltime = twoDigitsNum(d.getHours()) + twoDigitsNum(d.getMinutes()) + twoDigitsNum(d.getSeconds());
        filename = acall.accountcode + '_' + calldate + '_' + calltime + '_' + acall.dst;

        var actions = '';
        if (recording) actions += '<button class="recording btn btn-warning" disabled><i class="zmdi zmdi-rotate-right zmdi-hc-spin zmdi-hc-lg"></i> In registrazione</button>&nbsp;';
        else actions += '<button class="recording btn btn-warning record-call" onclick="Ami.recordCall(\'' + acall.channel + '\',\'' + filename + '\')">Registra</button>&nbsp;';
        actions += '<button class="hangup btn btn-danger hangup-call" onclick="Ami.hangUpCall(\'' + acall.channel + '\')">Riaggancia</button>';

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
