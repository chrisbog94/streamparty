from PIL import Image
import os, math, time
max_frames_row = 1
frames = []
tile_width = 0
tile_height = 0

spritesheet_width = 0
spritesheet_height = 0

files = os.listdir("./back/")
files.sort()

for current_file in files :
    try:
        with Image.open("./back/" + current_file) as im :
            frames.append(im.getdata())
    except:
        print(current_file + " is not a valid image")

tile_width = 3400
tile_height = 220

if len(frames) > max_frames_row :
    spritesheet_width = tile_width * max_frames_row
    required_rows = math.ceil(len(frames)/max_frames_row)
    spritesheet_height = tile_height * required_rows
else:
    spritesheet_width = tile_width*len(frames)
    spritesheet_height = tile_height
    
print(spritesheet_height)
print(spritesheet_width)

spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

for current_frame in frames :
    top = tile_height * math.floor((frames.index(current_frame))/max_frames_row)
    left = tile_width * (frames.index(current_frame) % max_frames_row)
    bottom = top + tile_height
    right = left + tile_width
    
    box = (left,top,right,bottom)
    box = [int(i) for i in box]
    print(box)
    print (tile_width, tile_height)
    cut_frame = current_frame
    
    spritesheet.paste(cut_frame, box)
    
spritesheet.save("spritesheet" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png", "PNG")