"""AntiSAT and SFLL Verilog generators extracted from the original NPS driver."""
import random
import re
from src.utils import (format_verilog, extract_io_v, gen_busport, io_port,
                       gencc_AntiSAT, hammingcc, randKey)

class PostSAT_LL:
  def __init__(self,netlist,mode="verilog"):
    if(mode=="verilog"):
      # self.netlist=netlist
      self.netlist=format_verilog(netlist,remove_wire=True)
      self.inputs,_=extract_io_v(self.netlist,mode="input")
      self.outputs,_=extract_io_v(self.netlist,mode="output")
      self.netlist=re.sub(r"module .* ?\((.*)\);",r"module org (\1);",self.netlist)
      # if("assign" in verilog):
      #   self.gates,self.gate_count=extract_gates_v(self.netlist)
      # else:
      #   self.gates,self.gate_count=extract_gates_va(self.netlist)

      self.logval={}
      self.info()

    # elif(mode=="bench"):
    #   self.netlist=format_bench(netlist)
    #   self.inputs=extract_io_b(self.netlist,mode="input")
    #   self.outputs=extract_io_b(self.netlist,mode="output")
    #   self.gates,self.gate_count=extract_gates_b(self.netlist)

  def info(self)->None:
    print("Number of Inputs = ",len(self.inputs))
    print("Number of Outputs = ",len(self.outputs))
    # print("Total Gates Count  = ",self.gate_count)

  def AntiSat(self,key_lengthi=None):
    if(key_lengthi==None):
      inputs_key=self.inputs
    else:
      inputs_key=random.sample(self.inputs, key_lengthi)

    keyport=gen_busport("keyinput",2*len(inputs_key))
    iportnodes, inputnodes,_ = io_port(self.inputs)
    oportnodes, outputnodes,_ = io_port(self.outputs,mode="output")

    tmporgport=""
    tmpx=""
    for i in self.outputs:
      if("[" in i):
        outorgi=re.sub(r"\[","_org[",i)
      else:
        outorgi=i+"_org"

      tmpx+="assign {} = {} ^ FC;\n".format(i,outorgi)

    for i in iportnodes.split(","):
      tmporgport+=".{}({}),".format(i,i)
    for i in oportnodes.split(","):
      tmporgport+=".{}({}),".format(i,i+"_org")

    self.logval["inputs"]=inputs_key
    self.logval["len"]=key_lengthi
    tmporgport=tmporgport[:-1]

    orgoutputwires=re.sub("output","wire",re.sub(";","_org;",outputnodes))

    corrupt,portnodes_antisat,pc=gencc_AntiSAT("antisat_top", inputs_key)


    # m c,m dx,m

    top="module top({topbus});\n{topio}\n{CRwire}\n{orgmodule}\n{CRmodule}\n{Xornet}\nendmodule"
    top=top.format(
                    topbus=iportnodes+","+oportnodes+","+keyport,
                    topio="input {};\n{}\n{}\n".format(keyport,inputnodes,outputnodes),
                    CRwire=orgoutputwires+"wire {};\n".format("FC"),
                    orgmodule="\norg o1({});".format(tmporgport),
                    CRmodule=pc.format(init="to",portnodes="{%s}"%portnodes_antisat,KEY="{%s}"%keyport,Q="FC"),
                    Xornet=tmpx
                    )

    return top+"\n\n{}\n\n{}".format(corrupt,self.netlist)


  def getCRunits(self, key, HD=0,key_length=None):  # 734
    if(key_length==None):
      tmp=self.inputs
    else:
      tmp=random.sample(self.inputs, key_length)

    # tmp,outnode=circuit.MaxInputCone()
    cc= hammingcc("corrupt",tmp,HD,key)
    rsc=hammingcc("restore",tmp,HD,None)
    # cc = gencc("corrupt", tmp, key)
    # rsc = gencc("restore", tmp, None)
    # print(cc)
    return tmp,cc, rsc

  def SFLL(self,HD=0,key=None,key_lengthi=None,log=False):
    if(key_lengthi==None):
      key_length=len(self.inputs)
    else:
      key_length=key_lengthi

    if (key == None):
      key, tmpkey = randKey(key_length)
    else:
      tmpkey=format(key, "0"+str(key_length)+"b")

    inputs_key,(corrupt,_,pc),(restore,_,rc)=self.getCRunits(key=key,HD=HD,key_length=key_lengthi)
    keyport=gen_busport("keyinput",len(inputs_key))


    if(log):
      self.logval={"bin":tmpkey,"int":key,"len":len(tmpkey),"inputs":inputs_key}
    else:
      print("\n\nGENERATING LOCKING COMPARATORS:")
      print("\tNode Input Length = ",len(self.inputs))
      print("\tKey Length = ",len(tmpkey))
      print("\tKey Value in Int = ",key,"<",2**key_length)
      print("\tKey Value in Binary = ", tmpkey, "\n")


    iportnodes, inputnodes,_ = io_port(self.inputs)
    oportnodes, outputnodes,_ = io_port(self.outputs,mode="output")


    tmporgport=""
    tmpx=""
    for i in self.outputs:
      if("[" in i):
        outorgi=re.sub(r"\[","_org[",i)
      else:
        outorgi=i+"_org"

      tmpx+="assign {} = {} ^ FC ^ FR;\n".format(i,outorgi)

    for i in iportnodes.split(","):
      tmporgport+=".{}({}),".format(i,i)
    for i in oportnodes.split(","):
      tmporgport+=".{}({}),".format(i,i+"_org")
    #tmporgport+=".{}({}),".format(i,i+"")

    # for i in self.inputs:
    #   tmporgport+=".{}({}),".format(i,i+"")

    tmporgport=tmporgport[:-1]

    orgoutputwires=re.sub("output","wire",re.sub(";","_org;",outputnodes))

    top="module top({topbus});\n{topio}\n{CRwire}\n{orgmodule}\n{CRmodule}\n{Xornet}\nendmodule"
    top=top.format(
                   topbus=iportnodes+","+oportnodes+","+keyport,
                   topio="input {};\n{}\n{}\n".format(keyport,inputnodes,outputnodes),
                   CRwire=orgoutputwires+"wire {},{};\n".format("FR","FC"),
                   orgmodule="\norg o1({});".format(tmporgport),
                   CRmodule=pc.format(init="to",Q="FC")+"\n"+rc.format(init="ro",
                   key="{%s}"%keyport,
                   Q="FR"),
                   Xornet=tmpx
                   )

    return top+"\n\n{}\n\n{}\n\n{}".format(corrupt,restore,self.netlist)

  def get_log(self):
    return self.logval
