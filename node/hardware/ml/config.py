import os

MODEL_NAME = 'audio_embeddings'
MODEL_LICENSE = 'Apache 2.0'

MODEL_META_DATA = {
    'id': '{}-tf-imagenet'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': '{} TensorFlow model trained on Audio Set'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}

DEFAULT_EMBEDDING_CHECKPOINT = os.path.join("assets","vggish_model.ckpt")
DEFAULT_PCA_PARAMS = os.path.join("assets","vggish_pca_params.npz")
DEFAULT_CLASSIFIER_MODEL = os.path.join("assets","classifier_model.h5")
