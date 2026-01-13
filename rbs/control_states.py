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

    def change_state(self, sel_state: int) -> None:

        if self.current_state == self.state_from_value(sel_state):
            return

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
