import rhinoscriptsyntax as rs
import operator

class Intersection():
    def __init__(self, obj):
      self.obj = obj
      self.getDimension()

    def getDimension(self):
      box = rs.BoundingBox(self.obj)
      diag = box[0]-box[2]
      self.width = diag[0]
      self.depth = diag[1]
      self.z = box[0][2]
    
class Slice():
    def __init__(self, inter):
      self.z = inter.z
      self.inters = []
      self.add(inter)

    def hasSameZ(self,inter, tol=1e-10):
        return abs(self.z - inter.z)<tol

    def add(self, inter):
        self.inters.append(inter)

    def getMaxWidth(self):
        widths = []
        for inter in self.inters:
            widths.append( abs(inter.width) )
        return max(widths)

    def move(self, offset):
      for inter in self.inters:
        xform = rs.XformTranslation([offset,0,-self.z])
        rs.TransformObjects( inter.obj, xform, True )
        rs.HideObject (inter.obj)
      return self.getMaxWidth()


if __name__ == '__main__':

    tolerance = 1e-10
    offset = 0

    objs = rs.GetObjects("Select objects to move")
    margin = rs.GetReal("Enter a margin value", 5.0)
    tolerance = rs.GetReal("Enter a tolerance value", 1e-10)

    inters = []
    for obj in objs:
        inter = Intersection(obj) 
        inters.append(inter )

    slices = []
    slices.append( Slice(inters[0]) )
    for inter in inters[1:]:
        hasFoundAFriend = False
        for slice in slices:
            if (slice.hasSameZ(inter,tolerance)):
                slice.add(inter)
                hasFoundAFriend = True
                break
        if hasFoundAFriend==False:
            slices.append( Slice(inter) )


    print "I found "+str(len(slices))+" slices! "
    print "If this number is not correct change the tolerance."

    slices = sorted(slices, key=operator.attrgetter('z'))

    for slice in slices:
        offset += slice.move(offset)+ margin
    print "Done"
    
