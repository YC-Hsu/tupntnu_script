


if [ $# != 2 ]; then
   echo "Usage: $0 [options] <src-dir> <target-dir>";
   echo "e.g.: $0 local/dict data/local/dict"
   echo "options: "
   echo "				"
   exit 1;
fi

src_dir=$1
target_dir=$2

mkdir -p $target_dir

echo "prepare $target_dir ..."
for x in extra_questions.txt lexicon.txt nonsilence_phones.txt optional_silence.txt silence_phones.txt; do 
	echo "prepare file $x ..."
	cp $src_dir/$x $target_dir/$x
done
