from ffmpy import FFmpeg

if __name__ == '__main__':
    ff = FFmpeg(
        inputs={'fate.mkv': None},
        outputs={'fate.m3u8': '-c:v libx264 -c:a aac -strict -2 -f hls -hls_list_size 0 -hls_time 2'}
    )
    print(ff.cmd)
    # ffmpeg -i fate.mkv -c:v libx264 -c:a aac -strict -2 -f hls -hls_list_size 0 -hls_time 2 fate.m3u8
    ff.run()