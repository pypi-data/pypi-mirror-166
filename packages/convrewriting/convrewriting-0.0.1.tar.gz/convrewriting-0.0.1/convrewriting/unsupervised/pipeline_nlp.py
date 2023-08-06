from smartpipeline.pipeline import Pipeline
from smartpipeline.stage import Stage, DataItem
import logging
import os
from convrewriting.unsupervised.source import UttFileSource
from convrewriting.unsupervised.topic import KeepContext
from convrewriting.unsupervised.topic import FirstTopic
from convrewriting.unsupervised.topic import TopicShift

class PrintItem(Stage):
    def process(self, item: DataItem) -> DataItem:
        print(item)
        return item


def rewrite_context():
    file_path = os.path.join(os.path.dirname(__file__), '../data/datasets', 'test_set.tsv')
    pipeline = Pipeline().set_source(
        UttFileSource(file_path)
    # ).append_stage(
    #     "print item",
    #     PrintItem()
    ).append_stage(
        "context",
        KeepContext()
    ).append_stage(
        "print rewritten",
        PrintItem()
    )

    print("Printing Context Rewrite:")

    for item in pipeline.run():
        logging.info(f'Processed document: {item}')

    print()


def rewrite_first_topic():
    file_path = os.path.join(os.path.dirname(__file__), '../data/datasets', 'test_set.tsv')
    pipeline = Pipeline().set_source(
        UttFileSource(file_path)
        # ).append_stage(
        #     "print item",
        #     PrintItem()
        ).append_stage(
            "first topic",
            FirstTopic()
        ).append_stage(
            "print rewritten",
            PrintItem()
    )

    print("Printing First Topic Rewrite:")

    for item in pipeline.run():
        logging.info(f'Processed document: {item}')

    print()


def rewrite_topic_shift():
    file_path = os.path.join(os.path.dirname(__file__), '../data/datasets', 'test_set.tsv')
    pipeline = Pipeline().set_source(
        UttFileSource(file_path)
        # ).append_stage(
        #     "print item",
        #     PrintItem()
        ).append_stage(
            "topic shift",
            TopicShift()
        ).append_stage(
            "print rewritten",
            PrintItem()
    )

    print("Printing Topics Shift Rewrite:")

    for item in pipeline.run():
        logging.info(f'Processed document: {item}')

    print()


if __name__ == "__main__":
    rewrite_context()
    rewrite_first_topic()
    rewrite_topic_shift()


