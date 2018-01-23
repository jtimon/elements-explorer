
from . import Field, FieldError

class NumericField(Field):

    def __init__(self, lt=None, gt=None, le=None, ge=None, 
                 lt_msg=None, gt_msg=None, le_msg=None, ge_msg=None,
                 **kwargs):

        self.lt, self.gt, self.le, self.ge = lt, gt, le, ge
        self.lt_msg, self.gt_msg, self.le_msg, self.ge_msg = lt_msg, gt_msg, le_msg, ge_msg

        super(NumericField, self).__init__(**kwargs)

    def validate(self, model, name):
        super(NumericField, self).validate(model, name)

        value = getattr(model, name)
        if value is None:
            return None

        if self.lt is not None and not value < self.lt:            
            raise FieldError(self.lt_msg or '"%s" must be less than %s' % (name, self.lt))
        if self.gt is not None  and not value > self.gt:
            raise FieldError(self.gt_msg or '"%s" must be greater than %s' % (name, self.gt))
        if self.le is not None  and not value <= self.le:
            raise FieldError(self.le_msg or '"%s" must be less than or equal to %s' % (name, self.le))
        if self.ge is not None and not value >= self.ge:
            raise FieldError(self.ge_msg or '"%s" must be greater than or equal to %s' % (name, self.ge))

        return value
