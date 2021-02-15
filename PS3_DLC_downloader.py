# Small python script that will download DLCs for specified PS3 title ID.
# Requirements: pkgi-formatted file containing DLCs

import csv
import os
import urllib.request

DOWNLOAD_WITHOUT_RAP = False  # Set it to true to download DLCs not having RAP files
DOWNLOAD_PKG_PATH = 'D:/DLC'  # Set path to download PKG
if not os.path.isdir(DOWNLOAD_PKG_PATH):
    os.mkdir(DOWNLOAD_PKG_PATH)
DOWNLOAD_RAP_PATH = 'D:/DLC/RAP'  # Set path to download RAP
if not os.path.isdir(DOWNLOAD_RAP_PATH):
    os.mkdir(DOWNLOAD_RAP_PATH)

GAME_LIST = [  # Containing list of title ID (e.g. BCUS00000)
    '',
]

with open('pkgi_dlcs.txt', encoding='utf8') as PKGI_DLCS:
    reader = csv.DictReader(PKGI_DLCS, fieldnames=[
        'contentid',
        'type',
        'name',
        'description',
        'rap',
        'url',
        'size',
        'checksum'
    ])
    dl_list = []
    for row in reader:
        if row['contentid'][7:16] not in GAME_LIST:  # Filter out content not in GAME_LIST
            continue
        if not DOWNLOAD_WITHOUT_RAP and row['rap'] == '':  # Skip content without RAP (or not)
            continue
        dl_list.append(row)

    for item in dl_list:
        download_dir = os.path.join(DOWNLOAD_PKG_PATH, item['contentid'][7:16])
        if not os.path.isdir(download_dir):  # Create folder for each title ID
            os.mkdir(download_dir)
        # Download PKG
        download_url = item['url']
        file_name = download_url.split('/')[-1]
        urllib.request.urlretrieve(download_url, os.path.join(download_dir, file_name))
        # Save RAP
        rap = item['rap']
        if rap == 'NOT REQUIRED':  # Skip downloading RAP if not required
            continue
        if not os.path.isdir(os.path.join(DOWNLOAD_RAP_PATH, item['contentid'][7:16])):
            os.mkdir(os.path.join(DOWNLOAD_RAP_PATH, item['contentid'][7:16]))
        rap_path = os.path.join(os.path.join(DOWNLOAD_RAP_PATH, item['contentid'][7:16]), rap + '.rap')
        rap_file = open(rap_path, 'wb')
        rap_file.write(bytes.fromhex(rap))
        rap_file.close()
