import tempfile
import unittest
from pathlib import Path

from PIL import Image
from build import build


class GalleryTest(unittest.TestCase):
    def test_folders_images_escaping_and_removal(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'source'
            output = Path(temporary) / 'public'
            source.mkdir()
            Image.new('RGB', (20, 30)).save(source / 'profilbillede.png')
            product = source / '01 Strik & <test>'
            product.mkdir()
            photo = product / '01 Blå.jpg'
            Image.new('RGB', (20, 30)).save(photo)
            (product / 'notes.txt').write_text('Not a photo')
            (source / '02 Tom mappe').mkdir()
            build(source, output)
            html = (output / 'index.html').read_text()
            self.assertEqual(html.count('class="product"'), 1)
            self.assertIn('Strik &amp; &lt;test&gt;', html)
            self.assertIn('Blå', html)
            self.assertIn('1 variant</span>', html)
            with Image.open(output / 'billeder/1-1.jpg') as image:
                self.assertEqual(image.size, (20, 30))
                self.assertFalse(image.getexif())
            photo.unlink()
            build(source, output)
            self.assertFalse((output / 'billeder/1-1.jpg').exists())
            self.assertIn('snart strik', (output / 'index.html').read_text())


if __name__ == '__main__':
    unittest.main()
