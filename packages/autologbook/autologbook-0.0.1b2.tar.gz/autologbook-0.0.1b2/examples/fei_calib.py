# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 21:16:29 2022

@author: Antonio
"""

import configparser
from pathlib import Path

from PIL import Image


class Resolution_Unit():
    none = 1
    inch = 2
    cm = 3
    inverse_resolution_unit = {none: 'none', inch: 'dpi', cm: 'dpcm'}


class Picture_Resolution():

    def __init__(self, xres, yres, ures):
        self.xres = float(xres)
        self.yres = float(yres)
        if ures not in (Resolution_Unit.none, Resolution_Unit.inch, Resolution_Unit.cm):
            raise ValueError('Invalid resolution unit')
        self.ures = ures

    def __eq__(self, other):
        if self.ures == other.ures:
            return round(self.xres, 5) == round(other.xres, 5) and round(self.yres, 5) == round(other.yres, 5)
        else:
            old_ures = other.ures
            other.convert_to_unit(self.ures)
            is_equal = round(self.xres, 5) == round(other.xres, 5) and round(
                self.yres, 5) == round(other.yres, 5)
            other.convert_to_unit(old_ures)
            return is_equal

    def __repr__(self):
        return (f'({self.xres:.5} {Resolution_Unit.inverse_resolution_unit[self.ures]} '
                f'x {self.yres:.5} {Resolution_Unit.inverse_resolution_unit[self.ures]})')

    def as_tuple(self):
        return (self.xres, self.yres, self.ures)

    def convert_to_unit(self, desired_um):

        if self.ures == Resolution_Unit.none or desired_um == Resolution_Unit.none:
            raise ValueError(
                'Impossible to convert, because resolution unit of measurement is none.')

        if self.ures == desired_um:
            conv_fact = 1
        else:
            if self.ures == Resolution_Unit.inch:
                if desired_um == Resolution_Unit.cm:
                    conv_fact = 1 / 2.54
                else:
                    raise ValueError('Invalid resolution unit of measurment')
            else:  # self.ures == resolution_unit.cm
                if desired_um == Resolution_Unit.inch:
                    conv_fact = 2.54
                else:
                    raise ValueError('Invalid resolution unit of measurment')

        self.ures = desired_um
        self.xres *= conv_fact
        self.yres *= conv_fact


def getFEIResolution(tiff_tags, preferred_um=None):

    fei_tag_code = 34682
    fei_metadata = configparser.ConfigParser(allow_no_value=True)
    fei_metadata.read_string(tiff_tags[fei_tag_code])

    pixel_width = fei_metadata.getfloat('Scan', 'PixelWidth')
    pixel_height = fei_metadata.getfloat('Scan', 'PixelHeight')

    xres = 1 / (pixel_width * 100)
    yres = 1 / (pixel_height * 100)
    ures = Resolution_Unit.cm

    fei_resolution = Picture_Resolution(xres, yres, ures)
    if preferred_um is not None:
        fei_resolution.convert_to_unit(preferred_um)

    return fei_resolution


def getTIFFResolution(tiff_tags, preferred_um=None):
    xres_code = 282
    yres_code = 283
    ures_code = 296

    tif_resolution = Picture_Resolution(tiff_tags.get(
        xres_code), tiff_tags.get(yres_code), tiff_tags.get(ures_code))
    if preferred_um is not None:
        tif_resolution.convert_to_unit(preferred_um)

    return tif_resolution


def main():

    tifin_filepath = Path('fei.tif')
    tifout_filepath = Path('fei_out.tif')

    with Image.open(tifin_filepath) as source_img:
        tiffinfo = source_img.tag_v2
        tif_resolution = getTIFFResolution(tiffinfo, None)
        print(f'TIFF resolution is {tif_resolution:}')

        fei_resolution = getFEIResolution(tiffinfo, None)
        print(f'FEI resolution is {fei_resolution}')

        if tif_resolution == fei_resolution:
            print('they are the same')
        else:
            print('they are different')

            xres, yres, ures = fei_resolution.as_tuple()
            source_img.save(tifin_filepath, x_resolution=xres,
                            y_resolution=yres, resolution_unit=ures, tiffinfo=tiffinfo)

    # with Image.open(tifout_filepath) as img:
    #     tiffinfo = img.tag_v2
    #     print(tiffinfo)

    with Image.open(tifin_filepath) as source_img:
        tiffinfo = source_img.tag_v2
        tif_resolution = getTIFFResolution(tiffinfo, None)
        print(f'TIFF resolution is {tif_resolution:}')

        fei_resolution = getFEIResolution(tiffinfo, None)
        print(f'FEI resolution is {fei_resolution}')

        if tif_resolution == fei_resolution:
            print('they are the same')
        else:
            print('they are different')

    with Image.open(tifin_filepath) as source_img:
        tiffinfo = source_img.tag_v2
        image_xsize, image_ysize = source_img.size

        fei_tag_code = 34682
        fei_metadata = configparser.ConfigParser(allow_no_value=True)
        fei_metadata.read_string(tiffinfo[fei_tag_code])

        scan_width = fei_metadata.getint('Image', 'ResolutionX')
        scan_height = fei_metadata.getint('Image', 'ResolutionY')

        if (image_xsize, image_ysize) != (scan_width, scan_height):
            source_img = source_img.crop((0, 0, scan_width, scan_height))
            tiffinfo[256] = scan_width
            tiffinfo[257] = scan_height
            source_img.save(tifout_filepath, tiffinfo=tiffinfo)
        else:
            print('no need to crop')


if __name__ == '__main__':
    main()
