/**
 * Funzione per attivazione modo Giorno/Notte 
 */
jQuery('body').on('click','.daynight', function(e){
	// GIORNO vs NOTTE
	var next_mode = jQuery(this).attr("data-next-mode");
	
	jQuery.ajax({
	       type: 'GET',
	       url: '/daynight/'+next_mode,
	       async: true,
	       success: function(response){
				location.reload()
	       },
	       error: function(jqXHR, textStatus, errorThrown){
	            //alert('Errore nella trasmissione del dato');
	       },
	   })
	
})

/**
 * Funzione hang-up chiamata
 */
jQuery('body').on('click','.hangup-call', function(e){
	var channel = jQuery(this).attr("data-channel");
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
})

/**
 * Funzione Record chiamata
 */
jQuery('body').on('click','.record-call', function(e){
	var channel = jQuery(this).attr("data-channel");
	var file = jQuery(this).attr("data-file");
	jQuery.ajax({
	       type: 'GET',
	       url: '/asterisk/mxml?action=login&username=youramiuser&secret=youramipw',
	       async: true,
	       dataType: 'xml',
	       success: function(response){
	    	   // registrazione
	    	   jQuery.ajax({
	    	       type: 'GET',
	    	       url: '/asterisk/mxml/?action=monitor&channel='+channel+'&file='+file+'&mix=1',
	    	       async: true,
	    	       dataType: 'xml',
	    	       success: function(response){
	    	    	   // settiamo variabile CALLFILENAME
	    	    	   jQuery.ajax({
	    	    	       type: 'GET',
	    	    	       url: '/asterisk/mxml?action=setvar&channel='+channel+'&variable=CALLFILENAME&value='+file,
	    	    	       async: true,
	    	    	       dataType: 'xml',
	    	    	       success: function(response){
	    	    	    	// settiamo variabile RECORDING_ENABLED
	    	    	    	   jQuery.ajax({
	    	    	    	       type: 'GET',
	    	    	    	       url: '/asterisk/mxml?action=setvar&channel='+channel+'&variable=RECORDING_ENABLED&value=1',
	    	    	    	       async: true,
	    	    	    	       dataType: 'xml',
	    	    	    	       success: function(response){
	    	    	    	    	   alert('Inizio registrazione con successo');
	    	    	    	       },
	    	    	    	       error: function(jqXHR, textStatus, errorThrown){
	    	    	    	            //alert('Errore nella trasmissione del dato')
	    	    	    	       },
	    	    	    	   })
	    	    	       },
	    	    	       error: function(jqXHR, textStatus, errorThrown){
	    	    	            //alert('Errore nella trasmissione del dato')
	    	    	       },
	    	    	   })
	    	       },
	    	       error: function(jqXHR, textStatus, errorThrown){
	    	            //alert('Errore nella trasmissione del dato')
	    	       },
	    	   })
	       },
	       error: function(jqXHR, textStatus, errorThrown){
	            //alert('Errore nella trasmissione del dato')
	       },
	})
})

/**
 * Funzione associa accountcode
 */
