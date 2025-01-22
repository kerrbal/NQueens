from PIL import Image
from PIL import ImageDraw

def create_board(file_name, board_length, queen_coordinates):

    color1 = (238,238,210)
    color2 = (118,150,86)

    queen = Image.open(r"masked_queen.png")
    multiplier = 500 // board_length
    queen = queen.resize((multiplier, multiplier))

    actual_queen = queen.copy()

    the_image = Image.new("RGBA", (500, 500), (255, 255, 255, 255))
    chess_board = ImageDraw.Draw(the_image, "RGBA")
    multiplier = 500 // board_length
    for i in range(board_length):
        pixel_x = multiplier*i
        if i % 2 == 0:
            color = color1
        else:
            color = color2
        for j in range(board_length):
            pixel_y = multiplier*j
            if color == color1:
                color = color2
            else:
                color = color1
            chess_board.rectangle(xy = [(pixel_x, pixel_y), (pixel_x + multiplier, pixel_y + multiplier)], fill = color, width = 0)
            if (i, j) in queen_coordinates:
                the_image.paste(actual_queen, (pixel_x, pixel_y), actual_queen)

    the_image.save(file_name)

