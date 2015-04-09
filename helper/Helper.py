class Helper(object):

    """
    Helper

    Classe generica di aiuto
    """

    @staticmethod
    def make_pagination(objects_list, page, items_per_page=10):
        """Returns the paginated object list, the range of pages and the next page number"""
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

        paginator = Paginator(objects_list, items_per_page)

        if page == 0:
            page = 1
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)

        if page < items_per_page + 1:
            pagination_number = 0
        else:
            pagination_number = page / items_per_page

        page_range = []
        for i in range(1, items_per_page + 1):
            newpage = pagination_number * items_per_page + i
            if newpage >= paginator.num_pages:
                break
            page_range.append(newpage)

        next_page = (page / items_per_page + 1) * items_per_page + 1
        if next_page > paginator.num_pages:
            next_page = paginator.num_pages

        return [objs, page_range, next_page]

    @staticmethod
    def file_export(path_to_file):
        """Funzione che consente il download del file passato"""
        import mimetypes
        import os
        from django.http import HttpResponse

        export_file = open(path_to_file, "r")
        mimetype = mimetypes.guess_type(path_to_file)[0]
        if not mimetype:
            mimetype = "application/octet-stream"

        response = HttpResponse(export_file.read(), mimetype=mimetype)
        response[
            "Content-Disposition"] = "attachment; filename=%s" % os.path.split(path_to_file)[1]

        return response

    @staticmethod
    def convert_datestring_format(actual_date, input_format, output_format):
        import datetime
        return datetime.datetime.strptime(
            actual_date, input_format).strftime(output_format)

    @staticmethod
    def get_filter_detail(d):
        """Costruisce una stringa con la lista dei filtri utilizzati"""
        detail = ''
        if(len(d.keys()) == 0):
            return 'Nessun Filtro'

        if 'start_date' in d.keys():
            detail += "Data inizio: %s " % d['start_date']

        if 'end_date' in d.keys():
            detail += "Data fine: %s " % d['end_date']

        if 'accountcode' in d.keys():
            detail += "Codice: %s " % d['accountcode']

        if 'dst' in d.keys():
            detail += "Destinazione: %s " % d['dst']

        return detail

    @staticmethod
    def get_daynight():
        """Restituisce lo stato GIORNO/NOTTE del sistema e la corrispondente classe css"""
        import os
        from django.conf import settings
        value = 1

        if not settings.DEBUG:
            output = os.popen('/usr/sbin/asterisk -rx "database get night dbnightman"').read()
            value = int(output[7:8])

        daynight_text = 'NOTTE'
        daynight_class = 'danger'

        if value == 1:
            # NIGHT MODE
            daynight_text = 'GIORNO'
            daynight_class = 'success'

        return (daynight_text, daynight_class)
