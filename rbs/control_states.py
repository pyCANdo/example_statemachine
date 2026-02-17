from statemachine import StateMachine, State, exceptions


class ControllerTargetStates(StateMachine):
    sleep = State("sleep", initial=True)
    standby = State("standby")
    speed = State("speed")
    torque = State("torque")

    to_standby = sleep.to(standby) | speed.to(standby) | torque.to(standby)
    to_speed = standby.to(speed)
    to_torque = standby.to(torque)
    to_sleep = standby.to(sleep)
    to_save_state = sleep.to(standby) | speed.to(standby) | torque.to(standby)

    def change_state(self, sel_state: int) -> str:

        if self.current_state != self.state_from_value(sel_state):
            try:
                match sel_state:
                    case 0:
                        self.to_sleep()

                    case 1:
                        self.to_standby()

                    case 2:
                        self.to_speed()

                    case 3:
                        self.to_torque()

            except exceptions.TransitionNotAllowed:
                self.to_save_state()

        return self.get_mermaid_string()

    def state_from_value(self, value: int) -> State:
        match value:
            case 0:
                return self.sleep

            case 1:
                return self.standby

            case 2:
                return self.speed

            case 3:
                return self.torque

    def get_mermaid_string(self) -> str:
        match self.current_state:
            case self.sleep:
                return SLEEP_MERMAID

            case self.standby:
                return STANDBY_MERMAID

            case self.speed:
                return SPEED_MERMAID

            case self.torque:
                return TORQUE_MERMAID

        return ""


SLEEP_MERMAID = """
graph TD
    classDef active fill:#22c55e,color:#fff,stroke:#333,stroke-width:2px;

    sleep:::active
    standby
    
    sleep --> standby
"""

STANDBY_MERMAID = """graph TD
    classDef active fill:#22c55e,color:#fff,stroke:#333,stroke-width:2px;

    sleep
    standby:::active
    speed
    torque

    %% Invisible link to force 'sleep' to be above 'standby' in the layout
    sleep ~~~ standby

    %% Actual transitions
    standby --> sleep
    standby --> speed
    standby --> torque
"""

SPEED_MERMAID = """graph TD
    classDef active fill:#22c55e,color:#fff,stroke:#333,stroke-width:2px;
    standby
    speed:::active
    standby ~~~ speed
    speed --> standby
"""


TORQUE_MERMAID = """graph TD
    classDef active fill:#22c55e,color:#fff,stroke:#333,stroke-width:2px;
    standby
    torque:::active
    standby ~~~ torque
    torque --> standby
"""
