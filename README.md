# FROGS

## Overview

The Frequent Rainfall Observations on GridS (FROGS) database
is a collection of daily precipitation products on a common 1×1 deg grid.
The collection includes satellite, ground-based and reanalysis products.
Most of the satellite products were calibrated using rain gauges data,
for these, where available, the non adjusted version is also provided.
The temporal range included starts from 1901 to 2019 depedning on the data product.
Where it is possible the database will be extended in future updates of FROGs.
The data products spatial coverage is also dependent on the original sources.

For more information please refer to the [FROGs website](https://frogs.prod.lamp.cnrs.fr/)
and in particular to their news page for updates.

## Data location

We've downloaded FROGS data to:

```
/g/data/ia39/frogs/replica/data/1DD_V1/<dataset>/<files>
```

Each `<dataset>` is listed below depending on the source data type and spatial coverage.

Satellite based quasi global:
- 3B42 v7.0
- 3B42 v7.0 IR
- 3B42 v7.0 MW
- 3B42 RT v7.0
- 3B42 RT v7.0 uncalibrated
- CMORPH V1.0, RAW
- CMORPH V1.0, CRT
- GPCP 1DD CDR v1.3, not-enforced
- GPCP 1DD CDR v1.3, enforced
- GPCP IP
- GSMAP-RNL-gauges v6.0
- GSMAP-RNL-no gauges v6.0
- GSMAP-NRT-gauges v6.0
- GSMAP-NRT-no gauges v6.0
- IMERG v6 early uncalibrated
- IMERG v6 late uncalibrated
- IMERG v6 final uncalibrated
- IMERG v6 final calibrated
- PERSIANN CCS CDR 
- PERSIANN CDR v1 r1

Land only:
- CHIRP v1
- CHIRP v2
- SM2RAIN-CCI

Ocean only:
- HOAPS v4

Satellite based regional:
- ARC v2
- COSH
- TAMSAT v2
- TAMSAT v3
- TAPEER v1.5

Rain gauges based:
- CPC
- GPCC First Guess v1
- GPCC Full Daily v1
- GPCC Full Daily v2018
- GPCC Full Daily v2020
- REGEN Long Term Stations v1-2019
- REGEN All Stations v1-2019

Atmospheric reanalysis:
- CFSR
- ERA5
- ERA Interim
- GSWP3 Rain & Snow
- JRA55
- MERRA1
- MERRA2

## Data citation

Roca, R., Alexander, L. V., Potter, G., Bador, M., Jucá, R., Contractor, S., Bosilovich, M. G., and Cloché, S.: FROGs: a daily 1×1 gridded precipitation database of rain gauge, satellite and reanalysis products, https://doi.org/10.14768/06337394-73A9-407C-9997-0E380DAC5598, 2019, accesed on <date>

As this is an ongoing collection more data is added without chnages to the doi, so please specify date of access in your citation.

Please note that this is a collection of datasets and the original sources should be cited too wherever possible.

## Reference

Roca R, Alexander LV, Potter G, Bador M, Jucá R, Contractor S, Bosilovich MG, and Cloché S (2019).
FROGS: a daily 1° × 1° gridded precipitation database of rain gauge, satellite and reanalysis products.
*Earth System Science Data*, 11, 1017-1035.
https://doi.org/10.5194/essd-11-1017-2019
