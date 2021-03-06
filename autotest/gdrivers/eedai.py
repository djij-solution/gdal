#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Earth Engine Data API Images driver test suite.
# Author:   Even Rouault, even dot rouault at spatialys.com
#
###############################################################################
# Copyright (c) 2017, Planet Labs
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import json
import struct
import sys

sys.path.append('../pymod')

from osgeo import gdal

import gdaltest

###############################################################################
# Find EEDAI driver


def eedai_1():

    gdaltest.eedai_drv = gdal.GetDriverByName('EEDAI')

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.SetConfigOption('CPL_CURL_ENABLE_VSIMEM', 'YES')

    gdaltest.EEDA_BEARER = gdal.GetConfigOption('EEDA_BEARER')
    gdaltest.EEDA_URL = gdal.GetConfigOption('EEDA_URL')
    gdaltest.EEDA_PRIVATE_KEY = gdal.GetConfigOption('EEDA_PRIVATE_KEY')
    gdaltest.EEDA_CLIENT_EMAIL = gdal.GetConfigOption('EEDA_CLIENT_EMAIL')

    return 'success'

###############################################################################
# Nominal case


def eedai_2():

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.FileFromMemBuffer('/vsimem/ee/assets/image', json.dumps({
        'type': 'IMAGE',
        'properties':
        {
            'foo': 'bar',
            'prop_B9': 'the_prop_B9',
            'prop_BAND_2': 'the_prop_B2'
        },
        'bands': [
            {
                "id": "B1",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 65535
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            },

            {
                "id": "B2",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 65535
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 10980,
                        "height": 10981
                    }
                }
            },

            {
                "id": "B9",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 65535
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            },

        ]
    }))

    # To please the unregistering of the persistent connection
    gdal.FileFromMemBuffer('/vsimem/ee/', '')

    gdal.SetConfigOption('EEDA_BEARER', 'mybearer')
    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    ds = gdal.OpenEx('EEDAI:image', open_options=['PIXEL_ENCODING=NPY'])
    gdal.SetConfigOption('EEDA_URL', None)

    expected_info = {
        "metadata": {
            "": {
                "foo": "bar"
            },
            "SUBDATASETS": {
                "SUBDATASET_1_DESC": "Bands B1,B9 of image",
                "SUBDATASET_2_DESC": "Band B2 of image",
                "SUBDATASET_2_NAME": "EEDAI:image:B2",
                "SUBDATASET_1_NAME": "EEDAI:image:B1,B9"
            },
            "IMAGE_STRUCTURE": {
                "INTERLEAVE": "PIXEL"
            }
        },
        "size": [
            1830,
            1831
        ],
        "driverLongName": "Earth Engine Data API Image",
        "bands": [
            {
                "colorInterpretation": "Undefined",
                "block": [
                    256,
                    256
                ],
                "metadata": {},
                "band": 1,
                "description": "B1",
                "type": "UInt16",
                "overviews": [
                    {
                        "size": [
                            915,
                            915
                        ]
                    },
                    {
                        "size": [
                            457,
                            457
                        ]
                    },
                    {
                        "size": [
                            228,
                            228
                        ]
                    }
                ]
            },
            {
                "colorInterpretation": "Undefined",
                "block": [
                    256,
                    256
                ],
                "metadata": {
                    "": {
                        "prop": "the_prop_B9"
                    }
                },
                "band": 2,
                "description": "B9",
                "type": "UInt16",
                "overviews": [
                    {
                        "size": [
                            915,
                            915
                        ]
                    },
                    {
                        "size": [
                            457,
                            457
                        ]
                    },
                    {
                        "size": [
                            228,
                            228
                        ]
                    }
                ]
            }
        ],
        "cornerCoordinates": {
            "center": [
                554880.0,
                4145070.0
            ],
            "upperRight": [
                609780.0,
                4200000.0
            ],
            "lowerLeft": [
                499980.0,
                4090140.0
            ],
            "lowerRight": [
                609780.0,
                4090140.0
            ],
            "upperLeft": [
                499980.0,
                4200000.0
            ]
        },
        "files": [],
        "description": "EEDAI:image",
        "geoTransform": [
            499980.0,
            60.0,
            0.0,
            4200000.0,
            0.0,
            -60.0
        ]
    }

    info = gdal.Info(ds, format='json')
    for key in expected_info:
        if not (key in info and info[key] == expected_info[key]):
            gdaltest.post_reason('fail')
            print('Got difference for key %s' % key)
            if key in info:
                print('Got: ' + str(info[key]))
            else:
                print('Does not exist in got info')
            print('Expected: ' + str(expected_info[key]))
            print('Whole info:')
            print(json.dumps(info, indent=4))
            return 'fail'

    if ds.GetProjectionRef().find('32610') < 0:
        gdaltest.post_reason('fail')
        print(ds.GetProjectionRef())
        return 'fail'

    if ds.GetRasterBand(1).GetOverview(-1) is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    if ds.GetRasterBand(1).GetOverview(3) is not None:
        gdaltest.post_reason('fail')
        return 'fail'

    npy_serialized = struct.pack(
        'B' * 8, 0x93, ord('N'), ord('U'), ord('M'), ord('P'), ord('Y'), 1, 0)
    descr = "{'descr': [('B1', '<u2'), ('B9', '<u2')], 'fortran_order': False, 'shape': (39, 38), }".encode(
        'ascii')
    npy_serialized += struct.pack('<h', len(descr))
    npy_serialized += descr
    val = struct.pack('<h', 12345) + struct.pack('<h', 23456)
    npy_serialized += ''.encode('ascii').join(val for i in range(38 * 39))

    gdal.FileFromMemBuffer(
        '/vsimem/ee/assets:getPixels&CUSTOMREQUEST=POST&POSTFIELDS={ "path": "image", "encoding": "NPY", "bandIds": [ "B1", "B9" ], "grid": { "origin": { "x": 607500.0, "y": 4092480.0 }, "pixelSize": { "x": 60.0, "y": -60.0 }, "dimensions": { "width": 38, "height": 39 } } }', npy_serialized)
    got_data = ds.GetRasterBand(1).ReadRaster(1800, 1810, 1, 1)
    got_data = struct.unpack('h', got_data)[0]
    if got_data != 12345:
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'
    got_data = ds.GetRasterBand(2).ReadRaster(1800, 1810, 1, 1)
    got_data = struct.unpack('h', got_data)[0]
    if got_data != 23456:
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    ds = None

    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    sub_ds = gdal.Open('EEDAI:image:B1,B9')
    gdal.SetConfigOption('EEDA_URL', None)
    if sub_ds.RasterCount != 2:
        gdaltest.post_reason('fail')
        print(sub_ds.RasterCount)
        return 'fail'

    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    sub_ds = gdal.Open('EEDAI:image:B2')
    gdal.SetConfigOption('EEDA_URL', None)
    if sub_ds.RasterCount != 1:
        gdaltest.post_reason('fail')
        print(sub_ds.RasterCount)
        return 'fail'

    got_md = sub_ds.GetRasterBand(1).GetMetadata()
    expected_md = {'prop': 'the_prop_B2'}
    if got_md != expected_md:
        gdaltest.post_reason('fail')
        print(got_md)
        return 'fail'

    gdal.SetConfigOption('EEDA_BEARER', None)

    return 'success'

