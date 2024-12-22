from fastapi import FastAPI, Request
from stitcher_unprocessed import stitch_unprocessed
from stitcher_processed import stitch_processed
from fromframesunprocessed import stitch_fromframesunprocessed
from fromframesprocessed import stitch_fromframesprocessed
app = FastAPI()


@app.get('/')
async def hw(request: Request):
    return "hw"


@app.get("/processed")
async def processed(video_name: str = '1', size_of_frames: int = 3, auto_count_videothresh: bool = True,
                    delay_framecount: int = -150,
                    need_to_resize: bool = True, need_to_clear_folder: bool = True, videothresh: int = 1):
    try:
        await stitch_processed(video_name, size_of_frames, auto_count_videothresh, delay_framecount, need_to_resize,
                               need_to_clear_folder, videothresh)
    except Exception as e:
        return {
            "response": "fail",
            "error": str(e)
        }
    return "success"


@app.get("/unprocessed")
async def unprocessed(video_name: str = '1', how_to_stitch: bool = True, step: int = 1, overlap: int = 5,
                      num_to_stitch: int = 10, every_count: int = 100,
                      need_to_clear_folder_unprocessed: bool = False):
    try:
        await stitch_unprocessed(video_name, how_to_stitch, step, overlap, num_to_stitch, every_count,
                                 need_to_clear_folder_unprocessed)
    except Exception as e:
        return {
            "response": "fail",
            "error": str(e)
        }
    return {
        "response": "success"
    }

#what flow pridetsia zadavat' vrychnuu esli gorizontal'no idet video false esli vertikalno true
@app.get("/fromframesunprocessed")
async def stitch_fromframesprocessed(pathtoframes: str='1', how_to_stitch: bool=True, step: int =1, overlap: int =5, num_to_stitch: int=10,
                       need_to_clear_folder_unprocessed: bool=False, what_flow: bool = False):
    try: 
        await stitch_fromframesunprocessed(pathtoframes, how_to_stitch, step, overlap, num_to_stitch,
                       need_to_clear_folder_unprocessed, what_flow)
    except Exception as e:
        return {
            "response": "fail",
            "error": str(e)
        }
    return {
        "response": "success"
    }

@app.get("/fromframesprocessed")
async def stitch_fromframesprocessed(path_to_frames: str = '1', 
                    need_to_resize: bool = True, need_to_clear_folder: bool = True):
    try:
        await stitch_fromframesprocessed(path_to_frames,  need_to_resize, need_to_clear_folder)
    except Exception as e:
        return {
            "response": "fail",
            "error": str(e)
        }
    return "success"
