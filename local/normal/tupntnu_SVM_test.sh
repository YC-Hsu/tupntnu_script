if [ $# != 3 ]; then
	echo "Usage: $0 [options] <phones-txt> <train-dir> <test-dir>";
	echo "e.g.: $0 data/lang/phones.txt \\"
	echo "\texp/PLFeats_train "
	echo "\texp/PLFeats_test "
	echo "options: "
	echo "				"
	exit 1;
fi

phones_txt=$1
train_dir=$2
test_dir=$3

echo "Start to SVM testing ... "
								
python local/py_code/SVM_predict.py $phones_txt $train_dir/pickle $test_dir/phone_level_corpus.txt || exit 1;

echo "Done."