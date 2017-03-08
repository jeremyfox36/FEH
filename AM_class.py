class AMAX(object):
    
    def __init__(self, File_Type, St_No, AM_Details, AM_Rejected, AM_Values):
        self.File_Type = File_Type
        self.St_No = St_No
        self.AM_Details = AM_Details
        self.AM_Rejected = AM_Rejected
        self.AM_Values = AM_Values

    
a = AMAX('AM', 2001, 'water year : Oct', [1974,1975], [23,24,25,26])

print a.File_Type
print a.St_No
print a.AM_Details
print a.AM_Rejected
print a.AM_Values