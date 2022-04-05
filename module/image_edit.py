from PIL import Image


def overpx_edit(cut_img, basic_file, base_floader, eposide_title, la, n):

    back_img = Image.new('RGB', (0, int(cut_img.size[1]) / 2), (255, 255, 255))
    back_second_img = Image.new('RGB', (0, int(cut_img.size[1]) / 2), (255, 255, 255))
    back_img.paste(cut_img, 0, cut_img.size[1] / 2)
    back_second_img.paste(cut_img, 0, cut_img.size[1])
    back_img.save(f"{basic_file}/{base_floader}/{eposide_title}/{la}/{n - 1}.jpg")
    back_second_img.save(f"{basic_file}/{eposide_title}/{la}/{n}.jpg")

    return None


def img_add(img_arr):
    new_img = None
    for i in range(len(img_arr) - 1):
        if i == 0:
            first_img = Image.open(img_arr[i])
        else:
            first_img = new_img
        second_img = Image.open(img_arr[i + 1])
        first_img_size = first_img.size
        second_img_size = second_img.size
        new_img = Image.new('RGB', (first_img_size[0], first_img_size[1] + (second_img_size[1])), (255, 255, 255))
        new_img.paste(first_img, (0, 0))
        new_img.paste(second_img, (0, first_img_size[1]))

    return new_img
