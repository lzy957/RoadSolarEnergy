#!/bin/bash

# Image and model names
#Root_IMG=$(dirname "$PWD")
#TEST_IMG=/datadrive/urbanplayground/Streetview/ALBSV/ALBSV1
TEST_IMG=$NFilePath
echo "$TEST_IMG"
MODEL_PATH=ade20k-resnet50dilated-ppm_deepsup
#RESULT_PATH=/datadrive/urbanplayground/Streetview/ALBSV/Segpic/ALBSV1_p
RESULT_PATH=$FilePath/SegPic/$nfilename

ENCODER=$MODEL_PATH/encoder_epoch_20.pth
DECODER=$MODEL_PATH/decoder_epoch_20.pth

# Download model weights and image
if [ ! -e $MODEL_PATH ]; then
  mkdir $MODEL_PATH
fi
if [ ! -e $ENCODER ]; then
  wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$ENCODER
fi
if [ ! -e $DECODER ]; then
  wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$DECODER
fi
#if [ ! -e $TEST_IMG ]; then
#  wget -P $RESULT_PATH http://sceneparsing.csail.mit.edu/data/ADEChallengeData2016/images/validation/$TEST_IMG
#fi

# Inference
python3 -u test.py \
  --imgs $TEST_IMG \
  --cfg config/ade20k-resnet50dilated-ppm_deepsup.yaml \
  DIR $MODEL_PATH \
  TEST.result $RESULT_PATH \
  TEST.checkpoint epoch_20.pth
