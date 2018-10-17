import os
import itertools
from dataflows import Flow
from . import dump_to_path, load


class checkpoint(Flow):

    def __init__(self, checkpoint_name, checkpoint_path='.checkpoints', steps=None, resources=None):
        if not steps:
            steps = []
        super().__init__(*steps)
        self.checkpoint_path = os.path.join(checkpoint_path, checkpoint_name)
        self.resources = resources

    def _preprocess_chain(self):
        checkpoint_package_json_path = os.path.join(self.checkpoint_path, 'datapackage.json')
        if os.path.exists(checkpoint_package_json_path):
            print('using checkpoint data from {}'.format(self.checkpoint_path))
            return load(checkpoint_package_json_path, resources=self.resources),
        else:
            print('saving checkpoint to: {}'.format(self.checkpoint_path))
            return itertools.chain(self.chain, (dump_to_path(self.checkpoint_path, resources=self.resources),))

    def handle_flow_checkpoint(self, parent_chain):
        self.chain = itertools.chain(self.chain, parent_chain)
        return [self]
