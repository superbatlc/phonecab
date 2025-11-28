var Record = {

    showWarning : function() {
        requestData("POST", "html", '/records/show_warning/', {},
            function(response){
                var title = "Eliminazione registrazioni";
                var dict = {
                    title : title,
                    content : response,
                    onSave : Record.check,
                    saveButton : 'Conferma',
                    onRemove : null,
                }
            Modal.open(dict);
            }, function(error){
                showMessageBox("Errore", "Il file è stato scaricato", "alert-danger");
            }
        );
    },

    check : function(callback) {
        if($('#confirm-delete').is(':checked')) {
            Record.delete(callback);
        } else {
            showMessageBox("Errore", "Per eliminare &egrave; necessario confermare la propria scelta.", "alert-danger");
            callback({success: false});
        }
    },

    delete : function(callback){
        data = {}
        data.start_date = $('#start-date').val()
        data.end_date = $('#end-date').val()
        data.start_time = $('#start-time').val()
        data.end_time = $('#end-time').val()
        data.dst = $('#dst').val()
        data.pincode = $('#pincode').val()

        requestData("POST", "html", '/records/remove/', {data: data},
        function(response){
            var with_filter = (window.location.href.indexOf('?') > -1 ? '&':'?');
            window.location.href += with_filter + "ok=1&msg=Registrazioni eliminate con successo.";
            callback({success: true}); // inutile se facciamo cambio pagina
        },
        function(error){
            showMessageBox("Errore", "Errore eliminazione registrazioni.", "alert-danger");
            callback({success: false});
        })
    },
}

// Gestione download registrazioni senza lasciare la pagina
$(function() {
    $(document).on('click', '.recording-download', function(event) {
        event.preventDefault();
        event.stopPropagation();

        var $link = $(this);
        var url = $link.data('url') || $link.attr('href');

        if (!url || $link.data('downloading')) return;

        $link.data('downloading', true);
        var previewWindow = window.open('about:blank', '_blank');

        var resetState = function() {
            $link.data('downloading', false);
        };

        var closePreview = function() {
            if (previewWindow && !previewWindow.closed) {
                previewWindow.close();
            }
        };

        var onError = function() {
            closePreview();
            showMessageBox("Errore", "Il file è stato scaricato.", "alert-danger");
            resetState();
        };

        var openRecording = function(contentType) {
            if (!previewWindow) {
                showMessageBox("Errore", "Impossibile aprire la registrazione: abilitare i popup.", "alert-danger");
                resetState();
                return;
            }

            var safeUrl = url.replace(/\"/g, '&quot;');
            var type = contentType || 'audio/wav';

            previewWindow.document.open();
            previewWindow.document.write('<!doctype html><html><head><title>Registrazione</title></head>');
            previewWindow.document.write('<body style="margin:20px;font-family:sans-serif;">');
            previewWindow.document.write('<audio controls autoplay style="width:100%"><source src="' + safeUrl + '" type="' + type + '">Il browser non supporta l\\\'audio. <a href="' + safeUrl + '" target="_blank">Apri il file</a></audio>');
            previewWindow.document.write('</body></html>');
            previewWindow.document.close();
            resetState();
        };

        if (window.fetch) {
            fetch(url, { method: 'HEAD', credentials: 'same-origin' })
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('missing file');
                    }
                    return response.headers.get('Content-Type') || '';
                })
                .then(openRecording)
                .catch(onError);
        } else {
            var xhr = new XMLHttpRequest();
            xhr.open('HEAD', url, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    openRecording(xhr.getResponseHeader('Content-Type'));
                } else {
                    onError();
                }
            };
            xhr.onerror = onError;
            xhr.send();
        }
    });
});
