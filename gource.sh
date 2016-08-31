#!/bin/sh
gource \
    -s .06 \
    -1280x720 \
    --auto-skip-seconds .1 \
    --multi-sampling \
    --stop-at-end \
    --key \
    --highlight-users \
    --hide mouse,progress \
    --file-idle-time 0 \
    --max-files 0  \
    --background-colour 000000 \
    --font-size 22 \
    --title "dabas minus" \
    --output-ppm-stream - \
    --output-framerate 25 \
    | ffmpeg -y -r 25 -f image2pipe -vcodec ppm -i - -b 65536K dbas_timelapse.mp4
