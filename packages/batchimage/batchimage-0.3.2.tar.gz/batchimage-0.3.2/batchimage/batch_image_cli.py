# Package Imports
import typer
import os
import time

from rich.pretty import pprint

# Module Imports
from batch_image_module import process_image

from typing import Tuple

# Typer App
app = typer.Typer()

interpolation_flags = {
    "cv2.INTER_NEAREST":  0,
    "cv2.INTER_LINEAR":  1,
    "cv2.INTER_CUBIC":  2,
    "cv2.INTER_AREA":  3,
    "cv2.INTER_LANCZOS4":  4,
    "cv2.INTER_LINEAR_EXACT":  5,
    "cv2.INTER_NEAREST_EXACT":  6,
    "cv2.INTER_MAX":  7,
    "cv2.WARP_FILL_OUTLIERS":  8,
    "cv2.WARP_INVERSE_MAP=":  16,
}

# Main Command.
#
# @app.callback(
#     invoke_without_command=True,
#     hidden=True
# )
# def main(
#         default: str  = typer.Option(
#             "",
#             "--dict",
#             "-d",
#             help="Python Dictionary / Ruby Hash name",
#         ),
#     ):
#
#     """
#         Process large batches of images in parallel.
#
#         You can,
#
#                 🔹 Compress Images - 🗜️
#
#                 🔹 Convert Images  - 🔄
#
#                 🔹 Crop Images  - 🔲
#
#                 🔹 Apply Filters  - 💅
#
#                 🔹 Convert Images  - 🔄
#
#
#         \n
#
#         batchimage on Pypi           :  https://pypi.org/project/batchimage
#
#         batchimage on Github         :  https://github.com/insumanth/batchimage
#
#         Please report any issues     :  https://github.com/insumanth/batchimage/issues
#     """
#
#     print(f"Main {default}")
#


@app.command(hidden=True)
def display(
        directory_path: str,
):
    print(directory_path)
    print(print_files(directory_path))


@app.command(hidden=True)
def compress(

        source: str = typer.Argument(
            ...,
            help="Source Directory containing Image files",
            metavar="source",
            # rich_help_panel="compress",
        ),

        destination: str = typer.Argument(
            ...,
            help="Destination Directory where processed images are stored",
            metavar="destination",
            # rich_help_panel="compress",
        ),

):
    print(f"{source} \n {destination}")
    print(f"compress. Yet to be implemented")


@app.command(hidden=True)
def convert(

):
    print(f"convert. Yet to be implemented")

# Resize

'''

@app.command(
    short_help="Resize Images",
)
def resize(

        source: str = typer.Argument(
            ...,
            help="Source Directory containing Image files",
        ),

        destination: str = typer.Argument(
            ...,
            help="Destination Directory where processed images are stored",
        ),

        process: int = typer.Option(
            os.cpu_count(),
            "--process",
            "-p",
            min=1,
            max=100,
            clamp=True,
            help="Number of process to be used to parallelize the task. (Default is the Cores in machine)",
        ),

        scale_percentage: int = typer.Option(
            None,
            "--scale",
            "-s",
            min=1,
            max=100000,
            clamp=True,
            help="Scale image to the specified percentage",
        ),

        dimensions: str = typer.Option(
            None,
            "--dimensions",
            "-d",
            help="Scale image to the specified width and height in pixels - 'wxh' format  (Eg: 800x600)",
        ),

        height: int = typer.Option(
            None,
            "--height",
            "-h",
            min=1,
            max=1000000,
            clamp=True,
            help="Scale image to the specified height in pixels (width is required along with this)",
        ),

        width: int = typer.Option(
            None,
            "--width",
            "-w",
            min=1,
            max=1000000,
            clamp=True,
            help="Scale image to the specified width in pixels (height is required along with this)",
        ),

        interpolation: int = typer.Option(
            1,
            "--interpolation",
            "-i",
            min=1,
            max=16,
            clamp=True,
            rich_help_panel="Optional",
            help=f"Image Interpolation to use, (Integer as per open-cv), only 0,1,2,3,4,5,6,7,8,16 are accepted. \n {interpolation_flags} ",
        ),

        prefix: str = typer.Option(
            None,
            "--prefix",
            "-pre",
            rich_help_panel="Optional",
            help="String to be prefixed with converted files Eg:- scaled_ ",
        ),

        suffix: str = typer.Option(
            None,
            "--suffix",
            "-suf",
            rich_help_panel="Optional",
            help="String to be suffixed with converted files Eg:- _downscale",
        ),

):
    """
    Resize Images in batches based on the specified options.
    """

    resize_config = {
        "source_directory": source,
        "destination_directory": destination,
        "process": process,
        "scale": scale_percentage,
        "dimensions": dimensions,
        "height": height,
        "width": width,
        "interpolation": interpolation,
        "prefix": prefix,
        "suffix": suffix,
        "function": None,
        "is_valid": False,
        "use_key": None,
        "status": None
    }
    pprint(resize_config, expand_all=True, indent_guides=False)
    start_time = time.time()
    status = process_image(resize_config, "resize")
    end_time = time.time()
    print(status)
    print(f"The Process completed in {end_time-start_time:.10f} Seconds")

'''

# Annotate

