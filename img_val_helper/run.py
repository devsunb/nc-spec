import argparse
import logging

from img_val_helper.helper import Helper

logger = logging.getLogger('img_val_helper')


def run():
    option = get_option()
    setup_logger(option.log_level)
    with Helper(option.input, option.output) as h:
        h.run()


def get_option():
    parser = argparse.ArgumentParser(description='Image validation helper')
    parser.add_argument('input', type=str, help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file path (ends with .xlsx)')
    parser.add_argument('-l', '--log-level', type=str,
                        default='INFO', help='Log level')
    return parser.parse_args()


def setup_logger(log_level):
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


if __name__ == '__main__':
    run()
