#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script per creare tutte le preferenze necessarie nel database PhoneCab
Eseguire con: python create_default_prefs.py
"""

import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phonecab.settings')

# Import Django after setting up the path
import django
django.setup()

from prefs.models import Pref


def create_default_prefs():
    """Crea tutte le preferenze predefinite necessarie"""
    
    default_prefs = [
        ('min_duration_with_credit', '0'),
        ('alert_before_end', '0'),
        ('enable_first_in', '0'),
        ('ordinary_lawyer', '0'),
        ('change_threshold', '0'),
        ('threshold', '600'),  # 10 minuti in secondi
        ('change_additional_calls', '0'),
        ('default_additional_calls', '0'),
        ('max_calls_per_day', '0'),
        ('lawyer_call_limit', '0'),
        ('limit_additional_calls_per_day', '0'),
        ('covid_general', '0'),
        ('limit_duration', '0'),
        ('header', 'PhoneCab - Sistema di Gestione Chiamate'),
    ]
    
    created_count = 0
    updated_count = 0
    
    for key, default_value in default_prefs:
        # Usa get_or_create che bypassa il custom save per la creazione
        pref, created = Pref.objects.get_or_create(
            key=key, 
            defaults={'value': default_value}
        )
        
        if created:
            print("✓ Creata preferenza '%s' con valore: '%s'" % (key, default_value))
            created_count += 1
        else:
            print("✓ Preferenza '%s' già esistente con valore: '%s'" % (key, pref.value))
            updated_count += 1
    
    print("\n--- RIEPILOGO ---")
    print("Preferenze create: %d" % created_count)
    print("Preferenze esistenti: %d" % updated_count)
    print("Totale preferenze: %d" % (created_count + updated_count))
    
    # Verifica finale
    print("\n--- VERIFICA FINALE ---")
    all_prefs = Pref.objects.all().order_by('key')
    for pref in all_prefs:
        print("'%s' = '%s'" % (pref.key, pref.value))


if __name__ == '__main__':
    print("Creazione preferenze predefinite per PhoneCab...")
    create_default_prefs()
    print("Completato!") 