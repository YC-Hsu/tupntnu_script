if [ $# != 2 ]; then
	echo "Usage: $0 [options] <phones-txt> <train-dir>";
	echo "e.g.: $0 data/lang/phones.txt \\"
	echo "\texp/PLFeats_train "
	echo "options: "
	echo "				"
	exit 1;
fi

phones_txt=$1
train_dir=$2

mkdir -p $train_dir/pickle
mkdir -p $train_dir/tmp

echo "Start to SVM training ... "

python local/py_code/SVM_train2pickle.py $phones_txt $train_dir/phone_level_corpus.txt \
								$train_dir/tmp/corpus.tmp $train_dir/pickle || exit 1;
								

rm -rf $train_dir/tmp

echo "Done."