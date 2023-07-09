# -*- coding: utf-8 -*-
# Copyright © 2023 by Nick Jenkins. All rights reserved

"""This self contained script will record audio for 5 seconds then play back the audio for 5 seconds.
Uses the singleton iOS audio playback controller AVAudio.
It will attempt to use bluetooth connected devices for input and output,
or if there is no bluetooth connected or it fails it will revert to default phone microphone and speaker.
Everytime a new record or playback sequence is about to begin the program will
check for and attempt to use bluetooth audio"""
