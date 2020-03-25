import warnings

from manimlib.animation.animation import Animation
from manimlib.mobject.numbers import DecimalNumber
from manimlib.utils.bezier import interpolate


class ChangingDecimal(Animation):
    """
    `manimlib.animation.numbers.ChangingDecimal`
    Changing Decimal
    ================
    WARNING: Deprecated

    Used earlier to show what the title says. It's preferred to use an `Updater`
    instead of this now. Use at your own risk.

    CONFIG Parameters:
    ------------------
    suspend_mobject_updating
    """
    CONFIG = {
        "suspend_mobject_updating": False,
    }

    def __init__(self, decimal_mob, number_update_func, **kwargs):
        self.check_validity_of_input(decimal_mob)
        self.yell_about_depricated_configuration(**kwargs)
        self.number_update_func = number_update_func
        super().__init__(decimal_mob, **kwargs)

    def check_validity_of_input(self, decimal_mob):
        if not isinstance(decimal_mob, DecimalNumber):
            raise Exception(
                "ChangingDecimal can only take "
                "in a DecimalNumber"
            )

    def yell_about_depricated_configuration(self, **kwargs):
        # Obviously this would optimally be removed at
        # some point.
        for attr in ["tracked_mobject", "position_update_func"]:
            if attr in kwargs:
                warnings.warn("""
                    Don't use {} for ChangingDecimal,
                    that functionality has been depricated
                    and you should use a mobject updater
                    instead
                """.format(attr)
            )

    def interpolate_mobject(self, alpha):
        self.mobject.set_value(
            self.number_update_func(alpha)
        )


class ChangeDecimalToValue(ChangingDecimal):
    def __init__(self, decimal_mob, target_number, **kwargs):
        start_number = decimal_mob.number
        super().__init__(
            decimal_mob,
            lambda a: interpolate(start_number, target_number, a),
            **kwargs
        )
