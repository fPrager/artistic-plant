from PIL import Image

MAX_SIZE= 800

def generateGif(inputs, output):
  frames = []
  for input in inputs:
    frame = Image.open(input)
    resizeTo = (MAX_SIZE, MAX_SIZE/frame.size[0] * frame.size[1])
    frame.thumbnail(resizeTo, Image.ANTIALIAS)
    frames.append(frame)
  frames[0].save(output, format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=300, loop=0)
