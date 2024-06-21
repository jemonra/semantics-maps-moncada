export LLAVA_PYTHON_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/LLaVA/
export LLAMA_MODEL_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Models/llama-7b/
export LLAVA_MODEL_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Models/LLaVA-7B-v0/

python $LLAVA_PYTHON_PATH/llava/model/apply_delta.py \
    --base $LLAMA_MODEL_PATH \
    --target $LLAVA_MODEL_PATH \
    --delta liuhaotian/LLaVA-7b-delta-v0