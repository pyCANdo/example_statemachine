from pyrbs import PyRbs, CanMessage, CanSignal, SysVar, Timer
from control_states import ControllerTargetStates, SLEEP_MERMAID
from value_mapping import value_mappings

rbs = PyRbs(dashboard=True, log_all=True)
value_mappings(rbs)

msg_control_01: CanMessage = rbs.can_message.get("CAN1.Control_01")
sig_control_01_activate: CanSignal = rbs.can_signal.get("CAN1.Control_01.Activate")
crtl_activate: SysVar = rbs.sysvar.add("crtl_activate", 0)

timer_100ms: Timer = rbs.timer.add("timer_100ms", 0.1, active_on_start=False)
select_mode: SysVar = rbs.sysvar.add("select_mode", 0)
ctrl_state: ControllerTargetStates = rbs.state.add_statemachine(
    "ctrl_state", ControllerTargetStates
)
state_mermaid: SysVar = rbs.sysvar.add("state_mermaid", SLEEP_MERMAID)


@rbs.timer.on("timer_100ms")
def on_timer_100ms(self: Timer):
    msg_control_01.send()


@rbs.sysvar.on_change("select_mode")
def change_mode(self: SysVar):

    print(f"change of select_mode: {self.value}")
    state_mermaid.value = ctrl_state.change_state(self.value)


@rbs.state.on_enter("ctrl_state", "sleep")
def on_enter_sleep(self: ControllerTargetStates):
    select_mode.value = 0
    timer_100ms.stop()


@rbs.state.on_exit("ctrl_state", "sleep")
def on_exit_sleep(self: ControllerTargetStates):
    timer_100ms.start()


@rbs.state.on_enter("ctrl_state", "standby")
def on_enter_standby(self: ControllerTargetStates):
    select_mode.value = 1
    msg_control_01["Mode"].raw = 0


@rbs.state.on_enter("ctrl_state", "speed")
def on_enter_speed(self: ControllerTargetStates):
    msg_control_01["Mode"].raw = 1


@rbs.state.on_enter("ctrl_state", "torque")
def on_enter_torque(self: ControllerTargetStates):
    msg_control_01["Mode"].raw = 2


@rbs.sysvar.on_change("crtl_activate")
def on_change_crtl_activate(self: SysVar):
    sig_control_01_activate.raw = self.value
