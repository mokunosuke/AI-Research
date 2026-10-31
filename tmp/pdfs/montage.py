from PIL import Image
from pathlib import Path
files = sorted(Path('tmp/pdfs').glob('minimax-final-*.png'))
ims = [Image.open(p).convert('RGB') for p in files]
w = 350
out = Image.new('RGB', (710, 1800), '#d9dde4')
for i, im in enumerate(ims):
    im = im.resize((w, round(im.height * w / im.width)))
    out.paste(im, ((i % 2) * 360, (i // 2) * 600))
out.save('tmp/pdfs/contact-fixed.png')
