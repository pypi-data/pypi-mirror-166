"""
Mosaik API to minimalistic reactive power market model.

Author: Thomas Wolgast <thomas.wolgast@uol.de>

"""

import json
import logging
from typing import Any, Dict

import mosaik_api

from .meta import META
from .model import QMarketModel

# import qmarket
LOG = logging.getLogger(__name__)


class SimQMarket(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "QMarketModel_"
        self.model_name = "Model_qmarket"
        self.entities = {}  # Maps EIDs to model indices in self.simulator

    def init(self, sid, **sim_params):
        self.step_size = sim_params.get("step_size", 900)
        if sim_params.get("eid_prefix", None) is not None:
            self.eid_prefix = sim_params["eid_prefix"]
        return self.meta

    def create(self, num, model, **model_params):
        # Only one market entity possible
        assert num == 1
        assert self.entities == {}

        idx = 0
        eid = f"{self.eid_prefix}{idx}"
        self.entities[eid] = idx
        entities = [{"eid": eid, "type": model}]
        self.simulator = QMarketModel(model_params)

        return entities

    def step(
        self,
        time: int,
        inputs: Dict[str, Dict[str, Dict[str, Any]]],
        max_advance: int = 0,
    ) -> int:

        if time == 0:
            LOG.debug("Skipping first step;")
            return self.step_size // 4

        if "grid_state" in inputs["QMarketModel_0"]:
            # Json formatted grid is ugly in the logs ...
            grid_state = inputs["QMarketModel_0"].pop("grid_state")
            inputs["QMarketModel_0"]["grid_state"] = {
                "Grid JSON": (
                    "This is just a placeholder ... "
                    "the grid is actually here"
                )
            }  # placeholder
            LOG.debug(f"At step {time} received inputs: {inputs}")
            inputs["QMarketModel_0"]["grid_state"] = grid_state
        else:
            LOG.debug(f"At step {time} received inputs: {inputs}")

        # There is only one Q Market
        for model_inputs in inputs.values():
            for attr, src_ids in model_inputs.items():
                if attr == "grid_state":
                    assert len(src_ids) == 1
                    self.simulator.set_grid_state(list(src_ids.values())[0])
                elif attr == "q_offers":
                    q_offers = deserialize_q_offers(src_ids)
                    self.simulator.q_offers = q_offers

        self.simulator.step()

        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta["models"]["QMarketModel"]["attrs"]:
                    raise ValueError(f"Unknown output attribute: {attr}")
                if attr in data[eid]:
                    continue
                if attr == "q_accept":
                    value = dict(self.simulator.q_accept)
                else:
                    value = getattr(self.simulator, attr)
                data[eid][attr] = value
        LOG.debug(f"Gathered outputs: {data}")
        return data


def deserialize_q_offers(src_ids):
    # If ICT is used, we will have only one src_id
    # -> the ICT node sending the o_offers from the
    # agents. Otherwise, each sending agent is a src_id.
    # The QMarket model should always receive only the
    # agents data.
    q_offers = {}
    if len(src_ids.keys()) > 1:
        # Most likely, we won't have ICT

        for src_id, offer in src_ids.items():
            q_offers[src_id] = json.loads(offer)

    elif len(src_ids.keys()) == 1:
        # We have either only one agent or ICT
        sender_id = list(src_ids.keys())[0]
        data = list(src_ids.values())[0]
        if isinstance(data, str):
            # Most likely, we have a single agent
            data = json.loads(data)

        if "agent_id" in data:
            q_offers[sender_id] = data
        else:
            # We have either ICT or a malformed message
            for src_id, offer in data.items():
                q_offers[src_id] = json.loads(offer)
    return q_offers


def main():
    return mosaik_api.start_simulation(SimQMarket())


if __name__ == "__main__":
    main()
