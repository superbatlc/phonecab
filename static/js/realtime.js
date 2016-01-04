var Realtime = {

    active: null,

    init: function(nightMode) {
        // Set active as the server said
        Realtime._setActive(!nightMode);

        // Login to AMI
        Ami.init();
        window.setInterval(Realtime._updateActiveLoop, Config.ami.loopInterval);
    },

    _updateActiveLoop() {
        //console.log('LOOP ACTIVE');
        requestData("GET", "json", '/nightmode', {}, function(response) {
            Realtime._setActive(!response.nightmode);
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
        requestData("POST", "html", '/nightmode/' + (newActive ? 0 : 1), {},
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
            Ami._noUICalls();
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
        //console.log('LOOP DURATION');
        $('#realtime-table .call-duration').each(function(i) {
            var time = $(this).html().split(':');
            if (time.length != 3) {
                return;
            }
            time[2] = parseInt(time[2]) + 1;
            if (time[2] == 60) {
                time[2] = 0;
                time[1] = parseInt(time[1]) + 1;
            }
            if (time[1] == 60) {
                time[1] = 0;
                time[0] = parseInt(time[0]) + 1;
            }
            $(this).html(time[0] + ':' + ("0" + time[1]).slice(-2) + ':' + ("0" + time[2]).slice(-2));
        })
    },

    _updateCallsLoop: function() {
        //console.log('LOOP CALLS');
        if (!Ami._checkAuthenticated) return;

        requestData("GET", "xml", Config.ami.url + '?action=coreshowchannels', {}, function(response) {

            var channels = []; // valid channels
            var bridged = {}; // grouped channels per bridgeid
            var calls = []; // final selection to be considered a call

            // GET CHANNELS FROM RESPONSE
            jQuery.each(jQuery.xml2json(response).response, function(idx, channel) {
                // channel.generic = {
                //     eventlist: "start",
                //     message: "Channels will follow",
                //     response: "Success",
                // }

                // channel.generic = {
                //     event: "CoreShowChannelsComplete",
                //     eventlist: "Complete",
                //     listitems: "2" // number of items (excluded START and SHOWCHANNELCOMPLETE)
                // }
                if (channel.generic.event == 'CoreShowChannel') channels.push(channel.generic);
            }); // END each channels.response

            // No calls, no reason to continue
            if (channels.length == 0) {
                Ami._noUICalls();
                return;
            }

            // Divide channels by bridges (and create calls objects, 1 per bridge)
            channels.forEach(function(channel) {
                var channel_name = channel.channel;
                var channel_bridgeid = channel.bridgeid;

                // if (!channel_bridgeid) return; // ignore the ones without bridgeid

                if (bridged.hasOwnProperty(channel_bridgeid)) {
                    bridged[channel_bridgeid].push(channel);
                } else {
                    bridged[channel_bridgeid] = [channel];
                    calls.push({
                        channel: channel_name,
                        src: '',
                        dst: '',
                        accountcode: '',
                        name: '',
                        duration: '',
                        bridgeid: channel_bridgeid,
                        recording: false,
                    });
                }

            }); // END each channel

            // Cycle calls (bridges) to get data
            calls.forEach(function(acall) {
                var call_exists = false;
                var channel = {}; //temproary value
                var current_channels = bridged[acall.bridgeid];
                var current_contexts = utils.getValues(current_channels, 'context');

                if (current_contexts.indexOf('cabs-dial-number') >= 0 && current_contexts.indexOf('from-trunk') >= 0) {

                    //DETENUTO [ cabs-dial-number + from-trunk]
                    channel = utils.getItem(current_channels, 'context', 'from-trunk');
                    call_exists = true;
                    acall.accountcode = channel.accountcode;
                    acall.duration = channel.duration;
                    acall.uniqueid = channel.uniqueid;
                    acall.startcall = (new Date(channel.uniqueid * 1000)).toLocaleTimeString();
                    acall.src = channel.connectedlinenum;
                    acall.dst = channel.calleridnum;

                } else if (current_contexts.indexOf('from-cabs') >= 0 && current_contexts.indexOf('from-trunk') >= 0) {

                    channel = utils.getItem(current_channels, 'context', 'from-cabs');
                    var trunk = utils.getItem(current_channels, 'context', 'from-trunk');
                    call_exists = true;
                    acall.accountcode = channel.accountcode;
                    acall.duration = channel.duration;
                    acall.uniqueid = channel.uniqueid;
                    acall.startcall = (new Date(channel.uniqueid * 1000)).toLocaleTimeString();
                    if (!trunk.exten) {
                        // PER CONTO [ from-cabs + from-trunk ]
                        acall.src = channel.calleridnum;
                        acall.dst = channel.connectedlinenum;
                    } else {
                        // ENTRANTE [from-cabs + from-trunk + from-trunk.exten valorizzato]
                        acall.src = '';
                        acall.dst = channel.calleridnum;
                    }

                }

                if (!call_exists) {
                    // rimuovi la chiamata
                    calls.pop(acall);
                }
            });

            Ami._cleanUICalls(calls);

            calls.forEach(function(acall) {
                // recuperiamo dati aggiuntivi sulla chiamata
                if (acall.accountcode != '') {

                    var data = {};
                    data.pincode = acall.accountcode;
                    data.dst = acall.dst;
                    data.src = acall.src;

                    requestData("POST", "json", '/phoneusers/realtime/info/', {
                            data: data
                        }, function(response) {
                            acall.name = response.data.name;
                            acall.dst = response.data.dst;
                            acall.src = response.data.src_name;
                            acall.recording = response.data.recording;
                            Ami._addUICall(acall);
                        },
                        function(error) {
                            console.log('Dati di link fra call<->db non recuperati', error);
                            Ami._addUICall(acall);
                        });
                }
            }); // END call each



            console.log('----------');
            console.log('channels:', channels);
            console.log('bridged:', bridged);
            console.log('calls:', calls);


        }, function(error) {
            // console.log('ERRORE', error);
            showMessageBox("Errore", "Impossibile aggiornare la lista chiamate.", "alert-danger");
        }); // main request mxml
    },


    /*********************** DOM MANIPULATION *********************************/

    _noUICalls: function() {
        $('#realtime-table tbody').empty();
        $('#realtime-table tbody').append('<tr class="empty"><td colspan="7" align="center"><h3>Non ci sono chiamate in corso</h3></td></tr>');
    },

    _cleanUICalls: function(calls) {
        // METHOD1 (refresh everytime)
        //$('#realtime-table tbody').empty();

        // METHOD2
        if (calls.length == 0) {
            Ami._noUICalls();
        } else {
            // remove finished calls
            $('#realtime-table tr.empty').remove();
            var ids = utils.getValues(calls, 'uniqueid');
            $('#realtime-table realtime-table-row').each(function() {
                console.log('remove ', $(this));
                if (ids.indexOf(String($(this).attr('data-uniqueid'))) < 0) $(this).remove();
            });
        }
    },

    _addUICall: function(acall) {

        // var acall = {
        //     channel: 'canale',
        //     src: 'sorgente',
        //     dst: 'destinazione',
        //     accountcode: 'codice',
        //     name: 'nome',
        //     duration: '20',
        //     uniqueid: 'univoco',
        //     linkedid: 'univocobridge',
        //     recording: 'hidden|progress|show',
        // }

        var d = new Date()
        calldate = d.getUTCFullYear().toString() + twoDigitsNum(d.getUTCMonth() + 1) + twoDigitsNum(d.getUTCDate());
        calltime = twoDigitsNum(d.getHours()) + twoDigitsNum(d.getMinutes()) + twoDigitsNum(d.getSeconds());
        filename = acall.accountcode + '_' + calldate + '_' + calltime + '_' + acall.dst;

        var actions = '';
        switch (acall.recording) {
            case 'progress':
                actions += '<button class="recording btn btn-warning" disabled><i class="zmdi zmdi-rotate-right zmdi-hc-spin zmdi-hc-lg"></i> In registrazione</button>';
                break;
            case 'show':
                actions += '<button class="recording btn btn-warning record-call" onclick="Ami.recordCall(\'' + acall.channel + '\',\'' + filename + '\')">Registra</button>'
                break;
            default:
                break;
        }
        actions += '&nbsp;<button class="hangup btn btn-danger hangup-call" onclick="Ami.hangUpCall(\'' + acall.channel + '\')">Riaggancia</button>';

        var element = $("[data-uniqueid='" + acall.uniqueid + "']");
        console.log(element);
        if (element.length) {
            console.log('edit ', element);

            element.find('call-name').html(acall.name);
            element.find('call-accountcode').html(acall.accountcode);
            element.find('call-src').html(acall.src);
            element.find('call-dst').html(acall.dst);
            element.find('call-startcall').html(acall.startcall);
            element.find('call-duration').html(acall.duration);
            element.find('call-actions').html(acall.actions);

        } else {

            console.log('add element');


            $('#realtime-table tbody').append(
                $(document.createElement('tr'))
                .addClass("realtime-table-row")
                .attr('data-uniqueid', acall.uniqueid)
                .append([
                    $(document.createElement('td')) // Anagrafica
                    .addClass('call-name text-left')
                    .html(acall.name),

                    $(document.createElement('td')) // Codice
                    .addClass('call-accountcode text-center')
                    .html(acall.accountcode),

                    $(document.createElement('td')) // Sorgente
                    .addClass('call-src text-center')
                    .html(acall.src),

                    $(document.createElement('td')) // Destinazione
                    .addClass('call-dst text-center')
                    .html(acall.dst),

                    $(document.createElement('td')) // Ora inizio
                    .addClass('call-startcall text-center')
                    .html(acall.startcall),

                    $(document.createElement('td')) // Durata
                    .addClass('call-duration text-center')
                    .html(acall.duration),

                    // $(document.createElement('td')) // Credito residuo
                    // .addClass('text-center')
                    // .html(''),

                    $(document.createElement('td')) // Azioni
                    .addClass('call-actions text-center')
                    .html(actions),
                ]));

        } // IF exists
    }


}


function twoDigitsNum(num) {
    num = num.toString();
    if (num.length == 1) {
        return "0" + num;
    }
    return num;
}
