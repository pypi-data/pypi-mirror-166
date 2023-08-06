"""
Minimalistic reactive power market based on sensitivity calculation
(not optimization)

- Does not use voltage measurements, but calculates them instead for
  Q=0
- sensitivity is calculated once at the beginning of each step
- Over- and undervoltage at the same time not implemented
- PU-nodes/pandapower gens not implemented/tested yet

TODO:
- clean sens calculation
- add P to sens calc
- Deal with double voltage violation
- Loads auch als Anbieter berücksichtigen? (Vorzeichen!)
- Dokumentation ergänzen / README füllen
- Add PU-nodes to sensitivity calculation


Author: Thomas Wolgast <thomas.wolgast@uol.de>

"""

import json
import logging
from collections import defaultdict
from typing import Optional

import numpy
import pandapower as pp
import scipy
from pandapower.pd2ppc import _pd2ppc
from pandapower.pypower.bustypes import bustypes

LOG = logging.getLogger(__name__)


class QMarketModel:
    def __init__(self, params: dict):
        self.net = None
        self.agent_bus_map = params["agent_bus_map"]
        self.u_max = params["u_max"]
        self.u_min = params["u_min"]
        self.market_clearing = self._run_merit_order_market_clearing

        # Inputs
        self.net: Optional[pp.pandapowerNet] = None
        self.q_accept: dict = defaultdict(float)
        self.q_offers = None

    def set_grid_state(self, grid_json):
        self.net = pp.from_json_string(grid_json)

    def step(self):
        """Perform a step of the qmarket.

        Collect all reactive power offers, find offers that solve
        voltage problems in the cheapest way, and return what reactive
        power values should be set.

        Parameters
        ----------
        grid_state: pandapower grid
            The current grid state
        q_offers: dict?
            Offers from the market agents.

        """

        LOG.debug("Agent_offers: %s", self.q_offers)
        # Default setting: accept no offers (q=0.0 => minimal costs)
        self.q_accept = defaultdict(float)

        self.market_clearing(self.q_offers)

        # Eval: delete!
        if self.q_accept:
            for idx in self.net.sgen.index:
                for agent_id, q_value in self.q_accept.items():
                    bus = self._get_offering_bus(agent_id)
                    if self.net.sgen.bus[idx] == bus:
                        self.net.sgen.q_mvar[idx] += q_value
                        continue
            pp.runpp(self.net)
            LOG.info(json.dumps({"Status": "Market clearing finished"}))
            LOG.info(
                json.dumps(
                    {
                        "Expected voltages": self.net.res_bus.vm_pu.values.tolist()
                    }
                )
            )

    def _run_opf_market_clearing(self, q_offers):
        # TODO: Delete?!
        """Run optimal powerflow-based market clearing.

        The merit order method is a bit too simplistic and maybe not
        really suited for a publication and serious simulations. An
        alternative would be to use an OPF to best the best bids.
        However, an OPF would require a quadratic cost function...
        Or a separate gen for every single bid, which changes the net
        object.

        """
        pass

    def _run_merit_order_market_clearing(self, q_offers):
        """Run merit order-based market clearing.

        Identify voltage constraint violations and find cheapest/most
        effective reactive power offers that can solve the issue at
        minimal costs. No offers are accepted, when there is no voltage
        violation.

        """
        LOG.info(json.dumps({"Status": "Run merit order market clearing"}))
        # Reset all q-values to baseline to perform market clearing
        self.net.sgen.q_mvar = 0.0
        self.sensitivity = get_sensitivity(self.net)["dUdQ"]
        LOG.debug("Voltages: %s", list(self.net.res_bus.vm_pu))

        # Check for violations
        overvolt = max(self.net.res_bus.vm_pu) > self.u_max
        undervolt = min(self.net.res_bus.vm_pu) < self.u_min

        LOG.info(json.dumps({"Voltage_violation": overvolt or undervolt}))
        if not overvolt and not undervolt:
            # No voltage violation -> no q-demand
            LOG.info(json.dumps({"Qset_sum": 0.0}))
            return

        if overvolt and undervolt:
            raise NotImplementedError(
                "Overvolt and undervolt at the same time! Not yet implemented"
            )
            # TODO: try to clear both at the same time? Or one after
            # the other? Difficult to solve without optimization!
            # TODO: Handle worst violation to be more robust
        elif undervolt:
            violated_bus = self.net.res_bus.vm_pu.idxmin()
            LOG.info(
                json.dumps(
                    {
                        "Status": "Undervoltage",
                        "voltage": round(min(self.net.res_bus.vm_pu), 4),
                        "violated bus": int(violated_bus),
                    }
                )
            )
            sorted_offers = self._sort_offers(
                self.sensitivity, q_offers, violated_bus
            )[0]
            constraint = self.u_min
        elif overvolt:
            violated_bus = self.net.res_bus.vm_pu.idxmax()
            LOG.info(
                json.dumps(
                    {
                        "Status": "Overvoltage",
                        "voltage": round(
                            max(self.net.res_bus.vm_pu.tolist()), 4
                        ),
                        "violated bus": int(violated_bus),
                    }
                )
            )
            sorted_offers = self._sort_offers(
                self.sensitivity, q_offers, violated_bus
            )[1]
            constraint = self.u_max

        # How big is required voltage change?
        if overvolt:
            # Sensitivity value is assumed to be linear, but is actually
            # not! 4% is a good estimation to counteract negative
            # effects of that phenomenon.
            factor = 0.96
        elif undervolt:
            factor = 1.04
        delta_u_set = factor * (
            constraint - self.net.res_bus.vm_pu[violated_bus]
        )

        # Accept cheapest offers until delta_u_set is achieved to clear
        # violation
        for agent_id, max_delta_u, price in sorted_offers:
            LOG.info(json.dumps({"Required delta_u": round(delta_u_set, 4)}))
            # Accept offer
            offering_bus = self._get_offering_bus(agent_id)
            if overvolt:
                max_delta_u = -max_delta_u
            if undervolt:
                possible_delta_u = min(max_delta_u, delta_u_set)
            elif overvolt:
                possible_delta_u = max(max_delta_u, delta_u_set)

            sensitivity_value = self.sensitivity[violated_bus][offering_bus]
            if possible_delta_u == 0.0 or sensitivity_value == 0:
                # This reactive power provider cannot solve the problem
                continue

            self.q_accept[agent_id] += possible_delta_u / sensitivity_value

            # Check whether clearing is be expected to be successful
            if ((max_delta_u < delta_u_set) and overvolt) or (
                (max_delta_u > delta_u_set) and undervolt
            ):
                break

            # Update required voltage delta for next offer
            delta_u_set -= max_delta_u
            # TODO: update sens again to be more precise?

        LOG.info(
            json.dumps({"Qset_sum": round(sum(self.q_accept.values()), 4)})
        )

    def _get_offering_bus(self, agent_id):
        """Assumption: The market model gets a mapping agent_id<->bus
        at init time."""
        return self.agent_bus_map[agent_id]

    def _sort_offers(self, sens, q_offers: dict, violated_bus: int):
        """Sort the market agents offers.

        Create sorted lists starting with least expensive reactive
        power to most expensive to clear a violation at a given bus.
        Separated for undervoltage and overvoltage situation (pos and
        neg reactive power).

        """
        overvolt_offers = []
        undervolt_offers = []
        for ict_channel_id, offer in q_offers.items():
            if offer is None or not offer:
                continue
            # TODO this is a quick workaround, probably won't work without the ict simulation
            # offer = json.loads(offer_json)
            # if isinstance(offer_json, str):
            #     offer = json.loads(offer_json)
            # else:
            #     offer = offer_json
            # if "agent_id" not in offer_json:
            #     continue
            # TODO end
            # for offer in offers:
            agent_id = offer["agent_id"]
            offering_bus = self._get_offering_bus(agent_id)
            sens_value = sens[violated_bus][offering_bus]
            # The higher the sensitivity the lower the q-demand
            # -> sensitivity^-1=weight!
            if sens_value == 0:
                # This generator/agent cannot help with the problem -> filter out
                continue
            else:
                weighted_price = offer["q_price"] / sens_value

            if offer["q_min"] < 0:
                max_delta_u = offer["q_min"] * sens_value
                overvolt_offers.append(
                    (agent_id, -max_delta_u, weighted_price)
                )
            if offer["q_max"] > 0:
                max_delta_u = offer["q_max"] * sens_value
                undervolt_offers.append(
                    (agent_id, max_delta_u, weighted_price)
                )

        # Sort by price
        overvolt_offers.sort(key=lambda tup: tup[2])
        undervolt_offers.sort(key=lambda tup: tup[2])

        return undervolt_offers, overvolt_offers


