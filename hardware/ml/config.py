MODEL_NAME = 'audio_embeddings'
MODEL_LICENSE = 'Apache 2.0'

MODEL_META_DATA = {
    'id': '{}-tf-imagenet'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': '{} TensorFlow model trained on Audio Set'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}

local = "/Users/priyesh/Desktop/audio-classifier/assets"
DEFAULT_EMBEDDING_CHECKPOINT = local + "/vggish_model.ckpt"
DEFAULT_PCA_PARAMS = local + "/vggish_pca_params.npz"
DEFAULT_CLASSIFIER_MODEL = local + "/classifier_model.h5"
