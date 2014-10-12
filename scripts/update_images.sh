mkdir tmp_images
cp images/* tmp_images/
git checkout gh-pages
mv tmp_images/* images/
rmdir tmp_images
