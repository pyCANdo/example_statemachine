from pyrbs import PyRbs, SysVar, CanMessage


def value_mappings(rbs: PyRbs):

    msg_control_01: CanMessage = rbs.can_message.get("CAN1.Control_01")

    crlt_target_value = rbs.sysvar.add("crlt_target_value", 0)
    crtl_p_value = rbs.sysvar.add("crtl_p_value", 0.10)
    crtl_i_value = rbs.sysvar.add("crtl_i_value", 0.05)
    crtl_d_value = rbs.sysvar.add("crtl_d_value", 0.4)

    @rbs.on_start()
    def init_values():
        print("on_start")
        msg_control_01["P_Value"].phys = crtl_p_value.value
        msg_control_01["I_Value"].phys = crtl_i_value.value
        msg_control_01["D_Value"].phys = crtl_d_value.value

    @rbs.sysvar.on_change("crlt_target_value")
    def change_crlt_target_value(self: SysVar):
        msg_control_01["Target_Value"].phys = self.value

    @rbs.sysvar.on_change("crtl_p_value")
    def change_p_value(self: SysVar):
        msg_control_01["P_Value"].phys = self.value

    @rbs.sysvar.on_change("crtl_i_value")
    def change_crtl_i_value(self: SysVar):
        msg_control_01["I_Value"].phys = self.value

    @rbs.sysvar.on_change("crtl_d_value")
    def change_crtl_d_value(self: SysVar):
        msg_control_01["D_Value"].phys = self.value
