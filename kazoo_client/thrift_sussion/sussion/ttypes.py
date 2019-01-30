#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class TSessionInfo:
  """
  Attributes:
   - id
   - type
   - uid
   - creationTime
   - lastAccessedTime
   - attributes
   - reqId
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'id', None, None, ), # 1
    (2, TType.I32, 'type', None, None, ), # 2
    (3, TType.I64, 'uid', None, None, ), # 3
    (4, TType.I64, 'creationTime', None, None, ), # 4
    (5, TType.I64, 'lastAccessedTime', None, None, ), # 5
    (6, TType.MAP, 'attributes', (TType.STRING,None,TType.STRING,None), None, ), # 6
    (7, TType.STRING, 'reqId', None, None, ), # 7
  )

  def __init__(self, id=None, type=None, uid=None, creationTime=None, lastAccessedTime=None, attributes=None, reqId=None,):
    self.id = id
    self.type = type
    self.uid = uid
    self.creationTime = creationTime
    self.lastAccessedTime = lastAccessedTime
    self.attributes = attributes
    self.reqId = reqId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.id = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.uid = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.creationTime = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.I64:
          self.lastAccessedTime = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.MAP:
          self.attributes = {}
          (_ktype1, _vtype2, _size0 ) = iprot.readMapBegin() 
          for _i4 in xrange(_size0):
            _key5 = iprot.readString();
            _val6 = iprot.readString();
            self.attributes[_key5] = _val6
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRING:
          self.reqId = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('TSessionInfo')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.STRING, 1)
      oprot.writeString(self.id)
      oprot.writeFieldEnd()
    if self.type is not None:
      oprot.writeFieldBegin('type', TType.I32, 2)
      oprot.writeI32(self.type)
      oprot.writeFieldEnd()
    if self.uid is not None:
      oprot.writeFieldBegin('uid', TType.I64, 3)
      oprot.writeI64(self.uid)
      oprot.writeFieldEnd()
    if self.creationTime is not None:
      oprot.writeFieldBegin('creationTime', TType.I64, 4)
      oprot.writeI64(self.creationTime)
      oprot.writeFieldEnd()
    if self.lastAccessedTime is not None:
      oprot.writeFieldBegin('lastAccessedTime', TType.I64, 5)
      oprot.writeI64(self.lastAccessedTime)
      oprot.writeFieldEnd()
    if self.attributes is not None:
      oprot.writeFieldBegin('attributes', TType.MAP, 6)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attributes))
      for kiter7,viter8 in self.attributes.items():
        oprot.writeString(kiter7)
        oprot.writeString(viter8)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    if self.reqId is not None:
      oprot.writeFieldBegin('reqId', TType.STRING, 7)
      oprot.writeString(self.reqId)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class SaveAttrReq:
  """
  Attributes:
   - clientId
   - sign
   - sessId
   - attrs
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'clientId', None, None, ), # 1
    (2, TType.STRING, 'sign', None, None, ), # 2
    (3, TType.STRING, 'sessId', None, None, ), # 3
    (4, TType.MAP, 'attrs', (TType.STRING,None,TType.STRING,None), None, ), # 4
  )

  def __init__(self, clientId=None, sign=None, sessId=None, attrs=None,):
    self.clientId = clientId
    self.sign = sign
    self.sessId = sessId
    self.attrs = attrs

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.clientId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.sign = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.sessId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.MAP:
          self.attrs = {}
          (_ktype10, _vtype11, _size9 ) = iprot.readMapBegin() 
          for _i13 in xrange(_size9):
            _key14 = iprot.readString();
            _val15 = iprot.readString();
            self.attrs[_key14] = _val15
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('SaveAttrReq')
    if self.clientId is not None:
      oprot.writeFieldBegin('clientId', TType.I64, 1)
      oprot.writeI64(self.clientId)
      oprot.writeFieldEnd()
    if self.sign is not None:
      oprot.writeFieldBegin('sign', TType.STRING, 2)
      oprot.writeString(self.sign)
      oprot.writeFieldEnd()
    if self.sessId is not None:
      oprot.writeFieldBegin('sessId', TType.STRING, 3)
      oprot.writeString(self.sessId)
      oprot.writeFieldEnd()
    if self.attrs is not None:
      oprot.writeFieldBegin('attrs', TType.MAP, 4)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.attrs))
      for kiter16,viter17 in self.attrs.items():
        oprot.writeString(kiter16)
        oprot.writeString(viter17)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class SaveAttrRsp:

  thrift_spec = (
  )

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('SaveAttrRsp')
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class GetSessReq:
  """
  Attributes:
   - clientId
   - sign
   - sessId
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'clientId', None, None, ), # 1
    (2, TType.STRING, 'sign', None, None, ), # 2
    (3, TType.STRING, 'sessId', None, None, ), # 3
  )

  def __init__(self, clientId=None, sign=None, sessId=None,):
    self.clientId = clientId
    self.sign = sign
    self.sessId = sessId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.clientId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.sign = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.sessId = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('GetSessReq')
    if self.clientId is not None:
      oprot.writeFieldBegin('clientId', TType.I64, 1)
      oprot.writeI64(self.clientId)
      oprot.writeFieldEnd()
    if self.sign is not None:
      oprot.writeFieldBegin('sign', TType.STRING, 2)
      oprot.writeString(self.sign)
      oprot.writeFieldEnd()
    if self.sessId is not None:
      oprot.writeFieldBegin('sessId', TType.STRING, 3)
      oprot.writeString(self.sessId)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DelSessReq:
  """
  Attributes:
   - clientId
   - sign
   - sessId
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'clientId', None, None, ), # 1
    (2, TType.STRING, 'sign', None, None, ), # 2
    (3, TType.STRING, 'sessId', None, None, ), # 3
  )

  def __init__(self, clientId=None, sign=None, sessId=None,):
    self.clientId = clientId
    self.sign = sign
    self.sessId = sessId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.clientId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.sign = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.sessId = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DelSessReq')
    if self.clientId is not None:
      oprot.writeFieldBegin('clientId', TType.I64, 1)
      oprot.writeI64(self.clientId)
      oprot.writeFieldEnd()
    if self.sign is not None:
      oprot.writeFieldBegin('sign', TType.STRING, 2)
      oprot.writeString(self.sign)
      oprot.writeFieldEnd()
    if self.sessId is not None:
      oprot.writeFieldBegin('sessId', TType.STRING, 3)
      oprot.writeString(self.sessId)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DelSessRsp:

  thrift_spec = (
  )

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DelSessRsp')
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class RecovKickedReq:
  """
  Attributes:
   - clientId
   - sign
   - sessId
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'clientId', None, None, ), # 1
    (2, TType.STRING, 'sign', None, None, ), # 2
    (3, TType.STRING, 'sessId', None, None, ), # 3
  )

  def __init__(self, clientId=None, sign=None, sessId=None,):
    self.clientId = clientId
    self.sign = sign
    self.sessId = sessId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.clientId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.sign = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.sessId = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('RecovKickedReq')
    if self.clientId is not None:
      oprot.writeFieldBegin('clientId', TType.I64, 1)
      oprot.writeI64(self.clientId)
      oprot.writeFieldEnd()
    if self.sign is not None:
      oprot.writeFieldBegin('sign', TType.STRING, 2)
      oprot.writeString(self.sign)
      oprot.writeFieldEnd()
    if self.sessId is not None:
      oprot.writeFieldBegin('sessId', TType.STRING, 3)
      oprot.writeString(self.sessId)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class RecovKickedRsp:
  """
  Attributes:
   - resultCode
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'resultCode', None, None, ), # 1
  )

  def __init__(self, resultCode=None,):
    self.resultCode = resultCode

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.resultCode = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('RecovKickedRsp')
    if self.resultCode is not None:
      oprot.writeFieldBegin('resultCode', TType.I32, 1)
      oprot.writeI32(self.resultCode)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)