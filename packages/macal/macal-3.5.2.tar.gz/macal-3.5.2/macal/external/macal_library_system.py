# Filename:       | macal_library_system.py
# Author:         | Marco Caspers
# Version:        | 3.5
# Description:
#
# Macal System Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 14-05-2022: detached from class MacalLibrary and now implemented through include system.mcl with "external" hooks to this module.
#

"""System library implementation"""


import platform
import macal


def console(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of console function"""
    macal.ValidateFunction(name, func, scope)
    out_str = ""
    # Since the param is type PARAMS we can have any number of arguments passed into us as an array.
    param_list = params[0].get_value()
    if len(param_list) > 0:
        if param_list[0].format:
            console_fmt(param_list)
            return
        for param in param_list:
            out_str = f"{out_str}{macal.ParamToString(param)}"
        print(out_str)
    else:
        print()



def console_fmt(args):
    """Console string formatting function"""
    fmt  = args[0].get_value()
    args = args[1:]
    arg_count = len(args)
    fmt_count = fmt.count("{}")
    if arg_count != fmt_count:
        raise RuntimeError("Console(args): Number of arguments ({}) mismatch with format string ({})".format(arg_count, fmt_count))
    argv = []
    for arg in args:
        argv.append(macal.ParamToString(arg))
    print(fmt.format(*argv))



def record_has_field(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func, True)
    fieldname = macal.GetParamValue(params, "fieldname")
    record = macal.GetParamValue(params, "rec")
    result =  fieldname in record
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def Type(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type()
    scope.SetReturnValue(result, macal.VariableTypes.STRING)



def IsString(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.STRING
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsInt(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.INT
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsFloat(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.FLOAT
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsBool(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.BOOL
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsRecord(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.RECORD
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsArray(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.ARRAY
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsAny(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.ANY
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsParams(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.PARAMS
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsFunction(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.FUNCTION
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def IsNil(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = macal.MacalScope.get_value_type(macal.GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == macal.VariableTypes.NIL
    scope.SetReturnValue(result, macal.VariableTypes.BOOL)



def create_list(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of create_list function"""
    macal.ValidateFunction(name, func, scope)
    result = []
    param_list = params[0].get_value()
    if len(param_list) > 0:
        for param in param_list:
            result.append(param.get_value())
    else:
        raise RuntimeError("List requires at least one argument.")
    scope.SetReturnValue(result, macal.VariableTypes.ARRAY)



def GetPlatform(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of platform function"""
    macal.ValidateFunction(name, func, scope)
    scope.SetReturnValue(platform.system(), macal.VariableTypes.STRING)


        
def ShowVersion(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of ShowVersion function"""
    macal.ValidateFunction(name, func, scope)
    print("Version: ",macal.__version__)
    print("Author:  ", macal.__author__)
    print("Credits:")
    print(macal.__credits__)



def Items(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of Items function used in conjunction with foreach for iterating over records.  Items returns key/value pairs."""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = macal.GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Items requires a record as argument.")
    pv = [{key: value} for key, value in value.items()]
    scope.SetReturnValue(pv,macal.VariableTypes.ARRAY)



def RecordKeyValue(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of Key function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = macal.GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict) or len(value) > 1:
        raise RuntimeError("Key requires a key/value pair that is returned when doing a foreach over items(x).")
    for k, v in value.items(): #there are different ways, but this is by far the most simple and safe way to do it.
        key = k
    scope.SetReturnValue(key,macal.VariableTypes.STRING)



def RecordKeys(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of Key function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = macal.GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Keys requires a record as input.")
    val = [k for k in value.keys()]
    scope.SetReturnValue(val,macal.VariableTypes.ARRAY)

    

def RecordItemValue(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = macal.GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict) or len(value) > 1:
        raise RuntimeError("Value requires a key/value pair that is returned when doing a foreach over items(x).")
    for k, v in value.items(): #there are different ways, but this is by far the most simple and safe way to do it.
        val = v
    scope.SetReturnValue(val,macal.VariableTypes.STRING)



def RecordValues(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = macal.GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Values requires a record as input.")
    val = [v for v in value.values()]
    scope.SetReturnValue(val,macal.VariableTypes.ARRAY)



def GetVariableValue(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        vv = macal.GetIndexedVariableValue(var, index)
    else:
        vv = var.get_value()
    if isinstance(vv, macal.MacalVariable):
        finalvar = scope.find_variable_outside(vv.name)
        fvv = finalvar.get_value()
        fvt = finalvar.get_type()
        scope.SetReturnValue(fvv, fvt)
    else:
        raise RuntimeError("Invalid use of getValue. GetValue can only be used inside a function on an argument marked as variable.")



def GetVariableType(func: macal.MacalFunction, name: str, params: list, scope: macal.MacalScope):
    """Implementation of record_has_field function"""
    macal.ValidateFunction(name, func, scope)
    macal.ValidateParams(name, params, scope, func)
    var, index = macal.GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        vv = macal.GetIndexedVariableValue(var, index)
    else:
        vv = var.get_value()
    if isinstance(vv, macal.MacalVariable):
        finalvar = scope.find_variable_outside(vv.name)
        fvt = finalvar.get_type()
        scope.SetReturnValue(fvt, macal.VariableTypes.STRING)
    else:
        raise RuntimeError("Invalid use of getValue. GetValue can only be used inside a function on an argument marked as variable.")
