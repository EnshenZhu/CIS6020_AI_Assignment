from PIL import Image
import pandas as pd
import numpy as np

all_img_sample = {
    "sample1": {
        "input_img_path": r"./inputs/starcraft.png",
        "downsample_img_path": r"./downsampled/starcraft_ds.png",
        "output_bw_image_path": r"./outputs/starcraft_bw.png"
    },
    "sample2": {
        "input_img_path": r"./inputs/blizzard.png",
        "downsample_img_path": r"./downsampled/blizzard_ds.png",
        "output_bw_image_path": r"./outputs/blizzard_bw.png"
    }
}


def downsample(file_location, downsampled_save_path):
    image_file = Image.open(file_location)

    # down sample to quality 50 * 50 pixels
    size = 50, 50
    im_resized = image_file.resize(size, Image.Resampling.LANCZOS)
    im_resized.save(downsampled_save_path)


def rgb_to_black_and_white(file_location, downsampled_save_path, final_save_path):
    downsample(file_location, downsampled_save_path)

    col = Image.open(downsampled_save_path)
    gray = col.convert('L')
    output_bw = gray.point(lambda x: 0 if x < 128 else 255)
    output_bw.save(final_save_path)


# we are going to convert the black and white image into numpy array
def convert_to_pd(file_path):
    image = Image.open(file_path).convert("L")
    map_array = np.array(image.getdata()).reshape(50, 50)

    map_dataframe = pd.DataFrame(map_array)  # turn the original array into the pandas dataFrame
    map_dataframe = map_dataframe.replace(255, 1)  # replace all 255 into 1
    return map_dataframe


def work(input_path, temp_path, output_path):
    rgb_to_black_and_white(file_location=input_path,
                           downsampled_save_path=temp_path,
                           final_save_path=output_path)

    pixel_dataFrame = convert_to_pd(output_path)
    print(pixel_dataFrame)


if __name__ == "__main__":
    work(all_img_sample["sample1"]["input_img_path"], all_img_sample["sample1"]["downsample_img_path"],
         all_img_sample["sample1"]["output_bw_image_path"])
    
    # work(input_img_path2, downsample_path2, output_bw_image_path2)
