#!/bin/bash
l=None
p=NONE

echo "$0 $@"  # Print the command line for logging

[ -f path.sh ] && . ./path.sh; 

while [[ $# > 3 ]]
do
key="$1"

case $key in
    -l)
    l="$2"
    shift
    ;;
    -p)
    p="$2"
    shift
    ;;
    *)
            # unknown option
    ;;
esac
shift
done

if [ $# != 3 ]; then
   echo "Usage: $0 [options] <train-dir> <corpus-info> <corpus-dir>";
   echo "e.g.: $0 data/MS_L1_T /mnt/corpus/TUP_NTNU/MS.info /mnt/corpus/TUP_NTNU/MS_WAV "
   echo "options: "
   echo -e '\t-l\t1 : native language learner, 2 : other language learner (default = None) . '
   echo -e '\t-p\tPronunciation True or False (default = None) . '
   echo "				"
   exit 1;
fi

train_dir=$1
corpus_info=$2
corpus_dir=$3


mkdir -p $train_dir

echo "prepare TUP_NTNU $train_dir ..."
echo "prepare file $train_dir/text ..."
python local/py_code/tupntnu_make_text.py -l $l -p $p $corpus_dir $corpus_info $train_dir/text
echo "prepare file $train_dir/wav.scp ..."
python local/py_code/tupntnu_make_wavscp.py $train_dir/text $train_dir/wav.scp $corpus_dir
echo "prepare file utt2spk ..."
python local/py_code/tupntnu_make_utt2spk.py $train_dir
echo "prepare file spk2utt ..."
utils/utt2spk_to_spk2utt.pl $train_dir/utt2spk > $train_dir/spk2utt
utils/fix_data_dir.sh $train_dir

echo 'Done.'
