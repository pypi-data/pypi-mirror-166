import os
from typing import Optional, Tuple, Union

import cv2
from lgg import logger


def read_video(video: str, resize: Optional[Union[Tuple, int]] = None, out_path: str = None, auto_viz: bool = False):
    """ Read video from path frame by frame.

    This function returns a generator that yields frames from the video.
    This function returns a list containing a single frame each time it is called,
    to ensure that all changes to the returned frame are saved in the new video (when out_path is specified).

    Note:
        - This function is a generator, i.e. it yields frames one by one.
        - If resize is not None, each video frame will be resized to the given size.
        - Video frames are BGR arrays.
        - If out_path is not None, video will be saved to the given path.
            Note that all changes that are applied to the first element of the yielded list will be saved to the
            given path.

    Args:
        video (str, cv2.VideoCapture): Path to video or the video capture itself.
        resize (tuple, Optional): Resize video frame to this size (w, h). If None, the frame is left as is.
        out_path (str, Optional): Path to save the video. If None, the video is not saved.

    Returns:
        video (cv2.VideoCapture): List containing a single video frame in RGB format.

    Examples:
        >>> for frame_list in read_video('video.mp4'):
        >>>     frame = frame_list[0]   # frame_list is a list containing a single frame
        >>>     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        >>>     cv2.imshow('frame', frame)
        >>>     frame_list[0] = frame  # save changes to the frame

    """
    if isinstance(resize, int):
        resize = (resize, resize)

    if out_path is not None:
        logger.info(f'Saving output video to {out_path}')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if isinstance(video, str):
        cap = cv2.VideoCapture(video)
    else:
        cap = video

    if out_path is not None:
        width = int(cap.get(3))  # float `width`
        height = int(cap.get(4))  # float `height`
        fps = cap.get(5)  # int `fps`
        if resize is not None:
            width, height = resize
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'h264'), fps, (width, height), True)

    # Check if camera opened successfully
    if not cap.isOpened():
        logger.error("Error opening video stream or file")
        exit(1)

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            if resize is not None:
                frame = cv2.resize(frame, resize)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            l = [frame]
            yield l
            frame = l[0]
            if out_path is not None:
                out.write(frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                logger.info("Video stream ended by the user")
                break
            if auto_viz:
                cv2.imshow('frame', frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()
    if out_path is not None:
        out.release()
    cv2.destroyAllWindows()
