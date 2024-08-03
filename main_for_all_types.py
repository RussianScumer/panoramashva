from key_framesver13 import stitch_processed
from stitcher_unprocessed import stitch_unprocessed
import configparser

if __name__ == '__main__':
    # Load settings from the configuration file
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    # Read configuration values
    stitch_type = settings.get('DEFAULT', 'WHAT_TYPE_OF_STITCH')
    video_name = settings.get('DEFAULT', 'VIDEO_NAME')

    if stitch_type == 'PROCESSED':
        size_of_frames = settings.getint('PROCESSED', 'SIZE_OF_FRAMES', fallback=3)
        auto = settings.getboolean('PROCESSED', 'AUTO_COUNT_VIDEOTHRESH', fallback=True)
        videothresh = settings.getint('PROCESSED', 'DELAY_FRAMECOUNT', fallback=235)
        framecount = settings.getint('PROCESSED', 'DELAY_FRAMECOUNT', fallback=150)
        need_to_resize = settings.getboolean('PROCESSED', 'NEED_TO_RESIZE', fallback=True)
        need_to_clear_folder = settings.getboolean('PROCESSED', 'NEED_TO_CLEAR_FOLDER', fallback=False)

        stitch_processed(
            video_name=video_name,
            size_of_frames=size_of_frames,
            auto=auto,
            videothresh=videothresh,
            framecount=framecount,
            need_to_resize=need_to_resize,
            need_to_clear_folder=need_to_clear_folder
        )

    elif stitch_type == 'UNPROCESSED':
        how_to_stitch = settings.get('UNPROCESSED', 'HOW_TO_STITCH', fallback=True)
        step = settings.getint('UNPROCESSED', 'STEP', fallback=1)
        overlap = settings.getfloat('UNPROCESSED', 'OVERLAP', fallback=5)
        num_to_stitch = settings.getint('UNPROCESSED', 'NUM_TO_STITCH', fallback=10)

        stitch_unprocessed(
            how_to_stitch=how_to_stitch,
            vid_name=video_name,
            step=step,
            overlap=overlap,
            num_to_stitch=num_to_stitch
        )