###############################################################################
# Test OAuth2 with ServiceAccount


def eedai_3():

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    # Generated with 'openssl genrsa -out rsa-openssl.pem 1024' and
    # 'openssl pkcs8 -nocrypt -in rsa-openssl.pem -inform PEM -topk8 -outform PEM -out rsa-openssl.pkcs8.pem'
    # DO NOT USE in production !!!!
    gdal.SetConfigOption('EEDA_PRIVATE_KEY', """-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAOlwJQLLDG1HeLrk
VNcFR5Qptto/rJE5emRuy0YmkVINT4uHb1be7OOo44C2Ev8QPVtNHHS2XwCY5gTm
i2RfIBLv+VDMoVQPqqE0LHb0WeqGmM5V1tHbmVnIkCcKMn3HpK30grccuBc472LQ
DVkkGqIiGu0qLAQ89JP/r0LWWySRAgMBAAECgYAWjsS00WRBByAOh1P/dz4kfidy
TabiXbiLDf3MqJtwX2Lpa8wBjAc+NKrPXEjXpv0W3ou6Z4kkqKHJpXGg4GRb4N5I
2FA+7T1lA0FCXa7dT2jvgJLgpBepJu5b//tqFqORb4A4gMZw0CiPN3sUsWsSw5Hd
DrRXwp6sarzG77kvZQJBAPgysAmmXIIp9j1hrFSkctk4GPkOzZ3bxKt2Nl4GFrb+
bpKSon6OIhP1edrxTz1SMD1k5FiAAVUrMDKSarbh5osCQQDwxq4Tvf/HiYz79JBg
Wz5D51ySkbg01dOVgFW3eaYAdB6ta/o4vpHhnbrfl6VO9oUb3QR4hcrruwnDHsw3
4mDTAkEA9FPZjbZSTOSH/cbgAXbdhE4/7zWOXj7Q7UVyob52r+/p46osAk9i5qj5
Kvnv2lrFGDrwutpP9YqNaMtP9/aLnwJBALLWf9n+GAv3qRZD0zEe1KLPKD1dqvrj
j+LNjd1Xp+tSVK7vMs4PDoAMDg+hrZF3HetSQM3cYpqxNFEPgRRJOy0CQQDQlZHI
yzpSgEiyx8O3EK1iTidvnLXbtWabvjZFfIE/0OhfBmN225MtKG3YLV2HoUvpajLq
gwE6fxOLyJDxuWRf
-----END PRIVATE KEY-----
""")
    gdal.SetConfigOption('EEDA_CLIENT_EMAIL', 'my@email.com')
    gdal.SetConfigOption('GO2A_AUD', '/vsimem/oauth2/v4/token')
    gdal.SetConfigOption('GOA2_NOW', '123456')
    gdal.FileFromMemBuffer('/vsimem/oauth2/v4/token&POSTFIELDS=grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiAibXlAZW1haWwuY29tIiwgInNjb3BlIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvZWFydGhlbmdpbmUucmVhZG9ubHkiLCAiYXVkIjogIi92c2ltZW0vb2F1dGgyL3Y0L3Rva2VuIiwgImlhdCI6IDEyMzQ1NiwgImV4cCI6IDEyNzA1Nn0%3D.1W564xcQESVsqZmBEIMzj4rr0RuGa4RiUPZp5H%2FNENN9V9oPSTdacw%2BMiu3pcFf9AJv8wj0ajUeRsgTmvSicAftER49xeCQYUrs6uV122FGVsxml26kMFacNsCgRad%2Fy7xCAhMPfRJsqxS2%2BB392ssBeEzTGCSI6W3AsJg64OfA%3D',
                           '{ "access_token": "my_token", "token_type": "Bearer", "expires_in": 3600 }')

    ds = gdal.Open('EEDAI:image')

    gdal.SetConfigOption('EEDA_URL', None)
    gdal.SetConfigOption('EEDA_PRIVATE_KEY', None)
    gdal.SetConfigOption('EEDA_CLIENT_EMAIL', None)

    if gdal.GetLastErrorMsg().find('CPLRSASHA256Sign() not implemented') >= 0:
        return 'skip'

    if ds is None:
        return 'fail'

    return 'success'

