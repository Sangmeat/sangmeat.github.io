import tempfile
import unittest
from pathlib import Path

from PIL import Image
from build import build


class GalleryTest(unittest.TestCase):
    def test_largest_groups_first_without_captions(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'source'
            output = Path(temporary) / 'public'
            source.mkdir()
            image = Image.new('RGB', (20, 30))
            image.save(source / 'profilbillede.png')
            for name, count in [('01 Small', 1), ('02 Large', 3), ('03 Medium', 2), ('04 Equal', 2)]:
                folder = source / name
                folder.mkdir()
                for number in range(count):
                    image.save(folder / f'{number}.jpg')
                (folder / '.hidden.jpg').write_text('ignored')
                (folder / 'notes.txt').write_text('ignored')
            build(source, output)
            html = (output / 'index.html').read_text()
            for index, name in enumerate(['Large', 'Medium', 'Equal', 'Small']):
                self.assertIn(f'<a href="#produkt-{index}">{name}</a>', html)
                self.assertIn(f'<h2 id="produkt-{index}">{name}</h2>', html)
            self.assertNotIn('<figcaption', html)
            self.assertNotIn('Garn 1', html)

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
            self.assertIn('<a href="#produkt-0">Strik &amp; &lt;test&gt;</a>', html)
            self.assertNotIn('Tom mappe', html)
            self.assertIn('1 variant</span>', html)
            with Image.open(output / 'billeder/1-1.jpg') as image:
                self.assertEqual(image.size, (20, 30))
                self.assertFalse(image.getexif())
            photo.unlink()
            build(source, output)
            self.assertFalse((output / 'billeder/1-1.jpg').exists())
            self.assertIn('snart strik', (output / 'index.html').read_text())
            self.assertNotIn('class="overview"', (output / 'index.html').read_text())


if __name__ == '__main__':
    unittest.main()
