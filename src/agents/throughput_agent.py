"""${agent^} Agent"""
from .base_agent import DetectionAgent, AgentType

class ${agent^}Agent(DetectionAgent):
    def __init__(self, *args, **kwargs):
        agent_type = AgentType.${agent^^}
        if agent_type == AgentType.THROUGHPUT:
            agent_type = AgentType.THROUGHPUT
        super().__init__(agent_type, *args, **kwargs)