def get_sensitivity(net):
    """Building the sensitivity matrix for a given net.

    dU_i = S_i,j * dQ_j -> S_i,j = sens['dUdQ'][i][j]
    """

    # How to handle PU nodes? We have no sensors!
    # -> TODO: test it
    pp.runpp(net, enforce_q_lims=True)

    J = net._ppc["internal"]["J"]
    # Inverse of the Jacobian equals the sensitivity matrix
    J_inv = scipy.sparse.linalg.inv(scipy.sparse.csc_matrix(J))

    # Get bus mapping from internal data structures
    _, ppci = _pd2ppc(net)
    ref, pv, pq = bustypes(ppci["bus"], ppci["gen"])
    pvpq = numpy.r_[pv, pq]

    # Number of (electrically different) buses
    n_PUPQ = len(pvpq)
    n_PQ = len(pq)
    try:
        slack_bus = int(ref)
    except TypeError:
        raise TypeError("Only one external grid possible at the moment!")

    # Extract both sub-matrices from inverse jacobian
    dUdQ = J_inv[n_PUPQ : n_PUPQ + n_PQ, n_PUPQ : n_PUPQ + n_PQ].toarray()
    # dUdP = J_inv[n_PUPQ:n_PUPQ+n_PQ, 0:n_PUPQ].toarray()

    # Assign "electrical" buses to "real" buses
    ppc_indices = list(net._pd2ppc_lookups["bus"])
    # Example: [0, 1, 1, 2, 2, 3, 4] means "real" buses 1 and 2 are
    # electrically equivalent -> both are "electrical bus" 1. The same
    # goes for "real" buses 3 and 4 (both together are
    # "electrical bus" 2). compare:
    # https://github.com/e2nIEE/pandapower/blob/develop/tutorials/
    # internal_datastructure.ipynb

    for idx, num in enumerate(ppc_indices):
        ppc_indices[idx] = num.item()  # Convert to "normal" integers

    # Reduce multiple buses which are electrical identical to singular
    # bus
    n_PUPQ_trans = len(set(ppc_indices)) - 1  # Minus slack bus
    if net._pd2ppc_lookups["gen"] is None:
        # No generator buses
        n_PU_trans = 0
    else:
        # TODO: Are PU nodes even allowed? -> Test + add!
        n_PU_trans = len(set(net._pd2ppc_lookups["gen"]))
    n_PQ_trans = n_PUPQ_trans - n_PU_trans

    # Sensitivity matrix must be transformed to pd (currently ppc)!
    sens = {}
    # Get sensitivity from "real" electrical buses
    sens["dUdQ"] = [
        list(dUdQ[bus_idx, :n_PQ_trans]) for bus_idx in range(n_PQ_trans)
    ]
    # Add sensitivity of Slack bus (=0)
    sens["dUdQ"].insert(slack_bus, list(numpy.zeros(n_PUPQ_trans)))
    for idx, vector in enumerate(sens["dUdQ"]):
        sens["dUdQ"][idx].insert(slack_bus, 0.0)

    # TODO: If required, add other submatrices
    # sens['dUdP'] = [list(dUdP[bus_idx, :n_PUPQ_trans])
    #                       for bus_idx in range(n_PQ_trans)]

    return sens