'''



@app.command(
    short_help="Annotate Images",
)
def annotate(

        source: str = typer.Argument(
            ...,
            help="Source Directory containing Image files",
        ),

        destination: str = typer.Argument(
            ...,
            help="Destination Directory where processed images are stored",
        ),

        process: int = typer.Option(
            os.cpu_count(),
            "--process",
            "-p",
            min=1,
            max=100,
            clamp=True,
            help="Number of process to be used to parallelize the task. (Default is the Cores in machine)",
        ),

        text: str = typer.Option(
            None,
            "--text",
            "-t",
            help="Annotate image with the given text",
        ),

        colour: Tuple[int, int, int] = typer.Option(
            (255, 0, 0),
            "--colour",
            "-c",
            min=0,
            max=255,
            clamp=True,
            help="Colour to be used to annotate image specified as rgb value Eg: 255, 0, 0 (red)",
        ),

        origin: Tuple[int, int] = typer.Option(
            (100, 100),
            "--origin",
            "-o",
            help="A Tuple if x and y coordinate from which the text will start. ( X_AXIS Y_AXIS )",
        ),

        fontscale: float = typer.Option(
            1,
            "--fontscale",
            "-f",
            min=0,
            max=100,
            clamp=True,
            help="Font Size for the text",
        ),

        thickness: int = typer.Option(
            1,
            "--thickness",
            "-th",
            min=0,
            max=100,
            clamp=True,
            help="Font Thickness for the text",
        ),

        prefix: str = typer.Option(
            None,
            "--prefix",
            "-pre",
            rich_help_panel="Optional",
            help="String to be prefixed with converted files Eg:- scaled_ ",
        ),

        suffix: str = typer.Option(
            None,
            "--suffix",
            "-suf",
            rich_help_panel="Optional",
            help="String to be suffixed with converted files Eg:- _downscale",
        ),

):
    """
    Annotate Images in batches based on the specified options.
    """

    config = {
        "source_directory": source,
        "destination_directory": destination,
        "process": process,
        "text": text,
        "colour": colour,
        "origin": origin,
        "fontscale": fontscale,
        "thickness": thickness,
        "prefix": prefix,
        "suffix": suffix,
        "function": None,
        "is_valid": False,
        "use_key": None,
        "status": None
    }
    pprint(config, expand_all=True, indent_guides=False)
    start_time = time.time()
    status = process_image(config, "annotate")
    end_time = time.time()
    print(status)
    print(f"The Process completed in {end_time-start_time:.10f} Seconds")









'''


# Timestamp


'''
'''
@app.command(
    short_help="Timestamp Images",
)
def timestamp(

        source: str = typer.Argument(
            ...,
            help="Source Directory containing Image files",
        ),

        destination: str = typer.Argument(
            ...,
            help="Destination Directory where processed images are stored",
        ),

        process: int = typer.Option(
            os.cpu_count(),
            "--process",
            "-p",
            min=1,
            max=100,
            clamp=True,
            help="Number of process to be used to parallelize the task. (Default is the Cores in machine)",
        ),

        timetext: str = typer.Option(
            time.asctime(),
            "--timetext",
            "-t",
            help="Annotate image with the given Time Stamp",
        ),

        strftime: str = typer.Option(
            None,
            "--strftime",
            "-s",
            help="Format time with the given string (Eg: 'Time is : %Y-%m-%dT%H:%M:%S' )",
        ),

        colour: Tuple[int, int, int] = typer.Option(
            (255, 0, 0),
            "--colour",
            "-c",
            min=0,
            max=255,
            clamp=True,
            help="Colour to be used to annotate image specified as rgb value Eg: 255, 0, 0 (red)",
        ),

        origin: Tuple[int, int] = typer.Option(
            (-1, -1),
            "--origin",
            "-o",
            help="A Tuple if x and y coordinate from which the text will start. ( X_AXIS Y_AXIS )",
        ),

        fontscale: float = typer.Option(
            1,
            "--fontscale",
            "-f",
            min=0,
            max=100,
            clamp=True,
            help="Font Size for the text",
        ),

        thickness: int = typer.Option(
            1,
            "--thickness",
            "-th",
            min=0,
            max=100,
            clamp=True,
            help="Font Thickness for the text",
        ),


        prefix: str = typer.Option(
            None,
            "--prefix",
            "-pre",
            rich_help_panel="Optional",
            help="String to be prefixed with converted files Eg:- scaled_ ",
        ),

        suffix: str = typer.Option(
            None,
            "--suffix",
            "-suf",
            rich_help_panel="Optional",
            help="String to be suffixed with converted files Eg:- _downscale",
        ),

):
    """
    Annotate Images with timestamp in batches based on the specified options.
    """

    config = {
        "source_directory": source,
        "destination_directory": destination,
        "process": process,
        "timetext": timetext,
        "strftime": strftime,
        "colour": colour,
        "origin": origin,
        "fontscale": fontscale,
        "thickness": thickness,
        "prefix": prefix,
        "suffix": suffix,
        "function": None,
        "is_valid": False,
        "use_key": None,
        "status": None
    }
    pprint(config, expand_all=True, indent_guides=False)
    start_time = time.time()
    status = process_image(config, "timestamp")
    end_time = time.time()
    print(status)
    print(f"The Process completed in {end_time-start_time:.10f} Seconds")








'''
'''



def start() -> None:
    app()


if __name__ == "__main__":
    app()
