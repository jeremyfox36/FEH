class AMAX(object):
    def __init__(self, file_type: str, st_no: int, am_details: str, am_rejected: list, am_values: list) -> object:
        self.File_Type = file_type
        self.St_No = st_no
        self.AM_Details = am_details
        self.AM_Rejected = am_rejected
        self.AM_Values = am_values


a = AMAX('AM', 2001, 'water year : Oct', [1974, 1975], [23, 24, 25, 26])

print
a.File_Type
print
a.St_No
print
a.AM_Details
print
a.AM_Rejected
print
a.AM_Values
