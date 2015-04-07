if [ $# != 3 ]; then
	echo "Usage: $0 [options] <phones-txt> <dev-dir> <test-dir>";
	echo "e.g.: $0 data/lang/phones.txt \\"
	echo "\texp/PLFeats_dev "
	echo "\texp/PLFeats_test "
	echo "options: "
	echo "				"
	exit 1;
fi

phones_txt=$1
dev_dir=$2
test_dir=$3

echo "Start to GOP testing ... "
	
python local/py_code/GOP_predict.py \
	$phones_txt $dev_dir/phone_level_corpus_gop.txt $test_dir/phone_level_corpus.txt || exit 1;
	
echo "Done."