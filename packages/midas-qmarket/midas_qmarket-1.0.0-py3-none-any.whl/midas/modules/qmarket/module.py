"""MIDAS upgrade module for QMarket.

Author: Stephan Balduin <stephan.balduin@offis.de>

"""

import logging
from typing import Any, Dict

from midas.util.upgrade_module import UpgradeModule
from pyparsing import Optional

LOG = logging.getLogger(__name__)


class QMarketModule(UpgradeModule):
    """QMarket upgrade module for MIDAS 1.0."""

    def __init__(self):
        super().__init__(
            module_name="qmarket",
            default_scope_name="midasmv",
            default_sim_config_name="QMarket",
            default_import_str="midas.modules.qmarket.simulator:SimQMarket",
            default_cmd_str="%(python)s -m midas.modules.qmarket.simulator %(addr)s",
            log=LOG,
        )

        self.models = {
            "SimQMarket": {
                "attrs": ["agent_bus_map", "u_max", "u_min"],
                "GOA": [("grid", "grid_state")],
                "MarketAgents": {
                    "name": "MarketAgentModel",
                    "from": [("reactive_power_offer", "q_offers")],
                    "to": [("q_accept", "q_set")],
                    "initial_data": {"q_accept": None},
                },
            }
        }
        self.full_id: Optional[str] = None
        self.num_agents: int = 0

    def check_module_params(self, module_params: Dict[str, Any]):
        """Check the module params and provide default values."""
        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("u_min", 0.96)
        module_params.setdefault("u_max", 1.04)
        module_params.setdefault("module_name_market_agents", "marketagents")
        module_params.setdefault("module_name_operator", "goa")

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("u_min", module_params["u_min"])
        self.sim_params.setdefault("u_max", module_params["u_max"])
        self.sim_params.setdefault(
            "module_name_market_agents",
            module_params["module_name_market_agents"],
        )
        self.sim_params.setdefault(
            "module_name_operator", module_params["module_name_operator"]
        )
        self.sim_params.setdefault("agent_bus_map", {})

        if self.scenario.base.no_rng:
            self.sim_params["seed"] = self.scenario.create_seed()
        else:
            self.sim_params.setdefault("seed", self.scenario.create_seed())

    def start_models(self):
        """Start all models defined in the mapping of a certain simulator."""

        if not self.sim_params["agent_bus_map"]:
            self.sim_params["agent_bus_map"] = {
                full_id: bus
                for full_id, bus in self.find_agent_bus_map().values()
            }

        model_key = self.scenario.generate_model_key(self, "qmarket")
        params = {}

        for attr in self.models["SimQMarket"]["attrs"]:
            params[attr] = self.sim_params[attr]

        self.full_id = self.start_model(model_key, "QMarketModel", params)

    def connect(self):
        self._connect_to_goa()
        self._connect_to_market_agents()

    def connect_to_db(self):
        pass

    def find_agent_bus_map(self):
        market_mappings = self.scenario.get_shared_mappings(
            self.sim_params["module_name_market_agents"]
        )
        for key, mapping in market_mappings.items():
            if "agent_bus_map" in key:
                return mapping

        raise ValueError("No agent bus map found!")

    def gen_mod_key(self):
        return f"{self.name}_{self.sim_name}_qmarket"

    def _connect_to_goa(self):
        model_key = self.scenario.generate_model_key(self, "qmarket")

        # We know there is only one operator
        # TODO Allow multiple operators in a
        # scenario ONCE PYRATE HAS FINISHED
        goa_key, _ = self.scenario.find_first_model(
            self.sim_params["module_name_operator"]
        )
        self.connect_entities(
            goa_key, model_key, self.models["SimQMarket"]["GOA"]
        )

    def _connect_to_market_agents(self):
        qmarket_key = self.scenario.generate_model_key(self, "qmarket")
        agent_bus_map = self.find_agent_bus_map()
        ict_mappings = self.scenario.get_ict_mappings()

        sender_attrs = self.models["SimQMarket"]["MarketAgents"]["from"]
        receiver_attrs = self.models["SimQMarket"]["MarketAgents"]["to"]
        initial_data = self.models["SimQMarket"]["MarketAgents"][
            "initial_data"
        ]
        for agent_key in agent_bus_map:
            self.num_agents += 1
            if self.scenario.base.with_ict:
                # provides a list of mapping, that ict can use to see
                # where to connect between the entities if initial data
                # is needed, it can be given. if not given, it is not
                # needed
                ict_mappings.append(
                    {
                        "sender": agent_key,
                        "receiver": qmarket_key,
                        "sender_before_ict": False,
                        "receiver_before_ict": False,
                        "attrs": sender_attrs,
                    }
                )
                ict_mappings.append(
                    {
                        "sender": qmarket_key,
                        "receiver": agent_key,
                        "sender_before_ict": False,
                        "receiver_before_ict": False,
                        "attrs": receiver_attrs,
                        "initial_data": list(initial_data.keys()),
                    }
                )
            else:
                self.connect_entities(agent_key, qmarket_key, sender_attrs)
                self.connect_entities(
                    qmarket_key,
                    agent_key,
                    receiver_attrs,
                    time_shifted=True,
                    initial_data=initial_data,
                )

    def _get_agent_list(self):
        agents = list()
        akey = f"marketagents_{self.sim_name}"
        amod_name = self.models["SimQMarket"]["MarketAgents"]["name"]
        for key, entity in self.scenario.items():
            if akey in key and amod_name.lower() in key:
                agents.append(entity)

        return agents

    def get_sensors(self):
        """Create sensors of the qmarket.

        The sensors of the qmarket are the market results, namely the
        accepted reactive power values.

        TODO: Maybe the respective prices could be added as well.
        TODO: Maybe all agents should see the whole market result
        -> only one sensor in total

        """
        low = -1
        high = 1  # TODO

        # agents = self._get_agent_list()
        for idx in range(self.num_agents):
            space = (
                f"Box(low={low}, high={high}, shape=(1,), dtype=np.float32)"
            )
            sensor = {
                "sensor_id": f"{self.full_id}.q_set_{idx}",
                "observation_space": space,
            }
            self.scenario.sensors.append(sensor)

        self.scenario.sensors.append(
            {
                "sensor_id": f"{self.full_id}.q_accept",
                "observation_space": space,
            }
        )

    def get_actuators(self):
        """Create actuators of the qmarket.

        The actuators for the market are the agent bids, which consist
        of two values: the relative amount of reactive power that is
        offered and the respective price.

        """
        # full_id = self.scenario[self.gen_mod_key()].full_id
        low = "[-1, -100]"
        high = "[1, 100]"
        # Negative prices necessary so that negative q can generate
        # profit TODO: arbitrary bidding values currently

        for idx in range(self.num_agents):  # Assumption: One unit per agent
            space = (
                f"Box(low={low}, high={high}, shape=(2,), dtype=np.float32)"
            )
            act = {
                "actuator_id": f"{self.full_id}.agent_bid_{idx}",
                "action_space": space,
            }
            self.scenario.actuators.append(act)
