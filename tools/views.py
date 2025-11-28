import os
import subprocess
import requests
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from acls.models import Acl
from prefs.models import Extension

logger = logging.getLogger(__name__)

#@login_required
#def tools_home(request):
#    user = request.user
#    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
#    variables['diskusage'] = 0
#    variables['extdiskusage'] = 0
#    if request.GET.get("err") != '1':
#        try:
#            variables['diskusage'] = _tool_get_disk_usage(settings.FILESYSTEM)
#            variables['extdiskusage'] = _tool_get_disk_usage(settings.EXT_FILESYSTEM)
#            variables['peers_status'] = _get_peers_status_remote()
#        except Exception as e:
#            return redirect("/tools/?err=1&err_msg=%s" % format(e))
#            #return redirect("/tools/?err=1&err_msg=Impossibile recuperare il valore di occupazione disco"
#    return render(request, 'tools/home.html', variables)

@login_required
def tools_home(request):
    user = request.user
    variables = Acl.get_permissions_for_user(user.id, user.is_staff)
    variables['diskusage'] = 0
    variables['extdiskusage'] = 0
    variables['peers_status'] = []

    if request.GET.get("err") != '1':
        try:
            variables['diskusage'] = _tool_get_disk_usage(settings.FILESYSTEM)
            variables['extdiskusage'] = _tool_get_disk_usage(settings.EXT_FILESYSTEM)
            # variables['extdiskusage'] = _tool_get_disk_usage_local(settings.EXT_FILESYSTEM)
            variables['peers_status'] = _get_peers_status_remote()
        except Exception as e:
            print(e)
            return redirect("/tools/?err=1&err_msg=%s" % str(e))

    return render(request, 'tools/home.html', variables)

def _tool_get_disk_usage(disk: str) -> float:
    # Esempi validi per `disk`: mountpoint (/ , /data) o device (/dev/sda1)
    try:
        # Usiamo df POSIX (-P) e non -h, poi estraiamo la colonna %
        out = subprocess.check_output(["df", "-P"], text=True)
        lines = [l for l in out.splitlines() if disk in l]

        if not lines:
            # fallback: prova a matchare per mountpoint esatto in colonna 6
            for l in out.splitlines()[1:]:
                parts = l.split()
                if len(parts) >= 6 and parts[5] == disk:
                    lines = [l]
                    break

        percents = []
        for l in lines:
            m = re.search(r"\s(\d+)%\s", l)
            if m:
                percents.append(int(m.group(1)))

        if not percents:
            return 0.0

        real_usage = max(percents)  # scegli il peggiore se ci sono più match
        safety_usage = real_usage * 1.2
        if safety_usage > 100:
            safety_usage = 100  # (attenzione: nella tua versione c’era un typo safety_sage)
        return float(safety_usage)
    except Exception:
        return 0.0

def _tool_get_disk_usage_old(disk):
    cmd = f"df -h | grep '{disk}' | awk '{{print $5}}' | sed 's/%//'"
    percent = os.popen(cmd).read().strip()

    if not percent or percent == '' or percent == '\n':
        cmd_alt = f"df -h | grep -E '/{disk}$|{disk}$'"
        result_alt = os.popen(cmd_alt).read().strip()

        if result_alt:
            lines = result_alt.split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 5 and '%' in parts[4]:
                    percent = parts[4].replace('%', '')
                    break
    if (percent):
        real_usage = float(percent.replace("%", "").strip())
        safety_usage = real_usage * 1.2
        if safety_usage > 100: safety_sage = 100
        return safety_usage
    return 0


def _get_peers_status_remote():
    """Recupera lo stato degli interni dal server remoto"""
    try:
        remote_url = settings.REMOTE_TOOLS_SERVER

        response = requests.get(
            f"{remote_url}/api/tools-peers-status",
            timeout=15
        )
        print(response.text)
        response.raise_for_status()

        data = response.json()
        if data.get('success'):
            peers = []
            for peer in data.get('peers', []):
                peers.append({
                    'extension': {'extension': peer['extension'], 'name': peer['name']},
                    'status': peer['status']
                })
            return peers
        else:
            logger.error(f"Errore dal server remoto: {data.get('error')}")
            return []

    except requests.exceptions.RequestException as e:
        logger.error(f"Errore di connessione al server remoto: {e}")
        raise Exception("Impossibile connettersi al server remoto")
    except Exception as e:
        logger.error(f"Errore generico: {e}")
        raise
