if [ $# != 2 ]; then
	echo "Usage: $0 [options] <phones-txt> <dev-dir> ";
	echo "e.g.: $0 data/lang/phones.txt \\"
	echo "\texp/PLFeats_dev "
	echo "options: "
	echo "				"
	exit 1;
fi

phones_txt=$1
dev_dir=$2

echo "Start to make GOP threshold ... "

python local/py_code/GOP_make_threshold.py \
	$phones_txt $dev_dir/phone_level_corpus.txt $dev_dir/phone_level_corpus_gop.txt || exit 1;
	
echo "Done."