jQuery('body').on('click','.link-call', function(e){
	var channel = jQuery(this).attr("data-channel");
	var accountcode = jQuery('#realtime-accountcode').val();
	// intanto settiamo il data-file per la registrazione
	var calldate = d.getUTCFullYear().toString()+twoDigitsNum(d.getUTCMonth()+1)+twoDigitsNum(d.getUTCDate());
    var calltime = twoDigitsNum(d.getHours())+twoDigitsNum(d.getMinutes())+twoDigitsNum(d.getSeconds());
    var data_file = accountcode + '_' + calldate + '_' + calltime + '_' + dst; 
	jQuery('.record-call').attr('data-file', data_file);
	
	// poi inviamo ad asterisk la variabile di canale per l'accountcode
	/*
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
})





/**
 * Funzione per aggiungere lo zero ai numeri a una cifra
 */
function twoDigitsNum(num){

        num = num.toString();
        if(num.length == 1){
                return "0" + num;
        }
        return num;
}




/**
 * Funzione per il recupero delle info sulle chiamate in corso
 */
function update_realtime(){
        //var channel;
        //var accountcode = '-';
        //var src = 'non disponibile';
        //var dst = 'non disponibile';
		//var calldate;
        //var duration = '00:00:00';
        //var managed = true;
        var filename = '';
		
		function Call() {
			this.channel = '';
			this.src = '';
			this.dst = '';
			this.accountcode = '';
			this.name = ''
			this.duration = '';
			this.uniqueid = '';
			this.bridgeduniqueid = '';
			/*
			check : function(){
				if(this.src != '' && this.dst != '' && this.accountcode != ''){
					return true;
				}
				return false;
			}
			*/
		}

		
		var calls = Array();

        jQuery.ajax({
			type: 'GET',
			url: '/asterisk/mxml?action=login&username=youramiuser&secret=youramipw',
			async: true,
			dataType: 'xml',
			success: function(response){
						// registrazione
						jQuery.ajax({
							type: 'GET',
							url: '/asterisk/mxml?action=coreshowchannels',
							async: true,
							dataType: 'xml',
							success: function(response){
								var xml_channels =  jQuery.xml2json(response);
								var channels = Array();					
								
								jQuery('tr.realtime-table-row').remove();							
								jQuery.each(xml_channels.response, function(idx, response){
									if(response.generic.event == 'CoreShowChannelsComplete' && response.generic.eventlist == "Complete" && response.generic.listitems == "0"){
										// ripuliamo la tabella
										jQuery('#realtime-table').append('<tr class="realtime-table-row"><td colspan="7" align="center"><br/><br/><h3>Non ci sono chiamate in corso</h3></td></tr>');
										return;
									}
									if(response.generic.event == 'CoreShowChannel'){
										channels.push(response);
									}
								});

								var uniqueid_relation = Array();						
								
								channels.forEach(function(response){
									
									var channel = response.generic.channel;
									var channel_uniqueid = response.generic.uniqueid;
									var channel_bridgeduniqueid = response.generic.bridgeduniqueid;
									
									//console.log("channel_uniqueid: " + channel_uniqueid + " - channel_bridgeduniqueid: " + channel_bridgeduniqueid);
									
									
									if(calls.length == 0){
										var c = new Call();
										c.uniqueid = response.generic.uniqueid;
										c.bridgeduniqueid = response.generic.bridgeduniqueid;
										c.channel = response.generic.channel;
										calls.push(c);
										//console.log("Zero chiamate. Aggiungo: " + c.uniqueid + " - " + c.bridgeduniqueid);
										uniqueid_relation.push(response.generic.uniqueid);
										return ;
									}
									
									//console.log("cerco uniqueid: " + channel_uniqueid + " =>" + uniqueid_relation.indexOf(channel_uniqueid));
									//console.log("cerco bridgeduniqueid: " + channel_bridgeduniqueid + " =>" + uniqueid_relation.indexOf(channel_bridgeduniqueid));
									
									
									if(uniqueid_relation.indexOf(channel_uniqueid) < 0 && uniqueid_relation.indexOf(channel_bridgeduniqueid) < 0 ){
										var c = new Call();
										c.uniqueid = response.generic.uniqueid;
										c.bridgeduniqueid = response.generic.bridgeduniqueid;
										c.channel = response.generic.channel;
										calls.push(c);
										console.log("Nessun legame. Aggiungo: " + c.uniqueid + " - " + c.bridgeduniqueid);
										uniqueid_relation.push(response.generic.uniqueid);

									}
								});
								
								//console.log("Chiamate: " + calls);
								calls.forEach(function(acall){
									var incoming = 0;
									var call_exists = false;
									channels.forEach(function(response){
										if(acall.uniqueid == response.generic.uniqueid || acall.uniqueid == response.generic.bridgeduniqueid){
											call_exists = true;
											var d = new Date(response.generic.uniqueid * 1000);
											var startcall = d.toLocaleTimeString();
											acall.startcall = startcall;
											if(response.generic.context == 'from-cabs'){
												acall.accountcode = response.generic.accountcode;
												if(!incoming){
													acall.src = response.generic.calleridnum;
												}
												incoming = 0;
												acall.duration = response.generic.duration;
											}
											if(response.generic.context == 'outgoing-operator-dial-number'){
												acall.dst = response.generic.calleridnum;
												//console.log('outgoing-operator-dial-number: dst = ' + dst);
												incoming = 0;
											}
											
											if(response.generic.context == 'incoming-operator-dial-number'){
												incoming = 1;
												acall.src = response.generic.calleridnum;
												acall.dst = response.generic.extension;
											}
											
											if(response.generic.context == 'cabs-dial-number'){
												acall.accountcode = response.generic.accountcode;
												acall.src = response.generic.calleridnum;
												acall.dst = response.generic.extension;
												acall.duration = response.generic.duration;
											}
											if(response.generic.context == 'from-trunk'){
												acall.src = response.generic.connectedlinenum;
												acall.dst = response.generic.calleridnum;
											}
											
											console.log("Nome : " + acall.name);
										}
									});
									
									if(!call_exists){
										// rimuovi la chiamata
										calls.pop(acall);
									}else{
										// costruiamo la tabella se abbiamo tutti i dati
										if(acall.src != '' && acall.dst != '' && acall.accountcode != ''){
											jQuery.ajax({
												   type: 'GET',
												   url: '/phoneusers/name/'+acall.accountcode,
												   async: false,
												   dataType: 'json',
												   success: function(response){
														acall.name = response.data.name;
														var recording = response.data.recording;
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
															row += '<button class="btn btn-warning disabled">In registrazione</button>&nbsp;';														
														}else{
															row += '<button class="btn btn-warning record-call" data-channel="' + acall.channel +'" data-file="' + filename + '">Registra</button>&nbsp;';
														}
														row += '<button class="btn btn-danger hangup-call" data-channel="' + acall.channel + '">Riaggancia</button>';
														row += '</td></tr>';
														//console.log(row);
														jQuery('#realtime-table').append(row);
												   },
												   error: function(jqXHR, textStatus, errorThrown){
														//alert('Errore nella trasmissione del dato');
												   },
											   });
										
											
										}
									}
								});
							},
							error: function(jqXHR, textStatus, errorThrown){
								console.log(textStatus, errorThrown);
							},
						});
			},
			error: function(jqXHR, textStatus, errorThrown){
			   console.log(textStatus, errorThrown);
			},
        });
}


jQuery(function(){
	var timer = setInterval(function(){
		next_mode = $('.daynight').attr('data-next-mode');
		// effettuiamo il realtime solo se non siamo in Notte
		if(next_mode == 'NOTTE'){
			update_realtime();
		}
	},3000);
	        
})
