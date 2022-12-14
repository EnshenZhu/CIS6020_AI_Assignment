import sys

from PIL import Image
import pandas as pd
import numpy as np

all_img_sample = {
    "originalimage1": {
        "input_img_path": r"./properties/inputs/originalimage1.png",
        "downsample_img_path": r"./properties/downsampled/originalimage1_DS.png",
        "output_bw_image_path": r"./properties/outputsImgPuzzle/puzzleImg1.png",
        "output_text_puzzle_path": r"./properties/outputsTextPuzzle/puzzleText1.txt"
    },
    "originalimage2": {
        "input_img_path": r"./properties/inputs/originalimage2.png",
        "downsample_img_path": r"./properties/downsampled/originalimage2_DS.png",
        "output_bw_image_path": r"./properties/outputsImgPuzzle/puzzleImg2.png",
        "output_text_puzzle_path": r"./properties/outputsTextPuzzle/puzzleText2.txt"
    }
}


def downsample(file_location, downsampled_save_path):
    image_file = Image.open(file_location)

    # down sample to quality 50 * 50 pixels
    size = 100, 100
    im_resized = image_file.resize(size, Image.Resampling.LANCZOS)
    im_resized.save(downsampled_save_path)


def rgb_to_black_and_white(file_location, downsampled_save_path, final_save_path):
    downsample(file_location, downsampled_save_path)

    col = Image.open(downsampled_save_path)
    gray = col.convert('L')
    output_bw = gray.point(lambda x: 255 if x < 128 else 0)  # RECALL: 255 is white; 0 is black
    output_bw.save(final_save_path)


# we are going to convert the black and white image into numpy array
def convert_to_pd(file_path):
    image = Image.open(file_path).convert("L")
    map_array = np.array(image.getdata()).reshape(100, 100)

    map_dataframe = pd.DataFrame(map_array)  # turn the original array into the pandas dataFrame
    map_dataframe = map_dataframe.replace(0, 1)  # replace all 0 into 1, which means this cell is filled in black
    map_dataframe = map_dataframe.replace(255, 0)  # replace all 255 into 0, which means this cell is not filled
    return map_dataframe


def handle_row(pd_data):
    row_ls = []  # create an empty row ls to record all rows' profile
    for row_idx in range(len(pd_data)):
        minor_ls = []
        counter = 0
        for column_idx in range(len(pd_data.iloc[row_idx, :])):

            if pd_data.iloc[row_idx, column_idx] == 1:

                # when there are continuous one, the counter accumulates
                counter += 1

            elif pd_data.iloc[row_idx, column_idx] == 0 and pd_data.iloc[row_idx, column_idx - 1] == 1:

                # when meet with zero after continues one, append the previous counter to the minor list
                # and make the counter back to zero and
                minor_ls.append(counter)
                counter = 0

        row_ls.append(minor_ls)

    return row_ls


def handle_column(pd_data):
    colunn_ls = []  # create an empty column ls to record all columns' profile

    for column_idx in range(len(pd_data.iloc[0, :])):
        minor_ls = []
        counter = 0
        for row_idx in range(len(pd_data.iloc[:, column_idx])):
            if pd_data.iloc[row_idx, column_idx] == 1:

                # when there are continuous one, the counter accumulates
                counter += 1

            elif pd_data.iloc[row_idx, column_idx] == 0 and pd_data.iloc[row_idx - 1, column_idx] == 1:

                # when meet with zero after continues one, append the previous counter to the minor list
                # and make the counter back to zero
                minor_ls.append(counter)
                counter = 0

        colunn_ls.append(minor_ls)

    return colunn_ls


def text_generation(pd_data, txt_output_path):
    row_profile = handle_row(pd_data)
    column_profile = handle_column(pd_data)

    with open(txt_output_path, "w") as f:
        f.write("The row profile is:" + "\n")
        f.write(str(row_profile))
        f.write("\n")
        f.write("The column profile is:" + "\n")
        f.write(str(column_profile))

    # print(len(row_profile))
    # print(len(column_profile))


def work(input_path, temp_path, output_path):
    rgb_to_black_and_white(file_location=input_path,
                           downsampled_save_path=temp_path,
                           final_save_path=output_path)

    pixel_dataFrame = convert_to_pd(output_path)
    return pixel_dataFrame


if __name__ == "__main__":
    filename = sys.argv[1]
    matrix = work(all_img_sample[filename]["input_img_path"], all_img_sample[filename]["downsample_img_path"],
                  all_img_sample[filename]["output_bw_image_path"])
    text_generation(matrix, all_img_sample[filename]["output_text_puzzle_path"])

    # work(input_img_path2, downsample_path2, output_bw_image_path2)
