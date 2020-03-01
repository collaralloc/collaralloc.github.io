## kaldi中文实例运行步骤（清华语料库）

> 参考博客
>
> [第三十章 kaldi 中文ASR实例](https://shichaog1.gitbooks.io/hand-book-of-speech-enhancement-and-recognition/content/chapter30.html)
>
> [Kaldi学习笔记（三）——运行thchs30（清华大学中文语料库）](https://blog.csdn.net/snowdroptulip/article/details/78943748)
>
>[基于kaldi的在线中文识别，online的操作介绍](http://www.voidcn.com/article/p-puqopdsz-ym.html)//这个可能应该是原版
> [Kaldi学习笔记（四）——thchs30中文在线识别](https://blog.csdn.net/snowdroptulip/article/details/78950038)//该博客略有问题,应该是参考上一篇是囫囵弄过来的
>
> [kaldi中文语音识别平台的搭建——运行thchs30](https://blog.csdn.net/Alexwym/article/details/82839495)
>
> [kaldi训练thchs30详细步骤](https://blog.csdn.net/Allyli0022/article/details/78355687)//问题同上
>
> 

### 原始数据下载

[thchs30数据集下载链接](http://www.openslr.org/18/)

**Downloads (use a mirror closer to you):** 
[ data_thchs30.tgz ](http://www.openslr.org/resources/18/data_thchs30.tgz) [6.4G]   ( speech data and transcripts)   Mirrors: [ [China](http://cn-mirror.openslr.org/resources/18/data_thchs30.tgz)]

[ test-noise.tgz ](http://www.openslr.org/resources/18/test-noise.tgz) [1.9G]   (   standard 0db noisy test data)   Mirrors: [ [China ](http://cn-mirror.openslr.org/resources/18/test-noise.tgz)]

[ resource.tgz ](http://www.openslr.org/resources/18/resource.tgz) [24M]   (   supplementary resources, incl. lexicon for training data, noise samples)   Mirrors: [ [China](http://cn-mirror.openslr.org/resources/18/resource.tgz)  ]

下载指令`wget http://www.openslr.org/resources/18/data_thchs30.tgz`

~~后台自动下载`nohup wget http://www.openslr.org/resources/18/data_thchs30.tgz &~~`

~~查看进程 `ps -aux`~~  (这个方法不太好使)

后台自动下载
```shell
wget -b http://www.openslr.org/resources/18/data_thchs30.tgz
备注： 你可以使用以下命令来察看下载进度： tail -f wget-log
```

依次下载三个压缩文件，解压到自己指定的目录

解压命令`tar -xvzf data_thchs30.tgz -C ./thdata`

### 训练生成模型

该example在kaildi的egs(样例)目录的thchs30中：

```
~/kaldi/egs/thchs30/s5
```

阅读cmd.sh的注释后可知，不使用联机模式的话，需要使cmd.sh按如下方式更改，以使用pc进行编译
cmd.sh源文件
```shell
# you can change cmd.sh depending on what type of queue you are using.
# If you have no queueing system and want to run on a local machine, you
# can change all instances 'queue.pl' to run.pl (but be careful and run
# commands one by one: most recipes will exhaust the memory on your
# machine).  queue.pl works with GridEngine (qsub).  slurm.pl works
# with slurm.  Different queues are configured differently, with different
# queue names and different ways of specifying things like memory;
# to account for these differences you can create and edit the file
# conf/queue.conf to match your queue's configuration.  Search for
# conf/queue.conf in http://kaldi-asr.org/doc/queue.html for more information,
# or search for the string 'default_config' in utils/queue.pl or utils/slurm.pl.
#联机的
#export train_cmd=queue.pl
#export decode_cmd="queue.pl --mem 4G"
#export mkgraph_cmd="queue.pl --mem 8G"
#export cuda_cmd="queue.pl --gpu 1"
#使用本地编译
export train_cmd=run.pl
export decode_cmd="run.pl --mem 4G"
export mkgraph_cmd="run.pl --mem 8G"
export cuda_cmd="run.pl --gpu 1"
```
修改run.sh文件,修改CPU内核数`n`，以及本地语料地址`thchs`：
```shell
#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.
. ./path.sh

H=`pwd`  #exp home
#n=8      #parallel jobs
n=2
#corpus and trans directory
#thchs=/nfs/public/materials/data/thchs30-openslr
thchs=~/thdata/data_thchs30
#you can obtain the database by uncommting the following lines
```
最后**运行run.sh**，等待aligning(校准)和estimate(估计)，等所有文件都调整好了，模型也就好了。

> 四、运行sh run.sh
>
> 五、等待训练，训练过程中可能会出现一些异常，当时还担心是数据没有下载完，等到后面的测试结果出来才发现，这些异常都算正常。
>
> 六、回到src目录下，运行：make ext，这个过程也耗费了四五个小时，我没耐心等待，后来直接测试了，也没啥影响。
>
> 运行完毕后，src下回出现onlinebin，进去后会有online-wav-gmm-decode-faster和online-gmm-decode-faster，前者测试wav文件，后者测试麦克风输入的音频。
>

### 安装portaudio

```shell
#进入kaldi的tools目录下，运行./install_portaudio.sh
cd ~/kaldi/tools
./install_portaudio.sh
#进入src目录下，执行make ext
cd ../src
make ext
```

9.去egs下，打开voxforge，里面有个online_demo，直接考到thchs30下。在online_demo里面建2个文件夹online-data  work,在online-data下建两个文件夹audio和models，audio下放你要回放的wav，models建个文件夹tri1，把s5下的exp下的tri1下的final.mdl和35.mdl（final.mdl是快捷方式）和 s5下的exp下的tri1下的graph_word里面的words.txt,和HCLG.fst，都考到models的tri1下。

其中，final.mdl是训练出来的模型，words.txt是字典，和HCLG.fst是有限状态机。

将**egs/voxforge**中的online_demo拷贝到egs/thchs30/

```shell
cd ~/kaldi/egs
mkdir thchs30/online_demo
cp voxforge/online_demo/*  thchs30/online_demo
cd thchs30
cp -a s5/exp/tri1/final.mdl online_demo/online-data/models/tri1
cp -a s5/exp/tri1/35.mdl online_demo/online-data/models
cp -a s5/exp/tri1/graph_word/words.txt online_demo/online-data/models
cp -a s5/exp/tri1/graph_word/HCLG.fst online_demo/online-data/models
```

修改脚本 修改online_demo 下的run.sh

```shell
#!/bin/bash

# Copyright 2012 Vassil Panayotov
# Apache 2.0

# Note: you have to do 'make ext' in ../../../src/ before running this.

# Set the paths to the binaries and scripts needed
KALDI_ROOT=`pwd`/../../..
export PATH=$PWD/../s5/utils/:$KALDI_ROOT/src/onlinebin:$KALDI_ROOT/src/bin:$PATH

data_file="online-data"
data_url="http://sourceforge.net/projects/kaldi/files/online-data.tar.bz2"

# Change this to "tri2a" if you like to test using a ML-trained model
ac_model_type=tri1

# Alignments and decoding results are saved in this directory(simulated decoding only)
decode_dir="./work"

# Change this to "live" either here or using command line switch like:
# --test-mode live
test_mode="simulated"

. parse_options.sh

ac_model=${data_file}/models/$ac_model_type
trans_matrix=""
audio=${data_file}/audio
<<!EOF!
if [ ! -s ${data_file}.tar.bz2 ]; then
    echo "Downloading test models and data ..."
    wget -T 10 -t 3 $data_url;

    if [ ! -s ${data_file}.tar.bz2 ]; then
        echo "Download of $data_file has failed!"
        exit 1
    fi
fi
!EOF!

if [ ! -d $ac_model ]; then
    echo "Extracting the models and data ..."
    tar xf ${data_file}.tar.bz2
fi


if [ -s $ac_model/matrix ]; then
    trans_matrix=$ac_model/matrix
fi

case $test_mode in
    live)
        echo
        echo -e "  LIVE DEMO MODE - you can use a microphone and say something\n"
        echo "  The (bigram) language model used to build the decoding graph was"
        echo "  estimated on an audio book's text. The text in question is"
        echo "  \"King Solomon's Mines\" (http://www.gutenberg.org/ebooks/2166)."
        echo "  You may want to read some sentences from this book first ..."
        echo
        online-gmm-decode-faster --rt-min=0.5 --rt-max=0.7 --max-active=4000 \
           --beam=12.0 --acoustic-scale=0.0769 $ac_model/final.mdl $ac_model/HCLG.fst \
           $ac_model/words.txt '1:2:3:4:5' $trans_matrix;;

    simulated)
        echo
        echo -e "  SIMULATED ONLINE DECODING - pre-recorded audio is used\n"
        echo "  The (bigram) language model used to build the decoding graph was"
        echo "  estimated on an audio book's text. The text in question is"
        echo "  \"King Solomon's Mines\" (http://www.gutenberg.org/ebooks/2166)."
        echo "  The audio chunks to be decoded were taken from the audio book read"
        echo "  by John Nicholson(http://librivox.org/king-solomons-mines-by-haggard/)"
        echo
        echo "  NOTE: Using utterances from the book, on which the LM was estimated"
        echo "        is considered to be \"cheating\" and we are doing this only for"
        echo "        the purposes of the demo."
        echo
        echo "  You can type \"./run.sh --test-mode live\" to try it using your"
        echo "  own voice!"
        echo
        mkdir -p $decode_dir
        # make an input .scp file
        > $decode_dir/input.scp
        for f in $audio/*.wav; do
            bf=`basename $f`
            bf=${bf%.wav}
            echo $bf $f >> $decode_dir/input.scp
        done
        online-wav-gmm-decode-faster --verbose=1 --rt-min=0.8 --rt-max=0.85\
            --max-active=4000 --beam=12.0 --acoustic-scale=0.0769 \
            scp:$decode_dir/input.scp $ac_model/final.mdl $ac_model/HCLG.fst \
            $ac_model/words.txt '1:2:3:4:5' ark,t:$decode_dir/trans.txt \
            ark,t:$decode_dir/ali.txt $trans_matrix;;

    *)
        echo "Invalid test mode! Should be either \"live\" or \"simulated\"!";
        exit 1;;
esac

# Estimate the error rate for the simulated decoding
if [ $test_mode == "simulated" ]; then
    # Convert the reference transcripts from symbols to word IDs
    sym2int.pl -f 2- $ac_model/words.txt < $audio/trans.txt > $decode_dir/ref.txt

    # Compact the hypotheses belonging to the same test utterance
    cat $decode_dir/trans.txt |\
        sed -e 's/^\(test[0-9]\+\)\([^ ]\+\)\(.*\)/\1 \3/' |\
        gawk '{key=$1; $1=""; arr[key]=arr[key] " " $0; } END { for (k in arr) { print k " " arr[k]} }' > $decode_dir/hyp.txt

   # Finally compute WER
   compute-wer --mode=present ark,t:$decode_dir/ref.txt ark,t:$decode_dir/hyp.txt
fi


```

