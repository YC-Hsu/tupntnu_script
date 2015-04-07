
if [ $# != 5 ]; then
   echo "Usage: $0 [options] <phones-txt> <ali-dir> <nnforward-exp> <feats-ark> <corpus-dir>";
   echo "e.g.: $0 data/lang/phones.txt \\"
   echo "\texp/tri3a_MPDN4H1024_test_ali \\"
   echo "\texp/tri3a_mfcc_pitch_dnn_nd4_hd1024 \\"
   echo "\tmfcc_pitch/raw_mfcc_pitch_test.1.ark \\"
   echo "\texp/PLFeats_test "
   echo "options: "
   echo "				"
   exit 1;
fi

phones_txt=$1
ali_dir=$2
nnforward_exp=$3
feats_ark=$4
corpus_dir=$5

mkdir -p $corpus_dir
mkdir -p $corpus_dir/tmp

gunzip -c $ali_dir/ali.*.gz > $corpus_dir/tmp/ali.txt
show-transitions $phones_txt $ali_dir/final.mdl > $corpus_dir/tmp/state_and_phone.txt

nnet-forward --no-softmax=true --prior-scale=1.0 \
			--feature-transform=$nnforward_exp/final.feature_transform \
			--class-frame-counts=$nnforward_exp/ali_train_pdf.counts \
			--use-gpu="no" $nnforward_exp/final.nnet \
			ark:$feats_ark ark,t:$corpus_dir/tmp/feats_nnf.txt 

python local/py_code/Create_phone_level_feats.py data/lang/phones.txt $corpus_dir/tmp/state_and_phone.txt \
													$corpus_dir/tmp/ali.txt $corpus_dir/tmp/feats_nnf.txt \
													$corpus_dir/phone_level_feats.txt
rm -rf $corpus_dir/tmp

python local/py_code/Create_phone_level_corpus.py $corpus_dir/phone_level_feats.txt $corpus_dir/phone_level_corpus.txt
