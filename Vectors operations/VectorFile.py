from math import sqrt, acos,pi 
from decimal import Decimal,getcontext
getcontext().prec=30

class Vector(object):
    CANNOT_NORMALIZE_VECTOR_MSG='can not normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MESG='NO_UNIQUE_PARALLEL_COMPONENT_MESG'
    def __init__(self,coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x)for x in  coordinates])
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('the coordinate must nonempty')
        except TypeError:
            raise TypeError('the coordinate must be itreable')
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)
    def __eq__ (self,v):
        return self.coordinates == v.coordinates
    def plus(self,v):
        new_coordinates = [x+y for x,y in zip (self.coordinates , v.coordinates)]
        return Vector(new_coordinates) 
    def minus(self,v):
        new_coordinates = [x-y for x,y in zip(self.coordinates , v.coordinates)]
        return Vector(new_coordinates)
    def time_scalar(self,c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return new_coordinates
    def magnitude(self):
        coordinate_squared = [Decimal(x)**2 for x in self.coordinates]
        return Decimal(sqrt(sum(coordinate_squared)))
    def normalized(self):
        try:
            magnitude = self.magnitude()
            return Vector(self.time_scalar(Decimal('1.0')/magnitude))
        except ZeroDivisionError:
            raise Exception('can Not normalized zero vector')
    def dot(self,v):
        return sum([x*y for x,y in zip(self.coordinates,v.coordinates)])
    def angle(self,v,in_degree = False):
        try:
            u1= self.normalized
            u2= v.normalized
            angel_in_radianes= acos(u1.dot(u2))
            if in_degree:
                degree_per_radian= 180. / pi 
                return angel_in_radianes * degree_per_radian
            else:
                return angel_in_radianes
        except Exception as e:
            if str(e)==self.CANNOT_NORMALIZE_VECTOR_MSG:
                raise Exception('can Not compute an angle with zero vector')
            else:
                raise e
    
    def is_orthogonal_to(self,v,tolerance=1e-10):
        return abs(self.dot(v)) < tolerance
    
    def is_zero(self,tolerance=1e-10):
        return self.magnitude() < tolerance
    
    def is_parallel_to(self,v):
        return (self.is_zero() or v.is_zero() or self.angle(v)==0 or self.angle(v)== pi )
    
    def component_parallel_to(self,basis):
        try:
            u = basis.normalized()
            weight= self.dot(u)
            return Vector(u.time_scalar(weight))
        except Exception as e :
            if str(e) == self.CANNOT_NORMALIZE_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MESG)
            else:
                raise e
                
    def component_orthogonal_to(self,basis):
        try:
            projection= self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e)== self.NO_UNIQUE_PARALLEL_COMPONENT_MESG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
    def cross(self,v):
        try:
            x1,y1,z1 = self.coordinates
            x2,y2,z2 = v.coordinates
            new_coordinates = [y1*z2 - y2*z1 ,
                              -(x1*z2 - x2*z1),
                               x1*y2 - x2*y1]
            return Vector(new_coordinates)
        except ValueError as e :
            msg=str(e)
            
            if msg == 'need more than value to unpack':
                self_embedded_in_R3= Vector(self.coordinates + ('0',))
                v_embedded_in_R3= Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif(msg == 'to many values to unpack' or msg == 'need more than 1 value to unpack' ):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIM_MSG)
            else :
                raise e
                
    def area_of_parallelogram(self,v):
        cross_product= self.cross(v)
        return cross_product.magnitude()
    
    def area_of_triangle(self,v):
        return self.area_of_parallelogram(v) / Decimal('2.0')
        
        