###############################################################################
# Request in PNG mode


def eedai_4():

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.FileFromMemBuffer('/vsimem/ee/assets/image', json.dumps({
        'type': 'IMAGE',
        'bands':
        [
            {
                "id": "B1",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 255
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            },
            {
                "id": "B2",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 255
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            },
            {
                "id": "B3",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 255
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            }
        ]
    }))

    gdal.SetConfigOption('EEDA_BEARER', 'mybearer')
    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    ds = gdal.Open('EEDAI:image')
    gdal.SetConfigOption('EEDA_URL', None)

    mem_ds = gdal.GetDriverByName('MEM').Create('', 256, 256, 3)
    mem_ds.GetRasterBand(1).Fill(127)
    mem_ds.GetRasterBand(2).Fill(128)
    mem_ds.GetRasterBand(3).Fill(129)
    gdal.GetDriverByName('PNG').CreateCopy('/vsimem/out.png', mem_ds)
    f = gdal.VSIFOpenL('/vsimem/out.png', 'rb')
    png_data = gdal.VSIFReadL(1, 1000000, f)
    gdal.VSIFCloseL(f)
    gdal.Unlink('/vsimem/out.png')

    gdal.FileFromMemBuffer(
        '/vsimem/ee/assets:getPixels&CUSTOMREQUEST=POST&POSTFIELDS={ "path": "image", "encoding": "PNG", "bandIds": [ "B1", "B2", "B3" ], "grid": { "origin": { "x": 499980.0, "y": 4200000.0 }, "pixelSize": { "x": 60.0, "y": -60.0 }, "dimensions": { "width": 256, "height": 256 } } }', png_data)
    got_data = ds.GetRasterBand(1).ReadRaster(0, 0, 1, 1)
    got_data = struct.unpack('B', got_data)[0]
    if got_data != 127:
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    # Same with dataset RasterIO
    got_data = ds.ReadRaster(0, 0, 1, 1)
    got_data = struct.unpack('B' * 3, got_data)
    if got_data != (127, 128, 129):
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    # Same after flushing cache
    ds.FlushCache()
    got_data = ds.ReadRaster(0, 0, 1, 1)
    got_data = struct.unpack('B' * 3, got_data)
    if got_data != (127, 128, 129):
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    # Sub-sampled query
    gdal.FileFromMemBuffer(
        '/vsimem/ee/assets:getPixels&CUSTOMREQUEST=POST&POSTFIELDS={ "path": "image", "encoding": "PNG", "bandIds": [ "B1", "B2", "B3" ], "grid": { "origin": { "x": 499980.0, "y": 4200000.0 }, "pixelSize": { "x": 120.0, "y": -120.06557377049181 }, "dimensions": { "width": 256, "height": 256 } } }', png_data)
    got_data = ds.GetRasterBand(1).ReadRaster(
        0, 0, 2, 2, buf_xsize=1, buf_ysize=1)
    got_data = struct.unpack('B', got_data)[0]
    if got_data != 127:
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    # Same after flushing cache with dataset RasterIO
    ds.FlushCache()
    got_data = ds.ReadRaster(0, 0, 2, 2, buf_xsize=1, buf_ysize=1)
    got_data = struct.unpack('B' * 3, got_data)
    if got_data != (127, 128, 129):
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    ds = None

    gdal.SetConfigOption('EEDA_BEARER', None)

    return 'success'

