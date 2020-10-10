# -*- coding: utf-8 -*-
BOT_NAME = 'LOGICIMMONEUF'
SPIDER_MODULES = ['LOGICIMMONEUF.spiders']
NEWSPIDER_MODULE = 'LOGICIMMONEUF.spiders'

ROBOTSTXT_OBEY = False
#USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
USER_AGENT = "curl 2.0"
#DOWNLOAD_DELAY = 360
#COOKIES_ENABLED = False
#HTTPCACHE_IGNORE_MISSING=True
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = '/home/h.mahmoudi/LOGICIMMONEUF/LOGICIMMONEUF/spiders/cache'
HTTPCACHE_IGNORE_HTTP_CODES =  [500, 503, 504, 407, 409, 429, 439, 307, 302,403, 404]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
'LOGICIMMONEUF.pipelines.LogicimmoneufPipeline': 300,
}


LOG_STDOUT = True
### Patch - Build a custom logs folder to store all log files with timestamp
# https://github.com/scrapy/scrapy/blob/master/scrapy/utils/log.py
site='logicimmoneuf'

import time, os
path = "/home/h.mahmoudi/LOGICIMMONEUF/LOGICIMMONEUF/spiders/logs"
if not os.path.exists(path):
        os.makedirs(path)
now = time.strftime("%Y%m%d_%Hh-%Mmin-%Ss")
LOG_FILE = "%s/%s_%s.log" % (path, site, now)

###
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'




CSV_DELIMITER = ";"
"""FEED_EXPORTERS = {
    'csv': 'LOGICIMMONEUF.middlewares.VO_databizCsvItemExporter'
}"""
"""FEED_EXPORTERS = {
            'csv': 'logicimmoneuf.middlewares.VO_databizCsvItemExporter'
}"""


#DOWNLOADER_MIDDLEWARES = {
#    'seloger_logique_immo_neuf.middlewares.SelogerLogiqueImmoNeufSpiderMiddleware': 1,
#'LOGICIMMONEUF.gabesmid.LuminatiRotateIpAddressMiddleware': 1,
#}


FEED_EXPORT_FIELDS = [
    'ANNONCE_LINK',
    'FROM_SITE',
    'ID_CLIENT',
    'ANNONCE_DATE',
    'ACHAT_LOC',
    'SOLD',
    'MAISON_APT',
    'CATEGORIE',
    'NEUF_IND',
    'NOM',
    'ADRESSE',
    'CP',
    'VILLE',
    'QUARTIER',
    'DEPARTEMENT',
    'REGION',
    'PROVINCE',
    'ANNONCE_TEXT',
    'ETAGE',
    'NB_ETAGE',
    'LATITUDE',
    'LONGITUDE',
    'M2_TOTALE',
    'SURFACE_TERRAIN',
    'NB_GARAGE',
    'PHOTO',
    'PIECE',
    'PRIX',
    'PRIX_M2',
    'URL_PROMO',
    'STOCK_NEUF',
    'PAYS_AD',
    'PRO_IND',
    'SELLER_TYPE',
    'MINI_SITE_URL',
    'MINI_SITE_ID',
    'AGENCE_NOM',
    'AGENCE_ADRESSE',
    'AGENCE_CP',
    'AGENCE_VILLE',
    'AGENCE_DEPARTEMENT',
    'EMAIL',
    'WEBSITE',
    'AGENCE_TEL',
    'AGENCE_TEL_2',
    'AGENCE_TEL_3',
    'AGENCE_TEL_4',
    'AGENCE_FAX',
    'AGENCE_CONTACT',
    'PAYS_DEALER',
]
