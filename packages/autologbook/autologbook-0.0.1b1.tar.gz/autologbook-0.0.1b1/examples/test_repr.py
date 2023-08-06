# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 11:31:18 2022

@author: Antonio
"""

from pathlib import Path

from autologbook import autoprotocol


def main():
    p = Path("C:/Users/Antonio/Documents/pyenv/devenv/autologbook/examples/fei.tif")

    sample = autoprotocol.Sample('NewSample')
    sample.parent = None
    print(f'Sample just after creation\n{sample}')

    ssample = autoprotocol.Sample('SubSample', sample.name)
    print(f'SubSample just after creation\n{ssample}')

    sample.addSubSample(ssample.name)
    print(f'Sample just after addition of 1 ssample\n{sample}')

    microPic = autoprotocol.QuattroFEIPicture(str(p))
    microPic.crop_databar()
    print(f'Microscope picture just after creation\n{microPic}')
    print('Representation on the next line')
    print(microPic.__repr__())

    sample.addMicroscopePicture(microPic)

    print(f'Sample just after addition of 1 pic\n {sample}')

    prot = autoprotocol.Protocol(p, '123', 'asa', 'saa')
    prot.addSample(sample)
    prot.addSample(ssample)
    print(prot)


if __name__ == '__main__':
    main()
