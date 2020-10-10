# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from parsel import Selector
from scrapy.http import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urlparse import urljoin
import datetime
import os
import phonenumbers
import re, sys
import scrapy
import string
from bs4 import BeautifulSoup




annonce_LI_dict_11 = OrderedDict({
    'annonce_tmp_1': '',
    'ANNONCE_LINK': '',
    'FROM_SITE': '',
    'ID_CLIENT': '', # regex
    'ANNONCE_DATE': '',
    'ACHAT_LOC': '',
    'MAISON_APT': '',
    'CATEGORIE': "//table/tbody/tr[1]/td[1]/text()", # todo check
    'NEUF_IND': '',
    'NOM': "//div[@class='tabs-info']/div[@class='tab-content']/h1/text()",
    'ADRESSE': '//*[@id="gmap"]/@data-address',
    'CP': '//*[@id="gmap"]/@data-cp',
    'VILLE': '//*[@id="gmap"]/@data-city',
    'QUARTIER': '',
    'DEPARTEMENT': '',
    'REGION': '',
    'PROVINCE': '',
    'ANNONCE_TEXT': "//p[@class='prog-description prog-close']/text()",
    'ETAGE': '',
    'NB_ETAGE': '',
    'LATITUDE': '//*[@id="gmap"]/@data-lat',
    'LONGITUDE': '//*[@id="gmap"]/@data-lng',
    'M2_TOTALE': "(//tr/td[2]/text())[1]",
    'SURFACE_TERRAIN': '',
    'NB_GARAGE': '',
    'PHOTO': "(count(//div[@class='item']/img)*0.5)",
    'PIECE': '',
    'PRIX': "(//tr/td[3]/text())[1]",
    'PRIX_M2': '',
    'URL_PROMO': '',
    'PAYS_AD': '',
    'PRO_IND': '',
    'SELLER_TYPE': '',
    'MINI_SITE_URL': '',
    'MINI_SITE_ID': '',
    'AGENCE_NOM': "//div[@class='clearfix agency-container']/div[@class='content']/div[@class='col-xs-12 col-md-4'][2]/div[@class='infos']/h3/text()",
    'AGENCE_ADRESSE': "//div[@class='clearfix agency-container']/div[@class='content']/div[@class='col-xs-12 col-md-4'][2]/div[@class='infos']/p[2]/text()",
    'AGENCE_CP': '', #regex
    'AGENCE_VILLE': '', #regex
    'AGENCE_DEPARTEMENT': '', # regex todo
    'EMAIL': '',
    'WEBSITE': '',
    'AGENCE_TEL': "(//p[@class='diplay-phone-mobile']/text())[1]",
    'AGENCE_TEL_2': '',
    'AGENCE_TEL_3': '',
    'AGENCE_TEL_4': '',
    'AGENCE_FAX': '',
    'AGENCE_CONTACT': '',
    'PAYS_DEALER': '',
    'FLUX': '',
    'SITE_SOCIETE_URL': "//div[@class='infos']/a/@href",
    'SITE_SOCIETE_ID': '',
    'SITE_SOCIETE_NAME': '',
    'SIREN': '',
    'SPIR_ID': '',
    'STOCK_NEUF': "count(//i[@class='icon-phone display-phone lot-phone popin_contact'])",
    #'STOCK_NEUF': "count(//div[@id ='list-lots']/ul/li)-1",
    'SOLD':'',
})
import datetime
class LogicIMMO2spider(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': '0',
    }
    name = 'LOGICIMMONEUF_2020_09'
    allowed_domains = ['neuf.logic-immo.com']
    start_urls = [
                'https://neuf.logic-immo.com/habiter/programmes-neufs']

    def parse(self, response):
        for link in LxmlLinkExtractor(allow=()).extract_links(response):
            if ("neuf.logic-immo.com/appartement-" in link.url) \
                    or ("neuf.logic-immo.com/programme-" in link.url) \
                    or ("neuf.logic-immo.com/maison-" in link.url) \
                    or ("neuf.logic-immo.com/studio-" in link.url):
                link.url = re.sub("\?.*", '', link.url)
                yield Request(link.url)
            elif ("neuf.logic-immo.com" in link.url) \
                    and ("neuf.logic-immo.com/contact" not in link.url):
                yield Request(link.url.strip().replace('%20', ''))
        if ("neuf.logic-immo.com/programme-" not in response.url):
            return
        item_annonce = OrderedDict(annonce_LI_dict_11.items())
        item_annonce['ANNONCE_LINK'] = response.url
        for key, val in sorted(annonce_LI_dict_11.items()):
            if val != '':
                item_annonce[key] = extract_item(val, response)
        item_annonce['PAYS_AD'] = 'FR'
        item_annonce['FROM_SITE'] = "http://neuf.logic-immo.com/"
        item_annonce['PAYS_DEALER'] = 'FR'
        item_annonce['NEUF_IND'] = "Y"
        item_annonce['PRO_IND'] = "Y"
        item_annonce['SELLER_TYPE'] = "pro"
        item_annonce['ACHAT_LOC'] = "1"
        item_annonce['ANNONCE_TEXT'] = extract_item("//p[@class='prog-description prog-close']/text()", response)
        item_annonce['SOLD'] = "N"
        item_annonce['ID_CLIENT'] = extract_re('-\d{5}-(.*)', response.url)
        item_annonce['AGENCE_NOM'] = extract_item("//div[@class='infos']/h3/text()", response)
        soup = BeautifulSoup(response.body, 'lxml')
        item_annonce['AGENCE_ADRESSE'] = soup.find("div",{"class":"infos"}).findAll("p")[-1].get_text()
        item_annonce['AGENCE_ADRESSE']= item_annonce['AGENCE_ADRESSE'].strip()
        item_annonce['CP'] = extract_re('-(\d{5})-', response.url)
        item_annonce['DEPARTEMENT'] = str(item_annonce['CP'])[0:2]
        item_annonce['AGENCE_CP'] = extract_re('\d{5}', item_annonce['AGENCE_ADRESSE'])
        item_annonce['AGENCE_DEPARTEMENT'] = str(item_annonce['AGENCE_CP'])[0:2]
        descrip_promot = extract_item("//div[@class='infos']", response)
        item_annonce['SITE_SOCIETE_URL'] = urljoin("http://neuf.logic-immo.com/", item_annonce['SITE_SOCIETE_URL'])
        item_annonce['EMAIL'] = get_emails(descrip_promot)
        if len(item_annonce['CATEGORIE'].split(' ', 1)) > 1 :
           item_annonce['PIECE'] = item_annonce['CATEGORIE'].split(' ', 1)[1].replace('T', '')
        item_annonce['CATEGORIE'] = item_annonce['CATEGORIE'].split(' ', 1)[0]
        item_annonce['AGENCE_VILLE'] = extract_re("[a-zA-Z]+", item_annonce['AGENCE_ADRESSE'])        
        item_annonce['VILLE']= soup.find("ul",{"class":"listBreadcrumb"}).findAll("li")[-2].get_text()
        item_annonce['VILLE']= item_annonce['VILLE'].strip()
        item_annonce['VILLE']= item_annonce['VILLE'][item_annonce['VILLE'].find("Programmes neuf")+ 16 : ]
        item_annonce['ADRESSE']= soup.find("h2", {"class":"address"}).get_text()
        item_annonce['ADRESSE']= item_annonce['ADRESSE'].strip()
        item_annonce['PRIX'] = extract_re("(\d.*\d)", item_annonce['PRIX'])
