# -*- coding: utf-8 -*-

"""Flybase Search.

Synopsis: fly <gene_name>"""

import re
import csv
import os
from albertv0 import *

__iid__          = "PythonInterface/v0.2"
__prettyname__   = "Flybase Search"
__version__      = "1.0"
__trigger__      = "fly "
__author__       = "Tomoki Ishibashi"
__dependencies__ = []

icon_path        = os.path.dirname(__file__) + "/flybaseicon.png"
fbgn_csv_path    = os.path.dirname(__file__) + "/fbgn.csv"

def genotype2url(genotype, genotype_dict):
    fbgn = genotype_dict.get(genotype, False)
    if fbgn:
        return "http://flybase.org/reports/" + fbgn
    else:
        fbgn = genotype_dict.get(genotype.capitalize(), False)
        if fbgn:
            return "http://flybase.org/reports/" + fbgn
        else:
            fbgn = genotype_dict.get(genotype.title(), False)
            if fbgn:
                return "http://flybase.org/reports/" + fbgn
            else:
                fbgn = genotype_dict.get(genotype.lower(), False)
                if fbgn:
                    return "http://flybase.org/reports/" + fbgn
                else:
                    pattern = re.compile(genotype, re.IGNORECASE)
                    for k in genotype_dict:
                        mch = pattern.search(k)
                        if mch:
                            return "http://flybase.org/reports/" + genotype_dict[mch.group()]
                    return "http://flybase.org"


def handleQuery(query):
    results = []

    if query.isTriggered:
        item = Item(
            id         = __prettyname__,
            icon       = icon_path,
            completion = query.rawString,
            text       = "Open flybase",
            actions = [
                UrlAction(
                    "Open flybase", "http://flybase.org")
            ]
        )

        genotype_dict = {}
        with open(fbgn_csv_path) as genotype_file:
            for row in csv.reader(genotype_file):
                genotype_dict[row[0]] = row[1]

        if len(query.string) >= 1:
            try:
                url = genotype2url(query.string, genotype_dict)
                results.append(Item(
                    id = __prettyname__,
                    icon = icon_path,
                    text = "{} gene was found!".format(query.string),
                    subtext = "Open {}?".format(url),
                    actions = [
                        UrlAction(
                            "Open flybase", url)
                    ]
                ))
            except:
                return item

        else:
            return item
    return results