###############################################################################
# Request in AUTO GTIFF mode


def eedai_geotiff():

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.FileFromMemBuffer('/vsimem/ee/assets/image', json.dumps({
        'type': 'IMAGE',
        'bands':
        [
            {
                "id": "B1",
                "dataType": {
                    "precision": "INTEGER",
                    "range": {
                        "max": 65535
                    }
                },
                "grid": {
                    "crsCode": "EPSG:32610",
                    "affineTransform": {
                        "translateX": 499980,
                        "translateY": 4200000,
                        "scaleX": 60,
                        "scaleY": -60
                    },
                    "dimensions": {
                        "width": 1830,
                        "height": 1831
                    }
                }
            }
        ]
    }))

    gdal.SetConfigOption('EEDA_BEARER', 'mybearer')
    gdal.SetConfigOption('EEDA_URL', '/vsimem/ee/')
    ds = gdal.Open('EEDAI:image')
    gdal.SetConfigOption('EEDA_URL', None)

    mem_ds = gdal.GetDriverByName('MEM').Create('', 256, 256, 1, gdal.GDT_UInt16)
    mem_ds.GetRasterBand(1).Fill(12345)
    gdal.GetDriverByName('GTiff').CreateCopy('/vsimem/out.tif', mem_ds)
    f = gdal.VSIFOpenL('/vsimem/out.tif', 'rb')
    data = gdal.VSIFReadL(1, 1000000, f)
    gdal.VSIFCloseL(f)
    gdal.Unlink('/vsimem/out.tif')

    gdal.FileFromMemBuffer(
        '/vsimem/ee/assets:getPixels&CUSTOMREQUEST=POST&POSTFIELDS={ "path": "image", "encoding": "GEOTIFF", "bandIds": [ "B1" ], "grid": { "origin": { "x": 499980.0, "y": 4200000.0 }, "pixelSize": { "x": 60.0, "y": -60.0 }, "dimensions": { "width": 256, "height": 256 } } }', data)
    got_data = ds.GetRasterBand(1).ReadRaster(0, 0, 1, 1)
    got_data = struct.unpack('H', got_data)[0]
    if got_data != 12345:
        gdaltest.post_reason('fail')
        print(got_data)
        return 'fail'

    ds = None

    gdal.SetConfigOption('EEDA_BEARER', None)

    return 'success'

