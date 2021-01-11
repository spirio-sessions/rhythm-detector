# rhythm-detector

## Description

This repository is part of the SPIRIO SESSIONS Project. It aims at designing and implementing means of detecting dominant beats in generic music as a sub-project of SPIRIO SESSIONS.

## Usage

`./rhythm deviceinfo --list`

gives a summary of all available physical audio devices on the local machine

`./rhythm detect --record DEVICE_ID [--profile NAME] --target IPv4:PORT`

runs rhythm detection on live recording of local hardware specified by `DEVICE_ID`

`./rhythm detect --load PATH [--profile NAME] --target IPv4:PORT`

runs rhythm detection on local file specified by `PATH`

both set detection parameter according to analysis profile `PROFILE` stored in `./analyser_config.ini`

both send detection results as OpenSoundControl messages via UDP to a target specified by `IPv4:PORT`