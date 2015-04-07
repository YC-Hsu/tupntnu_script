


if [ $# != 1 ]; then
   echo "Usage: $0 [options] <lang-dir>";
   echo "e.g.: $0 data/lang "
   echo "options: "
   echo "				"
   exit 1;
fi

lang_dir=$1


echo "prepare $lang_dir/G.fst ..."
python local/py_code/tupntnu_make_Gfst_MS.py $lang_dir/words.txt $lang_dir

cat $lang_dir/G.txt | fstcompile --isymbols=$lang_dir/words.txt --osymbols=$lang_dir/words.txt --keep_isymbols=false --keep_osymbols=false | fstrmepsilon > $lang_dir/G.fst

#utils/validate_lang.pl $lang_dir