###############################################################################
#


def eedai_real_service():

    if gdaltest.eedai_drv is None:
        return 'skip'

    if gdal.GetConfigOption('EEDA_PRIVATE_KEY_FILE') is None and gdal.GetConfigOption('EEDA_PRIVATE_KEY') is None:
        print('Missing EEDA_PRIVATE_KEY_FILE/EEDA_PRIVATE_KEY')
        return 'skip'

    if gdal.GetConfigOption('EEDA_CLIENT_EMAIL') is None:
        print('Missing EEDA_CLIENT_EMAIL')
        return 'skip'

    ds = gdal.Open('EEDAI:USDA/NAIP/DOQQ/n_4010064_se_14_2_20070725')
    if ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    res = gdal.Info(ds, format='json')
    expected = {'files': [], 'cornerCoordinates': {'upperRight': [415016.0, 4435536.0], 'lowerLeft': [408970.0, 4427936.0], 'lowerRight': [415016.0, 4427936.0], 'upperLeft': [408970.0, 4435536.0], 'center': [411993.0, 4431736.0]}, 'wgs84Extent': {'type': 'Polygon', 'coordinates': [[[-100.067433, 40.0651671], [-100.0663662, 39.9967049], [-99.9955511, 39.9973349], [-99.9965471, 40.0657986], [-100.067433, 40.0651671]]]}, 'description': 'EEDAI:USDA/NAIP/DOQQ/n_4010064_se_14_2_20070725', 'driverShortName': 'EEDAI', 'driverLongName': 'Earth Engine Data API Image', 'bands': [{'description': 'R', 'band': 1, 'colorInterpretation': 'Red', 'overviews': [{'size': [1511, 1900]}, {'size': [755, 950]}, {'size': [377, 475]}, {'size': [188, 237]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {}}, {'description': 'G', 'band': 2, 'colorInterpretation': 'Green', 'overviews': [{'size': [1511, 1900]}, {'size': [755, 950]}, {'size': [377, 475]}, {'size': [188, 237]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {}}, {'description': 'B', 'band': 3, 'colorInterpretation': 'Blue', 'overviews': [{'size': [1511, 1900]}, {'size': [755, 950]}, {'size': [377, 475]}, {'size': [188, 237]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {}}], 'coordinateSystem': {'wkt': 'PROJCS["NAD83 / UTM zone 14N",\n    GEOGCS["NAD83",\n        DATUM["North_American_Datum_1983",\n            SPHEROID["GRS 1980",6378137,298.257222101,\n                AUTHORITY["EPSG","7019"]],\n            TOWGS84[0,0,0,0,0,0,0],\n            AUTHORITY["EPSG","6269"]],\n        PRIMEM["Greenwich",0,\n            AUTHORITY["EPSG","8901"]],\n        UNIT["degree",0.0174532925199433,\n            AUTHORITY["EPSG","9122"]],\n        AUTHORITY["EPSG","4269"]],\n    PROJECTION["Transverse_Mercator"],\n    PARAMETER["latitude_of_origin",0],\n    PARAMETER["central_meridian",-99],\n    PARAMETER["scale_factor",0.9996],\n    PARAMETER["false_easting",500000],\n    PARAMETER["false_northing",0],\n    UNIT["metre",1,\n        AUTHORITY["EPSG","9001"]],\n    AXIS["Easting",EAST],\n    AXIS["Northing",NORTH],\n    AUTHORITY["EPSG","26914"]]'}, 'geoTransform': [408970.0, 2.0, 0.0, 4435536.0, 0.0, -2.0], 'metadata': {'IMAGE_STRUCTURE': {'INTERLEAVE': 'PIXEL'}}, 'size': [3023, 3800]}
    if expected != res:
        gdaltest.post_reason('fail')
        print(res)
        return 'fail'
    if ds.ReadRaster(0, 0, 1, 1) is None:
        gdaltest.post_reason('fail')
        return 'fail'

    ds = gdal.Open('EEDAI:MODIS/006/MYD09GA/2017_05_24')
    if ds is None:
        gdaltest.post_reason('fail')
        return 'fail'
    res = gdal.Info(ds, format='json')
    expected = {'files': [], 'cornerCoordinates': {'upperRight': [20015109.354, 10007554.677], 'lowerLeft': [-20015109.354, -10007554.677], 'lowerRight': [20015109.354, -10007554.677], 'upperLeft': [-20015109.354, 10007554.677], 'center': [9.6e-06, 6e-06]}, 'wgs84Extent': {'type': 'Polygon', 'coordinates': [[]]}, 'description': 'EEDAI:MODIS/006/MYD09GA/2017_05_24', 'driverShortName': 'EEDAI', 'driverLongName': 'Earth Engine Data API Image', 'bands': [{'description': 'num_observations_1km', 'band': 1, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {'IMAGE_STRUCTURE': {'PIXELTYPE': 'SIGNEDBYTE'}}}, {'description': 'state_1km', 'band': 2, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'UInt16', 'block': [256, 256], 'metadata': {}}, {'description': 'SensorZenith', 'band': 3, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Int16', 'block': [256, 256], 'metadata': {}}, {'description': 'SensorAzimuth', 'band': 4, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Int16', 'block': [256, 256], 'metadata': {}}, {'description': 'Range', 'band': 5, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'UInt16', 'block': [256, 256], 'metadata': {}}, {'description': 'SolarZenith', 'band': 6, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Int16', 'block': [256, 256], 'metadata': {}}, {'description': 'SolarAzimuth', 'band': 7, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Int16', 'block': [256, 256], 'metadata': {}}, {'description': 'gflags', 'band': 8, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {}}, {'description': 'orbit_pnt', 'band': 9, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {'IMAGE_STRUCTURE': {'PIXELTYPE': 'SIGNEDBYTE'}}}, {'description': 'granule_pnt', 'band': 10, 'colorInterpretation': 'Undefined', 'overviews': [{'size': [21600, 10800]}, {'size': [10800, 5400]}, {'size': [5400, 2700]}, {'size': [2700, 1350]}, {'size': [1350, 675]}, {'size': [675, 337]}, {'size': [337, 168]}, {'size': [168, 84]}], 'type': 'Byte', 'block': [256, 256], 'metadata': {}}], 'coordinateSystem': {'wkt': 'PROJCS["MODIS Sinusoidal",\n    GEOGCS["WGS 84",\n        DATUM["WGS_1984",\n            SPHEROID["WGS 84",6378137,298.257223563,\n                AUTHORITY["EPSG","7030"]],\n            AUTHORITY["EPSG","6326"]],\n        PRIMEM["Greenwich",0,\n            AUTHORITY["EPSG","8901"]],\n        UNIT["degree",0.01745329251994328,\n            AUTHORITY["EPSG","9122"]],\n        AUTHORITY["EPSG","4326"]],\n    PROJECTION["Sinusoidal"],\n    PARAMETER["false_easting",0.0],\n    PARAMETER["false_northing",0.0],\n    PARAMETER["central_meridian",0.0],\n    PARAMETER["semi_major",6371007.181],\n    PARAMETER["semi_minor",6371007.181],\n    UNIT["m",1.0],\n    AUTHORITY["SR-ORG","6974"]]'}, 'geoTransform': [-20015109.354, 926.625433056, 0.0, 10007554.677, 0.0, -926.625433055], 'metadata': {'IMAGE_STRUCTURE': {'INTERLEAVE': 'PIXEL'}, 'SUBDATASETS': {'SUBDATASET_2_NAME': 'EEDAI:MODIS/006/MYD09GA/2017_05_24:num_observations_500m,sur_refl_b01,sur_refl_b02,sur_refl_b03,sur_refl_b04,sur_refl_b05,sur_refl_b06,sur_refl_b07,QC_500m,obscov_500m,iobs_res,q_scan', 'SUBDATASET_2_DESC': 'Bands num_observations_500m,sur_refl_b01,sur_refl_b02,sur_refl_b03,sur_refl_b04,sur_refl_b05,sur_refl_b06,sur_refl_b07,QC_500m,obscov_500m,iobs_res,q_scan of MODIS/006/MYD09GA/2017_05_24', 'SUBDATASET_1_NAME': 'EEDAI:MODIS/006/MYD09GA/2017_05_24:num_observations_1km,state_1km,SensorZenith,SensorAzimuth,Range,SolarZenith,SolarAzimuth,gflags,orbit_pnt,granule_pnt', 'SUBDATASET_1_DESC': 'Bands num_observations_1km,state_1km,SensorZenith,SensorAzimuth,Range,SolarZenith,SolarAzimuth,gflags,orbit_pnt,granule_pnt of MODIS/006/MYD09GA/2017_05_24'}}, 'size': [43200, 21600]}
    if expected != res:
        gdaltest.post_reason('fail')
        print(res)
        return 'fail'
    if ds.ReadRaster(0, 0, 1, 1) is None:
        gdaltest.post_reason('fail')
        return 'fail'

    return 'success'

###############################################################################
#


def eedai_cleanup():

    if gdaltest.eedai_drv is None:
        return 'skip'

    gdal.SetConfigOption('CPL_CURL_ENABLE_VSIMEM', None)
    gdal.SetConfigOption('EEDA_BEARER', gdaltest.EEDA_BEARER)
    gdal.SetConfigOption('EEDA_URL', gdaltest.EEDA_URL)
    gdal.SetConfigOption('EEDA_PRIVATE_KEY', gdaltest.EEDA_PRIVATE_KEY)
    gdal.SetConfigOption('EEDA_CLIENT_EMAIL', gdaltest.EEDA_CLIENT_EMAIL)
    gdal.SetConfigOption('GO2A_AUD', None)
    gdal.SetConfigOption('GOA2_NOW', None)

    gdal.Unlink('/vsimem/ee/assets/image')
    gdal.RmdirRecursive('/vsimem/ee/')

    return 'success'


gdaltest_list = [
    eedai_1,
    eedai_2,
    eedai_3,
    eedai_4,
    eedai_geotiff,
    eedai_cleanup,
    eedai_real_service,
]

if __name__ == '__main__':

    gdaltest.setup_run('eedai')

    gdaltest.run_tests(gdaltest_list)

    gdaltest.summarize()
