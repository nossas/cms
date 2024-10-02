import sys
from captcha.fields import ReCaptchaField


class ValidateOnceReCaptchaField(ReCaptchaField):
    def clean(self, values):
        # find the 'revalidating' value in stack
        frame = sys._getframe()
        max_depth = 25
        while frame and max_depth != 0:
            if "revalid" in frame.f_locals:
                return values[0]
            max_depth -= 1
            frame = frame.f_back
        return super(ValidateOnceReCaptchaField, self).clean(values)
