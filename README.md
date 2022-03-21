# H8-Detect
This repository stores the code for "Changes in Baselines of Hatespeech Detection with pretraining and Transformers",
a report done in the WiSe21/22 as part of a seminar on hatespeech detection.
*Caution this code requires a GPU to function, at various places we push to GPU explicitly if you wanna run this code on CPU you need to search for the .to("cuda") calls to fix that*

## How to use:
If one wants to see the performance of the model, the evaluate_model notebook is the place to start.
Everything one needs is already precalculated in the repository, so the evaluate_model is ready to run out of the box.
If one tries to recreate the training, you need to set path = None in the model_init function in Trainerclass in the train_model notebook.
This way it will load a default distilbert-uncased model otherwise it will load the pretrained model in results/model.
