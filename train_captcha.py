import os
import tensorflow as tf
from utils import PrepareData
from image_ocr_model import CnnRnnCtcOrc

tf.flags.DEFINE_string(name="image_path", default="/usr/projects/nlp/imageRecognition/data/china_tax.txt", help="image path which had prepared")
tf.flags.DEFINE_string(name="char_path", default="/usr/projects/nlp/imageRecognition/data/char_index.txt", help="how many chars to identify")
tf.flags.DEFINE_string(name="mode", default="train", help="train, test")
tf.flags.DEFINE_float(name="ratio", default=0.9, help="train ratio of all data")
tf.flags.DEFINE_integer(name="max_captcha_len", default=5, help="max captcha len")
tf.flags.DEFINE_integer(name="num_lstm_hidden", default=64, help="multi lstm num hidden")
tf.flags.DEFINE_integer(name="batch_size", default=24, help="batch size of train data ")
tf.flags.DEFINE_integer(name="epoch", default=200, help="maximum epochs")
tf.flags.DEFINE_float(name="learning_rate", default=0.01, help="inital learning rate")
tf.flags.DEFINE_string(name="export_dir", default="/usr/projects/nlp/imageRecognition/data/ocr", help="inital learning rate")

FLAGS = tf.flags.FLAGS


def main(_):
    if os.path.exists(FLAGS.export_dir):
        raise Exception("export_dir {} has exist! please choose another export_dir".format(FLAGS.export_dir))
    pd = PrepareData(FLAGS.image_path, FLAGS.ratio, FLAGS.char_path, FLAGS.max_captcha_len)
    train_x, train_y, test_x, test_y = pd.train_and_test_data
    model = CnnRnnCtcOrc(FLAGS.max_captcha_len, 37, FLAGS.num_lstm_hidden)
    model.train(train_x, train_y, FLAGS)
    model.test(test_x, test_y, FLAGS)
    model.release(FLAGS.export_dir)


if __name__ == "__main__":
    tf.app.run(main)
