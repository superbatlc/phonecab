-- Script per inserire tutte le preferenze necessarie nel database PhoneCab
-- Eseguire questo script per risolvere i problemi di preferenze mancanti

-- Nota: I valori possono essere modificati secondo le esigenze
-- 0 = disabilitato/falso, 1 = abilitato/vero

INSERT IGNORE INTO prefs_pref (key, value) VALUES 
('min_duration_with_credit', '0'),
('alert_before_end', '0'), 
('enable_first_in', '0'),
('ordinary_lawyer', '0'),
('change_threshold', '0'),
('threshold', '600'),  -- 10 minuti in secondi
('change_additional_calls', '0'),
('default_additional_calls', '0'),
('max_calls_per_day', '0'),
('lawyer_call_limit', '0'),
('limit_additional_calls_per_day', '0'),
('covid_general', '0'),
('limit_duration', '0'),
('header', 'PhoneCab - Sistema di Gestione Chiamate');

-- Verifica che tutte le preferenze siano state inserite
SELECT * FROM prefs_pref ORDER BY key; 