#        print(item_annonce['PRIX'])
        item_annonce['M2_TOTALE'] = extract_re("(\d.*\d)", item_annonce['M2_TOTALE'])
        if "Parking" in extract_item("(//tr/td[1]/text())[1]", response):
            item_annonce['CATEGORIE'] = extract_item("//table/tbody/tr[2]/td[1]/text()", response)
            item_annonce['PRIX'] = extract_item("(//tr/td[3]/text())[2]", response)
            item_annonce['M2_TOTALE'] = extract_item("(//tr/td[2]/text())[2]", response)
        if ("ous" in item_annonce['PRIX']):
            item_annonce['PRIX'] = extract_item("(//tr/td[3]/text())[2]", response)
        if ("N" in item_annonce['M2_TOTALE']):
            item_annonce['M2_TOTALE'] = extract_item("(//tr/td[2]/text())[2]", response)
        if len(extract_item("//div[@class='infos']/a/@href",response)) > 5:
            item_annonce['MINI_SITE_URL'] = "http://neuf.logic-immo.com/" + extract_item("//div[@class='infos']/a/@href",response)
        try:
            if (item_annonce['STOCK_NEUF'] == 0):
                item_annonce['STOCK_NEUF'] = 1
        except:
            pass
        item_annonce['AGENCE_TEL'] = get_phones(item_annonce['AGENCE_TEL'])[0]
        item_annonce['AGENCE_TEL_2'] = get_phones(item_annonce['AGENCE_TEL_2'])[0]
        item_annonce['AGENCE_TEL_3'] = get_phones(item_annonce['AGENCE_TEL_3'])[0]
        item_annonce['AGENCE_TEL_4'] = get_phones(item_annonce['AGENCE_TEL_4'])[0]
        lat_long = soup.find("div", {"id" : "gmap"})
        print(lat_long)
        lat_long= str(lat_long)
        lat_long_2 =   lat_long[lat_long.find("position")+13:lat_long.find("]}]}")-1]

        item_annonce['LATITUDE'] = lat_long_2.split(",")[0]
        for i in  item_annonce['LATITUDE'] :
            if i == '"':
                 item_annonce['LATITUDE'] = item_annonce['LATITUDE'].replace(i, "")
        print("latitude" , item_annonce['LATITUDE'])
        item_annonce['LONGITUDE']= lat_long_2.split(",")[-1]
        for i in  item_annonce['LONGITUDE']  :
            if i == '"':
                 item_annonce['LONGITUDE'] = item_annonce['LONGITUDE'].replace(i, "")

        print("longitude" , item_annonce['LONGITUDE'])
        yield item_annonce


def extract_item(item_xpath, resp):
    return " ".join(" ".join(resp.xpath(item_xpath).extract()).split())

def get_phones(text):
    tels = ['', '', '', '', '', '', '', '', '', ]
    i = 0
    for match in phonenumbers.PhoneNumberMatcher(text, "FR"):
        if i < 5:
            exp = phonenumbers.format_number(
                match.number, phonenumbers.PhoneNumberFormat.NATIONAL)
            tels[i] = str(" ".join("".join(re.findall('\d+', exp)).split()))
            i = i + 1
    return tels    

def get_emails(ss):
    email = re.findall("[a-z0-9.\-]+@[a-z0-9.\-]+", ss)
    email = " ".join(" ".join(email).split())
    return email

def extract_re(pat, text):
    l = re.findall(pat, text)
    if not l:
        return ""
    return re.findall(pat, text)[0]    
