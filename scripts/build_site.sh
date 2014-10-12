mkdir tmp_files
cp images/* tmp_files/
cp README.md tmp_files/
git checkout gh-pages
mv tmp_files/README.md _includes/
mv tmp_files/* images/
rmdir tmp_files
