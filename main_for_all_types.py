from stitcher_processed import stitch_processed
from stitcher_unprocessed import stitch_unprocessed
import configparser

if __name__ == '__main__':
    settings = configparser.ConfigParser()
    with open('settings.ini', 'r', encoding='utf-8') as config_file:
        settings.read_file(config_file)
    stitch_type = settings.get('DEFAULT', 'WHAT_TYPE_OF_STITCH')
    video_name = settings.get('DEFAULT', 'VIDEO_NAME')

    if stitch_type == 'PROCESSED':
        size_of_frames = settings.getint('PROCESSED', 'SIZE_OF_FRAMES', fallback=3)
        auto = settings.getboolean('PROCESSED', 'AUTO_COUNT_VIDEOTHRESH', fallback=True)
        videothresh = settings.getint('PROCESSED', 'VIDEOTHRESH', fallback=235)
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
        how_to_stitch = settings.getboolean('UNPROCESSED', 'HOW_TO_STITCH', fallback=True)
        step = settings.getint('UNPROCESSED', 'STEP', fallback=1)
        overlap = settings.getint('UNPROCESSED', 'OVERLAP', fallback=5)
        num_to_stitch = settings.getint('UNPROCESSED', 'NUM_TO_STITCH', fallback=10)
        every_count = settings.getint('UNPROCESSED', 'EVERY_COUNT', fallback=100)
        need_to_clear_folder_unprocessed = settings.getboolean('UNPROCESSED', 'NEED_TO_CLEAR_FOLDER_UNPROCESSED', fallback=False)

        stitch_unprocessed(

            how_to_stitch=how_to_stitch,
            every_count=every_count,
            video_name=video_name,
            step=step,
            overlap=overlap,
            num_to_stitch=num_to_stitch,
            need_to_clear_folder_unprocessed=need_to_clear_folder_unprocessed
        )
