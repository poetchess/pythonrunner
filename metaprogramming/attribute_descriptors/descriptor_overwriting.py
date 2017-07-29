# Regardless of whether a descriptor is overriding or not, it can be overwritten
# by assignment to the class. This is a monkey-patching technique.

# But in this example, the descriptors are replaced by integers, which would
# break any class that depended on the descriptors for proper operation.
# It also reveals another asymmetry regarding reading and writing attributes:
#   although the reading of a class attribute can be controlled by a descriptor
#   with __get__ attached to the managed class, the writing of a class attribute
#   cannot be handled by a descriptor with __set__ attached to the same class.
if __name__ == '__main__':
    from descriptorkinds import Managed
    obj = Managed()
    Managed.over = 1
    Managed.over_no_get = 2
    Managed.non_over = 3
    print('obj.over: {}, obj.over_no_get: {}, obj.non_over: {}'.format(
          obj.over, obj.over_no_get, obj.non_over))

